#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on 8 15 2017

@author: jpl4job@126.com

"""
import os
pwd = os.path.dirname(__file__)
father_path = os.path.abspath(os.path.dirname(pwd)+os.path.sep+".")
import sys
sys.path.append("..")
from trainFT.log.loggerfactory import logger
from sklearn.metrics import accuracy_score
from sklearn.externals import joblib
from train_FT1 import Model
from shallowlearn.models import FastText
import princeple2 as pri
import numpy as np
# import Base.conf as conf
import pandas as pd
import time
from Model1 import publisher
from log.hash import get_md5_02
# from item_content_KNN5 import knn5


def recovery(df, attri):
    df[attri] = pd.Series(index=df.index,
                          data=df[attri].apply(lambda x: ' '.join(x)))
    return df

def test_by_tree(raw_df, item, lab,tree_id = None, name=None):
    model = Model()
    logger.info('开始测试')
    if tree_id == 'all':
        # 读取测试集,并测试
        test_df = joblib.load(model.data_dirs+str(tree_id)+'_FTtest1.pkl')

        FTmodel1 = FastText.load('Model1/'+str(tree_id)+lab+'.model')


        y_predit = []
        # y_pro = []
        for i in range(len(test_df[lab])):
            predit1 = FTmodel1.predict([test_df[item].iloc[i]])
            y_predit.extend(predit1)
            # predit3 = FTmodel1._classifier.predict_proba(iter(' '.join(d) for d in [test_df[item].iloc[i]]), FTmodel1._label_count)
            # y_pro.append(predit3[0])

        # y_predit = FTmodel1.predict_proba(test_df.stem_seg)
        acc = accuracy_score(test_df[lab], y_predit)*100
        logger.info('标签为'+str(tree_id)+'的正确率为:'+str(acc))

        # 发送模型
        information =str(tree_id) + '|' + lab + '|' + str(acc) + '%' + '|' + str(get_md5_02(father_path+'/Model1/'+str(tree_id)+lab+'.model'+'.CLF.bin'))
        publisher.send_model('Model1/'+str(tree_id)+lab+'.model'+'.CLF.bin')
        logger.info('发送'+str(tree_id)+lab+'.model'+'.CLF.bin'+' md5码: '+get_md5_02(father_path+'/Model1/'+str(tree_id)+lab+'.model'+'.CLF.bin'))
        time.sleep(20)
        publisher.send_model('Model1/'+str(tree_id)+lab+'.model', information)
        logger.info('发送'+str(tree_id)+lab+'.model')
        #time.sleep(20)
    else:
        if tree_id != None:
            tree_ids = tree_id
        for tree_id in tree_ids:
            if lab != 'pid4':
                tree_id = name
            # 读取测试集,并测试
            try:
                test_df = joblib.load(model.data_dirs+str(tree_id)+'_FTtest1.pkl')
                FTmodel1 = FastText.load('Model1/'+str(tree_id)+lab+'.model')
            except:
                continue

            y_predit = []
            # y_pro = []
            for i in range(len(test_df[lab])):
                predit1 = pri.my_principle(test_df.iloc[i], lab)
                if predit1 == True:
                    predit1 = FTmodel1.predict([test_df[item].iloc[i]])

                y_predit.extend(predit1)
            # 测试时knn
            # if lab == 'pid4':
            #     pid4_knn = []
            #     for i in range(len(test_df[item])):
            #         pid4_knn.append(knn5(5, str(test_df[item].iloc[i]).replace(' ', '')))

                # predit3 = FTmodel1._classifier.predict_proba(iter(' '.join(d) for d in [test_df[item].iloc[i]]), FTmodel1._label_count)
                # y_pro.append(predit3[0])

                # y_predit = FTmodel1.predict_proba(test_df.stem_seg)
            # if lab == 'pid4':
            #     pid4_knn_acc = accuracy_score(test_df[lab].values.astype(str), pid4_knn)*100
            acc = accuracy_score(test_df[lab].values.astype(str), y_predit)*100


            # 发送模型

            logger.info('标签为'+str(tree_id)+'的正确率为:'+str(acc))
            information = str(tree_id) + '|' + lab + '|' + str(acc) + '%' + '|' + str(get_md5_02(father_path+'/Model1/'+str(tree_id)+lab+'.model'+'.CLF.bin'))
            publisher.send_model('Model1/'+str(tree_id)+lab+'.model'+'.CLF.bin', information)
            logger.info('发送'+str(tree_id)+lab+'.model'+'.CLF.bin'+' md5码: '+get_md5_02(father_path+'/Model1/'+str(tree_id)+lab+'.model'+'.CLF.bin'))
            time.sleep(20)
            publisher.send_model('Model1/'+str(tree_id)+lab+'.model', information)
            logger.info('发送'+str(tree_id)+lab+'.model')
            #time.sleep(20)

            try:
                # 将错题保存到excel
                df1 = pd.DataFrame()
                # df2 = pd.DataFrame()
                y_predit = np.array(y_predit)
                # 分类错误的Dataframe
                x_worng = test_df[y_predit != test_df[lab]]
                df1[u'tree_id'] = x_worng.tree_id
                df1[lab] = x_worng[lab]
                df1[u'pre'] = y_predit[y_predit != test_df[lab]]
                df1[item] = x_worng[item]
                df1[u'answer'] = x_worng[u'answer']
                df1 = recovery(df1, item)

                # # 分类正确的Dataframe
                # x_true = test_df[y_predit == test_df[lab]]
                # df2[u'tree_id'] = x_true.tree_id
                # df2[lab] = x_true[lab]
                # df2[u'pre'] = y_predit[y_predit == test_df[lab]]
                # df2[item] = x_true[item]
                # df2 = recovery(df2, item)


                writer = pd.ExcelWriter(model.father_path +
                                        '/wrong_answer/' + str(tree_id) + lab + '_FTwrong.xlsx') # 保存问excel文件,方便查看

                df1.to_excel(writer, 'Sheet1')
                writer.save()
                writer.close()

                # writer = pd.ExcelWriter(model.father_path +
                #                         '/true_answer/' + str(tree_id) + '_FTtrue.xlsx') # 保存问excel文件,方便查看
                # df2.to_excel(writer, 'Sheet1')
                # writer.save()
                # writer.close()
            except:
                pass
            if lab != 'pid4':
                break
