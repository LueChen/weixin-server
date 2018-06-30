# -*- coding: utf-8 -*-
# filename: main.py
import web
from handle import Handle
from handle import Phone
import basic

urls = (
    '/wx', 'Handle',
    '/phone', 'Phone'
)

if __name__ == '__main__':
#    basic.Basic().run()

    app = web.application(urls, globals())
    print "fucking start: "
    app.run()
