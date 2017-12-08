#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on 10 19 2017

@author: jpl4job@126.com

"""
import re
import json
import requests
from collections import Counter


def ping(host):
    '''ping 1次指定地址'''
    import subprocess,traceback, platform
    if platform.system()=='Windows':
        cmd = 'ping -n %d %s'%(1,host)
    else:
        cmd = 'ping -c %d %s'%(1,host)
    try:
        p = subprocess.Popen(args=cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        (stdoutput,erroutput) = p.communicate()
        # print stdoutput
    except Exception, e:
        traceback.print_exc()
    if platform.system()=='Windows':
        return stdoutput.find('Received = 1')>=0
    else:
        return stdoutput.find('1 packets received') >= 0 or stdoutput.find('1 received') >= 0
online = ping('10.10.63.68')


def knn5(k, item_content, online = online):
    # 由于返回的可能是书妖的所以要夺取几个, 默认先取20个, 取20个中的k个
    if online:
        url = 'http://10.10.63.68:8080/search/query?task=matrix&' \
          'keywords={0}&limit={1}&withoutData=true'.format(item_content, '20')
    else:
        url = 'http://10.2.1.21:8081/search/query?task=matrix&' \
          'keywords={0}&limit={1}&withoutData=true'.format(item_content, '20')
    result = requests.get(url)

    try:
        result = json.loads(result.content)
        result = result['questions']
        point_ids = []
        for each in result:
            if each.has_key(u'point_ids'):
                point_ids.append(str(each[u'point_ids']).split()[0])
                k -= 1
                if k == 0:
                    break
        point_id = Counter(point_ids).most_common(1)[0][0]
    except:
        item_content = re.findall(u'[\u4e00-\u9fa5]+', item_content.decode('utf8'))
        item_content = ''.join(item_content).encode('utf8')

        if online:
            url = 'http://10.10.63.68:8080/search/query?task=matrix&' \
                  'keywords={0}&limit={1}&withoutData=true'.format(item_content, '20')
        else:
            url = 'http://10.2.1.21:8081/search/query?task=matrix&' \
                  'keywords={0}&limit={1}&withoutData=true'.format(item_content, '20')
        result = requests.get(url)
        result = json.loads(result.content)
        result = result['questions']
        point_ids = []
        for each in result:
            if each.has_key(u'point_ids'):
                point_ids.append(str(each[u'point_ids']).split()[0])
                k -= 1
                if k == 0:
                    break
        if not point_ids:
            point_id = 'None'
        else:
            point_id = Counter(point_ids).most_common(1)[0][0]




    return point_id


