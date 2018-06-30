# -*- coding: utf-8 -*-
# filename: handle.py

import hashlib
import web

import reply
import receive

global msgs
msgs = {}

class Handle(object):
    def GET(self):
        try:
            data = web.input()
            if len(data) == 0:
                return "hello, this is handle view"
            
            signature = data.signature
            timestamp = data.timestamp
            nonce = data.nonce
            echostr = data.echostr
            token = "fucku" #请按照公众平台官网\基本配置中信息填写

            list = [token, timestamp, nonce]
            list.sort()
            sha1 = hashlib.sha1()
            map(sha1.update, list)
            hashcode = sha1.hexdigest()
            print "handle/GET func: hashcode, signature: ", hashcode, signature
            if hashcode == signature:
                return echostr
            else:
                return ""
        except Exception, Argument:
            print "what a fucking exception!"
            return Argument

    def POST(self):
        try:
            webData = web.data()
            print "Handle Post webdata is ", webData   #后台打日志
            recMsg = receive.parse_xml(webData)
            if isinstance(recMsg, receive.Msg):
                toUser = recMsg.FromUserName
                fromUser = recMsg.ToUserName
                if recMsg.MsgType == 'text':
                    query = recMsg.Content
                    if query in msgs.keys():
                      if msgs[query]:
                        content = msgs[query].pop();
                      else:
                        content = 'there is no msg for ' + query
                    else:
                      content = 'there is no msg for ' + query

                    replyMsg = reply.TextMsg(toUser, fromUser, content)
                    return replyMsg.send()
                if recMsg.MsgType == 'image':
                    mediaId = recMsg.MediaId
                    replyMsg = reply.ImageMsg(toUser, fromUser, mediaId)
                    return replyMsg.send()
                else:
                    return reply.Msg().send()
            else:
                print "暂且不处理"
                return reply.Msg().send()
        except Exception, Argment:
            return Argment


class Phone(object):
    def GET(self):
        data = web.input()
        if len(data) == 0:
            return "hello, this is phone view"

    def POST(self):
        webData = web.data()
        print "Handle Post webdata is ", webData   #后台打日志
        recMsg = receive.parse_xml(webData)
        if isinstance(recMsg, receive.Msg):
          fromUser = recMsg.ToUserName
          if isinstance(recMsg, receive.TextMsg):
            # 只取末尾的11位作为key值，方便查询手机号
            if not recMsg.FromUserName[-11:] in msgs.keys():
              msgs[recMsg.FromUserName[-11:]] = [recMsg.Content]
            else:
              msgs[recMsg.FromUserName[-11:]].append(recMsg.Content)
              return 'success'

          return 'success'
        else:
          print "暂且不处理"
          return 'success'
