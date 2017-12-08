#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sat Apr  1 11:15:30 2017

@author: xidong.zhang@wenba100.com
"""
import os
import logging
import logging.handlers
pwd = os.path.dirname(__file__)



class LoggerFactory(object):

    LOG_FILE = pwd+'/runlog'

    @classmethod
    def logger_maker(cls):
        logging.basicConfig(
            filename = cls.LOG_FILE,
            format = '%(asctime)s - %(levelname)s -%(process)d- %(filename)s:%(funcName)s:%(lineno)d - %(message)s',
            level = logging.DEBUG)
        # 2017-03-27 16:19:13,254 - INFO -1144- log.py:<module>:31 - hello info

        logging.handlers.TimedRotatingFileHandler(cls.LOG_FILE, when='W0', backupCount=5)
        logger = logging.getLogger(__name__)
        return logger




logger = LoggerFactory.logger_maker()