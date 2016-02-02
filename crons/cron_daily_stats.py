# coding: utf-8

import sys
import datetime

sys.path.append('..')
from flaskapp import app, mail, db
from flask_mail import Message


day = datetime.datetime.now() - datetime.timedelta(days=1)
body = "Messages Stats For %s <br><br>" % day.strftime("%Y-%m-%d")

body += """
<table>
    <tr>
        <td>Status</td>
        <td>Total</td>
    </tr>
"""

cursor = db.engine.execute("""
    select count(1) AS total, status
    from SMS__status
    where DATE(send_date)= CURDATE() - INTERVAL 1 DAY
    GROUP BY status
""")
try:
    for item in cursor.fetchall():
        body += """
        <tr>
            <td>%s</td>
            <td>%s</td>
        </tr>
        """ % (item["status"], item["total"])
except Exception, e:
    print "ERROR: %s " % e.message

body += "</table> <br><br><br>"

with app.app_context():
    msg = Message("Messages Stats For %s <br><br>" % day.strftime("%Y-%m-%d"),
                  ['rrguardo83@gmail.com'],
                  html=body, body=body)
    mail.send(msg)
