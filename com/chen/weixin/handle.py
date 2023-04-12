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
            token = "fucku"  # 请按照公众平台官网\基本配置中信息填写

            list = [token, timestamp, nonce]
            list.sort()
            sha1 = hashlib.sha1()
            map(sha1.update, list)
            hashcode = sha1.hexdigest()
            print("handle/GET func: hashcode, signature: ", hashcode, signature)
            if hashcode == signature:
                return echostr
            else:
                return ""
        except Exception as e:
            print("what a fucking exception!")
            return -1

    def POST(self):
        try:
            webData = web.data()
            print("Handle Post webdata is ", webData)  # 后台打日志
            recMsg = receive.parse_xml(webData)
            if isinstance(recMsg, receive.Msg):
                toUser = recMsg.FromUserName
                fromUser = recMsg.ToUserName
                if recMsg.MsgType == 'text':
                    queryUser = recMsg.Content
                    if queryUser in msgs.keys():
                        if msgs[queryUser]:
                            content = msgs[queryUser].pop();
                        else:
                            content = 'there is no msg for ' + queryUser
                    else:
                        content = 'there is no msg for ' + queryUser

                    replyMsg = reply.TextMsg(toUser, fromUser, content)
                    return replyMsg.send()
                if recMsg.MsgType == 'image':
                    mediaId = recMsg.MediaId
                    replyMsg = reply.ImageMsg(toUser, fromUser, mediaId)
                    return replyMsg.send()
                else:
                    return reply.Msg().send()
            else:
                print("暂且不处理")
                return reply.Msg().send()
        except Exception:
            return -2


class Phone(object):
    def GET(self):
        data = web.input()
        if len(data) == 0:
            return "hello, this is phone view"

    def POST(self):
        webData = web.data()
        print("Handle Post webdata is ", webData)  # 后台打日志
        recMsg = receive.parse_xml(webData)
        if isinstance(recMsg, receive.Msg):
            recUser = '99108515'
            if isinstance(recMsg, receive.TextMsg):
                # 当前固定使用99108515作为我的手机代号
                content = '[Msg From ' + recMsg.FromUserName + ']: \n' + recMsg.Content
                if not recUser in msgs.keys():
                    msgs[recUser] = [content]
                else:
                    msgs[recUser].append(content)
                    return 'success'

            return 'success'
        else:
            print("暂且不处理")
            return 'success'
