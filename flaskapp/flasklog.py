# -*- coding: utf-8 -*-
"""
    flaskapp.flasklog
    ~~~~~~~~~~~~~~~~~

    All logger functions.
"""


from flaskapp import app


def set_loggers():
    """ Set loggers here, by default errors are send to a file and email"""
    if not app.debug:
        import logging
        from logging.handlers import SMTPHandler
        from logging import Formatter, FileHandler
        #Loading settings vars
        log_smtp_srv = app.config['LOG_SMTP_SRV']
        log_eml_sender = app.config['LOG_EML_SENDER']
        log_eml_admins = app.config['LOG_EML_ADMINS']
        log_file = app.config['LOG_FILE']
        #email logger
        mail_handler = SMTPHandler(log_smtp_srv, log_eml_sender,
            log_eml_admins,'YourApplication Failed')
        mail_handler.setLevel(logging.ERROR)
        mail_handler.setFormatter(Formatter('''
        Message type:       %(levelname)s
        Location:           %(pathname)s:%(lineno)d
        Module:             %(module)s
        Function:           %(funcName)s
        Time:               %(asctime)s
        
        Message:
        
        %(message)s
        '''))
        #file logger
        file_handler = FileHandler(log_file)
        file_handler.setLevel(logging.ERROR)
        file_handler.setFormatter(Formatter(
            '%(asctime)s %(levelname)s: %(message)s '
            '[in %(pathname)s:%(lineno)d]'
        ))
        app.logger.addHandler(mail_handler)
        app.logger.addHandler(file_handler)

