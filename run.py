# !/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on 8 15 2017

@author: jpl4job@126.com

"""
from main import train_main
from log.loggerfactory import logger
from clear_tmp import file_name
import schedule
import time
from Base.zip_file import zip_wrong_file
def job():
    train_main(True, 'tree_id', 'all')  # 每天第一次运行时True,更新数据
    train_main(False, 'tree_id', 'all')  # 每天第一次运行时True,更新数据
    file_name('/tmp')  # 清空tmp里面的临时文件
    train_main(True, 'teach_item_type', None)
    train_main(False, 'tree_id', 'all')  # 每天第一次运行时True,更新数据
    train_main(False, 'pid4', None)
    train_main(False, 'difficulty', None)
    file_name('/tmp')  # 清空tmp里面的临时文件
    zip_wrong_file()

schedule.every().day.at("00:20").do(job) # 每天做任务

# 主训练函数
if __name__ == '__main__':
    # lab = pid4, teach_item_type, difficulty
    logger.info('开始')
    #file_name('/tmp')  # 清空tmp里面的临时文件
    while True:
        schedule.run_pending()
        time.sleep(1)

