#!/usr/bin/env python2
# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf8')
sys.path.append('..')
from sklearn.externals import joblib
import pandas as pd
from Base.clear_data import filter_latex_html
import Base.processes as processes


# 将每一列转换一遍
def change_type(doc_df, items):
    for item in items:
        doc_df[item] = doc_df[item].astype(str)
    return doc_df

class init:
    def run(self, firtst = False, doc_df=None, piece=None):
        print('开始载入数据')
        if firtst == False:
            doc_df = joblib.load('Data1/add_df.pkl')
        doc_df = doc_df.fillna('')  # 将nan填充',先填充在转程str格式'
        items = ['item_content', 'answer']
        doc_df = change_type(doc_df, items)

        #  选择需要的列
        # items = ['tree_id', 'item_content', 'answer', 'hint', 'remark', 'question_options', 'teach_item_type', 'difficulty', 'pid2']
        # doc_df = doc_df.loc[:, items]

        print('数据载入完毕')

        # 过滤question_options这一列
        #doc_df.loc[:, u"options"] = pd.Series(index=doc_df.index, data=doc_df.question_options.apply(processes.extract_question_options))

        # 将其他列合并成新的stem列
        #doc_df.loc[:, u"stem"] = doc_df.item_content+doc_df.answer+doc_df.hint+doc_df.remark+doc_df.options

        #doc_df.loc[:, u'stem_chinese'] = pd.Series(index=doc_df.index,data=doc_df.stem.apply(filter_latex_html))

        doc_df.loc[:, u'item_content'] = pd.Series(index=doc_df.index,
                                             data=doc_df.item_content.apply(filter_latex_html))


        doc_df.loc[:, u'answer'] = pd.Series(index=doc_df.index,
                                             data=doc_df.answer.apply(filter_latex_html))

        # # 使用jieba分词,将stem_chinese列分开,每个词同/t区分
        #doc_df.loc[:, u'stem_seg'] = pd.Series(index=doc_df.index,data=doc_df.stem_chinese.apply(processes.segment_sentence))


        doc_df.loc[:, u'item_content'] = pd.Series(index=doc_df.index,data=doc_df.item_content.apply(processes.segment_sentence))

        doc_df.loc[:, u'tree_id'] = pd.Series(index=doc_df.index,data=doc_df.tree_id.apply(lambda x: str(x)))

        doc_df.loc[:, u'teach_item_type'] = pd.Series(index=doc_df.index,data=doc_df.teach_item_type.apply(lambda x: str(x)))

        doc_df.loc[:, u'pid4'] = pd.Series(index=doc_df.index,data=doc_df.pid4.apply(lambda x: str(x)))

        doc_df.loc[:, u'difficulty'] = pd.Series(index=doc_df.index,data=doc_df.difficulty.apply(lambda x: str(x)))

        # # 取['tree_id', 'pid2', 'stem_seg']这三列作为训练样本

        raw_data = doc_df[['tree_id', 'teach_item_type', 'pid1', 'pid2', 'pid3', 'pid4', 'item_content', 'answer', 'difficulty']]

        # 保存
        if firtst:
            joblib.dump(raw_data, 'Data1/raw_df' + piece + '.pkl')
            # raw_data.to_excel('Data1/raw_df.xlsx')
            print '第' + piece + '段跑完'
        else:
            df = joblib.load('Data1/raw_df_filter.pkl')
            frames = [raw_data, df]
            df = pd.concat(frames)
            joblib.dump(df, 'Data1/raw_df_filter.pkl')

    def join_piece(self, pieces):
        df = joblib.load('Data1/raw_df' + '1' + '.pkl')
        for i in range(2, pieces+1):
            _df = joblib.load('Data1/raw_df' + str(i) + '.pkl')
            frames = [df, _df]
            df = pd.concat(frames)
        joblib.dump(df, 'Data1/raw_df_filter.pkl')



# def run(firtst = False, doc_df=None, piece=None):
#     print('开始载入数据')
#     if firtst == False:
#         doc_df = joblib.load('Data1/add_df.pkl')
#     doc_df = doc_df.fillna('')  # 将nan填充',先填充在转程str格式'
#     items = ['item_content', 'answer']
#     doc_df = change_type(doc_df, items)
#
#         #  选择需要的列
#         # items = ['tree_id', 'item_content', 'answer', 'hint', 'remark', 'question_options', 'teach_item_type', 'difficulty', 'pid2']
#         # doc_df = doc_df.loc[:, items]
#
#     print('数据载入完毕')
#
#         # 过滤question_options这一列
#         #doc_df.loc[:, u"options"] = pd.Series(index=doc_df.index, data=doc_df.question_options.apply(processes.extract_question_options))
#
#         # 将其他列合并成新的stem列
#         #doc_df.loc[:, u"stem"] = doc_df.item_content+doc_df.answer+doc_df.hint+doc_df.remark+doc_df.options
#
#         #doc_df.loc[:, u'stem_chinese'] = pd.Series(index=doc_df.index,data=doc_df.stem.apply(filter_latex_html))
#
#     doc_df.loc[:, u'item_content'] = pd.Series(index=doc_df.index,
#                                              data=doc_df.item_content.apply(filter_latex_html))
#
#     print 'step1'
#     doc_df.loc[:, u'answer'] = pd.Series(index=doc_df.index,
#                                              data=doc_df.answer.apply(filter_latex_html))
#
#         # # 使用jieba分词,将stem_chinese列分开,每个词同/t区分
#         #doc_df.loc[:, u'stem_seg'] = pd.Series(index=doc_df.index,data=doc_df.stem_chinese.apply(processes.segment_sentence))
#
#     print 'step2'
#     doc_df.loc[:, u'item_content'] = pd.Series(index=doc_df.index,data=doc_df.item_content.apply(processes.segment_sentence))
#     print 'step3'
#     doc_df.loc[:, u'tree_id'] = pd.Series(index=doc_df.index,data=doc_df.tree_id.apply(lambda x: str(x)))
#     print 'step4'
#     doc_df.loc[:, u'teach_item_type'] = pd.Series(index=doc_df.index,data=doc_df.teach_item_type.apply(lambda x: str(x)))
#     print 'step5'
#     doc_df.loc[:, u'pid4'] = pd.Series(index=doc_df.index,data=doc_df.pid4.apply(lambda x: str(x)))
#     print 'step6'
#     doc_df.loc[:, u'difficulty'] = pd.Series(index=doc_df.index,data=doc_df.difficulty.apply(lambda x: str(x)))
#     print 'step7'
#         # # 取['tree_id', 'pid2', 'stem_seg']这三列作为训练样本
#
#     raw_data = doc_df[['tree_id', 'teach_item_type', 'pid1', 'pid2', 'pid3', 'pid4', 'item_content', 'answer', 'difficulty']]
#
#         # 保存
#     if firtst:
#         joblib.dump(raw_data, 'Data1/raw_df' + piece + '.pkl')
#             # raw_data.to_excel('Data1/raw_df.xlsx')
#         print '第' + piece + '段跑完'
#     else:
#         df = joblib.load('Data1/raw_df.pkl')
#         frames = [raw_data, df]
#         df = pd.concat(frames)
#         joblib.dump(df, 'Data1/raw_df.pkl')
#
# def join_piece(pieces):
#     df = joblib.load('Data1/raw_df' + 1 + '.pkl')
#     for i in range(2, pieces+1):
#         _df = joblib.load('Data1/raw_df' + i + '.pkl')
#         frames = [df, _df]
#         df = pd.concat(frames)
#     joblib.dump(df, 'Data1/raw_df.pkl')
