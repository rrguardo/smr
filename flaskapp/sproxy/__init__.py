# -*- coding: utf-8 -*-


class ProxyInterface:
    """Base proxy class."""

    def send(self, to, msg, src):
        raise NotImplementedError()

    def get_balance(self):
        raise NotImplementedError()
