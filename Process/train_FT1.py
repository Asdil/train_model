#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on 8 15 2017

@author: jpl4job@126.com

"""
import sys
sys.path.append("..")
import os
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import accuracy_score, make_scorer
from sklearn.model_selection import train_test_split
from sklearn.externals import joblib
from shallowlearn.models import FastText
from Base.conf import Config
# from Model1 import publisher
from log.loggerfactory import logger
# from log.hash import get_md5_02
# import time



class Model(object):
    def __init__(self):
        self.pwd = os.path.dirname(__file__)
        self.father_path = os.path.abspath(os.path.dirname(self.pwd)+os.path.sep+".")
        self.data_dirs = self.father_path + '/Data1/'
        self.model_dirs = self.father_path + '/Model1/'
        self.stop_words = Config.get_stop_words()
        self.grid = None

    # 建立模型
    def build_model(self):
        #  注意看这里有tfidf!!!
        estimator = FastText(dim=100)  # , pretrained_vectors=self.model_dirs+'skipgram.vec'
        param_grid = {
            'lr': (0.7, 0.8, 1),
            #'lr': (0.7, 0.8, 1, 2),
            #'loss': ('ns', 'hs', 'softmax'),
            # 'min_count': (0, 1, 3, 5),
            #'ws': (4, 5, 6),
            # 'dim': (100, 200, 300)
        }

        grid = GridSearchCV(estimator=estimator, param_grid=param_grid,
                            cv=2, scoring=make_scorer(accuracy_score), n_jobs=4, verbose=0)
        self.grid = grid


    def train_and_save_model(self, raw_df, item, lab, tree_id=None, name=None):
        self.build_model()

        logger.info('开始训练')
        if tree_id == 'all':
            tmp_raw_df = raw_df[raw_df[item] != '']  # 去除为空的
            #tmp_raw_df = tmp_raw_df[item].astype(int)
            lab = 'tree_id'
            del raw_df

            train_df, test_df = train_test_split(tmp_raw_df, train_size=0.8, random_state=42)

            # joblib.dump(train_df, self.data_dirs+str(tree_id)+'_FTtrain1.pkl')
            # 如果文件存在,则不存储

            joblib.dump(test_df, self.data_dirs+str(tree_id)+'_FTtest1.pkl')

            # train_df = joblib.load(self.data_dirs+str(tree_id)+'_FTtrain1.pkl')
            self.grid.fit(train_df[item], train_df[lab])

            # 将模型集保存到Model文件夹中
            logger.info('树'+str(tree_id)+'最好的模型参数为:'+ str(self.grid.best_params_))
            # print(self.grid.best_estimator_.predict([['tall', 'am', 'i']]))
            self.grid.best_estimator_.save('Model1/'+str(tree_id)+lab+'.model')

        else:

            if tree_id != None:
                tree_ids = tree_id
            for tree_id in tree_ids:
                if lab == 'pid4':
                    print tree_id + '=============================='
                    tmp_raw_df = raw_df[raw_df[u'tree_id'] == tree_id]
                    tmp_raw_df = tmp_raw_df[tmp_raw_df[item] != '']  # 去除为空的
                else:
                    print name + '=============================='
                    tmp_raw_df = raw_df[raw_df['tree_id'].isin(tree_ids)]
                    tmp_raw_df = tmp_raw_df[tmp_raw_df[item] != '']  # 去除为空的

                if len(tmp_raw_df) == 0:
                    continue
                train_df, test_df = train_test_split(tmp_raw_df, train_size=0.8, random_state=42)


                # 如果是题型判断, 不要选择题, 填空题, 判断题
                if lab == 'teach_item_type':
                    print(len(train_df))
                    train_df = train_df[train_df[lab] != '1']
                    train_df = train_df[train_df[lab] != '7']
                    train_df = train_df[train_df[lab] != '9']
                    print(len(train_df))

                # joblib.dump(train_df, self.data_dirs+str(tree_id)+'_FTtrain1.pkl')
                # 如果文件存在,则不存储


                # print(self.grid.best_estimator_.predict([['tall', 'am', 'i']]))
                if lab != 'pid4':
                    joblib.dump(test_df, self.data_dirs+str(name)+'_FTtest1.pkl')
                    self.grid.fit(train_df[item], train_df[lab])
                    logger.info('树'+str(name)+'最好的模型参数为:'+ str(self.grid.best_params_))
                    self.grid.best_estimator_.save('Model1/'+str(name)+lab+'.model')
                else:
                    
                    joblib.dump(test_df, self.data_dirs+str(tree_id)+'_FTtest1.pkl')
                    print(len(train_df))
                    self.grid.fit(train_df[item], train_df[lab])
                    logger.info('树'+str(tree_id)+'最好的模型参数为:'+ str(self.grid.best_params_))
                    self.grid.best_estimator_.save('Model1/'+str(tree_id)+lab+'.model')


                if lab != 'pid4':
                    break


                # 第一种方法
                # message.send(str(tree_id)+lab)
