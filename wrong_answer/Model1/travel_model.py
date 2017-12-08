# !/usr/bin/env python2
# -*- coding: utf-8 -*-
import redis


class RedisHelper:
    def __init__(self):
        self.pool = redis.ConnectionPool(host='127.0.0.1', port=6379)
        self.sending = redis.Redis(connection_pool=self.pool)
        self.receiving = redis.Redis(connection_pool=self.pool)

    def send(self, key):
        f1 = open('Model1/'+ key, 'rb')
        f2 = open('Model1/'+ key+'.CLF.bin', 'rb')
        filedata1 = f1.read()
        filedata2 = f2.read()
        f1.close()
        f2.close()

        self.sending.set(key, value=filedata1)
        self.sending.set(key+'.CLF.bin', value=filedata2)
        print(key, key+'.CLF.bin')

    def receive(self, key):
        value1 = self.receiving.get(key)
        value1 = bytearray(value1)
        f1 = open('Model1/'+key, 'wb')

        f1.write(value1)
        f1.close()
        value1 = self.receiving.get(key+'.CLF.bin')
        f1 = open('Model1/'+key + '.CLF.bin', 'wb')
        f1.write(value1)
        f1.close()
