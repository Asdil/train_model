# !/usr/bin/env python2
# -*- coding: utf-8 -*-
import redis

class RedisHelper:
    def __init__(self):
        self.__conn = redis.Redis(host='127.0.0.1', port=6379)
        self.pub = 'message'
        self.name = 'name'
        self.model = 'model'

    def public(self, name, value, information):
        self.__conn.set(self.name, name)  # 上传模型名
        self.__conn.set(self.model, value)  # 上传模型
        self.__conn.publish(self.pub, information)  # 发布上传成功
        return True

    def subscribe(self):
        pub = self.__conn.pubsub()
        pub.subscribe(self.pub)
        pub.parse_response()
        return pub

    def getmodel(self):
        name = self.__conn.get(self.name)
        model = self.__conn.get(self.model)
        # self.__conn.delete(self.name)
        # self.__conn.delete(self.model)
        return name, model
