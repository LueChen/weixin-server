# -*- coding: utf-8 -*-
# filename: main.py
import web
from handle import Handle
import basic

urls = (
    '/wx', 'Handle',
)

if __name__ == '__main__':
#    basic.Basic().run()

    app = web.application(urls, globals())
    print "fucking start: "
    app.run()
