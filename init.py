# !/usr/bin/env python2
# -*- coding: utf-8 -*-
import Process.process_raw_data as process
from Update import download_Tree as DNtree
from sklearn.externals import joblib
import multiprocessing
from log.loggerfactory import logger

#down = DNtree.Download()
#down.init_all()
init = process.init()
#doc_df = joblib.load('Data1/raw_df.pkl')
#total = len(doc_df) #总的数目
#piece = total//8

#init.run(True, doc_df[:piece], str(1))
#logger.info('第一个服务成功')
#init.run(True, doc_df[piece:2*piece], str(2))
#logger.info('第二个服务成功')
#init.run(True, doc_df[2*piece:3*piece], str(3))
#logger.info('第三个服务成功')
#init.run(True, doc_df[3*piece:4*piece], str(4))
#logger.info('第四个服务成功')
#init.run(True, doc_df[4*piece:5*piece], str(5))
#logger.info('第五个服务成功')
#init.run(True, doc_df[5*piece:6*piece], str(6))
#logger.info('第六个服务成功')
#init.run(True, doc_df[6*piece:7*piece], str(7))
#logger.info('第七个服务成功')
#init.run(True, doc_df[7*piece:8*piece], str(8))
#logger.info('第八个服务成功')
#init.run(True, doc_df[8*piece:], str(9))
#logger.info('第九个服务成功')
init.join_piece(9)
logger.info('合并成功')
