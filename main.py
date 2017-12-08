# !/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on 8 15 2017

@author: jpl4job@126.com

"""
from sklearn.externals import joblib
from Process import train_FT1, test_FT1
import Process.process_raw_data as process
from Update import download_Tree as DNtree

tree_name = DNtree.tree_name
tree_id_dict = DNtree.Download()
tree_id_dict = tree_id_dict.get_tree_ids()
save_tree = {'高中生物': '9', '初中化学': '164', '高中化学':'6', '初中物理':'114', '高中物理':'4', '高中数学': '199', '初中数学': '209'}

def train_main(init, lab, tree, item='item_content'):
    if init == True:
        down = DNtree.Download()  # 更新增量模型
        down.update_all()
        init = process.init()
        init.run()
    raw_df = joblib.load('Data1/raw_df_filter.pkl')
    model = train_FT1.Model()
    if tree == 'all':
        model.train_and_save_model(raw_df, item, lab, tree)
        test_FT1.test_by_tree(raw_df, item, lab, tree)
    else:
        for name in tree_name:
            tree = tree_id_dict[name]
            model.train_and_save_model(raw_df, item, lab, tree, save_tree[name])
            test_FT1.test_by_tree(raw_df, item, lab, tree, save_tree[name])
    print('训练完成!')
#from clear_tmp import file_name
#file_name('/tmp')  # 清空tmp里面的临时文件
#train_main(False, 'teach_item_type', None)
#train_main(False, 'tree_id', 'all')  # 每天第一次运行时True,更新数据
#train_main(False, 'pid4', None)
#train_main(False, 'difficulty', None)

