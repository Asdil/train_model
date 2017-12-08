#!/usr/bin/env python2
# -*- coding: utf-8 -*-
from conf.config import Config
from sklearn.externals import joblib
import pandas as pd
import os
import datetime
import sys
sys.path.append("..")
from log.loggerfactory import logger


bus_tree = [16]

class Download():
    def __init__(self):
        self.__sql1 = """
select *
from
(
select subject,t1.class,t1.tree_id,pid1,pid2,pid3,pid4,t1.name1,t1.name2,t1.name3,t1.name4,
	t2.item_id,item_content,answer,hint,remark,question_options,options,answers,teach_item_type,difficulty,grade
from
(select tree.class,tree.subject,tree.name,tree.tree_id,
    t1.name as name1,t2.name as name2,t3.name name3,t4.name as name4,
    t1.point_id as pid1,t2.point_id as pid2,t3.point_id as pid3,t4.point_id as pid4
    from knowledge_point_tree as t1 join knowledge_point_tree as t2
    on t1.level = 1 and t2.level=2 and t2.pid = t1.point_id and t1.tree_id = t2.tree_id
    join knowledge_point_tree as t3
    on t2.level = 2 and t3.level=3 and t3.pid = t2.point_id and t2.tree_id = t3.tree_id
    join knowledge_point_tree as t4
    on t3.level = 3 and t4.level=4 and t4.pid = t3.point_id and t4.tree_id = t3.tree_id
    join knowledge_tree as tree on tree.tree_id = t1.tree_id and tree.class=1) as t1 join
(select t1.point_id,t1.item_id,item_content,answer,hint,remark,question_options,options,answers,
teach_item_type,difficulty,grade
    from item_point as t1 join item as t2 on t1.item_id = t2.item_id
    where t2.state=0 and t2.in_source=2 and t1.last_update_time > '{1}' and t1.last_update_time < '{2}') as t2 on t1.pid4 = t2.point_id

union all


select subject,class,tree_id,pid1,pid2,pid3,pid4,name1,name2,name3,name4,
	item_id,item_content,answer,hint,remark,question_options,options,answers,teach_item_type,difficulty,grade
from
(select tree.class,tree.subject,tree.name,tree.tree_id,
    t1.name as name1,t2.name as name2,t3.name name3,t4.name as name4,
    t1.point_id as pid1,t2.point_id as pid2,t3.point_id as pid3,t4.point_id as pid4
    from knowledge_point_tree as t1 join knowledge_point_tree as t2
    on t1.level = 1 and t2.level=2 and t2.pid = t1.point_id and t1.tree_id = t2.tree_id
    join knowledge_point_tree as t3
    on t2.level = 2 and t3.level=3 and t3.pid = t2.point_id and t2.tree_id = t3.tree_id
    join knowledge_point_tree as t4
    on t3.level = 3 and t4.level=4 and t4.pid = t3.point_id and t4.tree_id = t3.tree_id
    join knowledge_tree as tree on tree.tree_id = t1.tree_id and tree.class=2) as t1 join
knowledge_point_relation as points_relation on t1.pid4 = points_relation.point_id join
(select t1.point_id,t1.item_id,item_content,answer,hint,remark,question_options,options,answers,
teach_item_type,difficulty,grade
    from item_point as t1 join item as t2 on t1.item_id = t2.item_id
    where t2.state=0 and t2.in_source=2 and t1.last_update_time > '{1}' and t1.last_update_time < '{2}') as t2 on points_relation.base_point_id = t2.point_id
) t
where tree_id = {0}

"""

        self.__sql2 ='''
select subject,tree_id,pid1,pid2,pid3,pid4,name1,name2,name3,name4,
	t2.item_id,item_content,answer,hint,remark,question_options,options,answers,teach_item_type,difficulty,grade
from
(select tree.subject,tree.name,tree.tree_id,
    t1.name as name1,t2.name as name2,t3.name name3,t4.name as name4,
    t1.point_id as pid1,t2.point_id as pid2,t3.point_id as pid3,t4.point_id as pid4
    from knowledge_point_tree as t1 join knowledge_point_tree as t2
    on t1.level = 1 and t2.level=2 and t2.pid = t1.point_id and t1.tree_id = t2.tree_id
    join knowledge_point_tree as t3
    on t2.level = 2 and t3.level=3 and t3.pid = t2.point_id and t2.tree_id = t3.tree_id
    join knowledge_point_tree as t4
    on t3.level = 3 and t4.level=4 and t4.pid = t3.point_id and t4.tree_id = t3.tree_id
    join knowledge_tree as tree on tree.tree_id = t1.tree_id) as t1 join
(select t1.point_id,t1.item_id,item_content,answer,hint,remark,question_options,options,answers,
teach_item_type,difficulty,grade
    from item_point as t1 join item as t2 on t1.item_id = t2.item_id
    where t2.state=0 and t2.in_source=2 and t1.last_update_time > '{1}' and t1.last_update_time < '{2}') as t2 on t1.pid4 = t2.point_id
where tree_id = {0}
'''

        self.__sql3 = """
select *
from
(
select subject,t1.class,t1.tree_id,pid1,pid2,pid3,pid4,t1.name1,t1.name2,t1.name3,t1.name4,
	t2.item_id,item_content,answer,hint,remark,question_options,options,answers,teach_item_type,difficulty,grade
from
(select tree.class,tree.subject,tree.name,tree.tree_id,
    t1.name as name1,t2.name as name2,t3.name name3,t4.name as name4,
    t1.point_id as pid1,t2.point_id as pid2,t3.point_id as pid3,t4.point_id as pid4
    from knowledge_point_tree as t1 join knowledge_point_tree as t2
    on t1.level = 1 and t2.level=2 and t2.pid = t1.point_id and t1.tree_id = t2.tree_id
    join knowledge_point_tree as t3
    on t2.level = 2 and t3.level=3 and t3.pid = t2.point_id and t2.tree_id = t3.tree_id
    join knowledge_point_tree as t4
    on t3.level = 3 and t4.level=4 and t4.pid = t3.point_id and t4.tree_id = t3.tree_id
    join knowledge_tree as tree on tree.tree_id = t1.tree_id and tree.class=1) as t1 join
(select t1.point_id,t1.item_id,item_content,answer,hint,remark,question_options,options,answers,
teach_item_type,difficulty,grade
    from item_point as t1 join item as t2 on t1.item_id = t2.item_id
    where t2.state=0 and t2.in_source=2 and t1.last_update_time < '{1}') as t2 on t1.pid4 = t2.point_id

union all


select subject,class,tree_id,pid1,pid2,pid3,pid4,name1,name2,name3,name4,
	item_id,item_content,answer,hint,remark,question_options,options,answers,teach_item_type,difficulty,grade
from
(select tree.class,tree.subject,tree.name,tree.tree_id,
    t1.name as name1,t2.name as name2,t3.name name3,t4.name as name4,
    t1.point_id as pid1,t2.point_id as pid2,t3.point_id as pid3,t4.point_id as pid4
    from knowledge_point_tree as t1 join knowledge_point_tree as t2
    on t1.level = 1 and t2.level=2 and t2.pid = t1.point_id and t1.tree_id = t2.tree_id
    join knowledge_point_tree as t3
    on t2.level = 2 and t3.level=3 and t3.pid = t2.point_id and t2.tree_id = t3.tree_id
    join knowledge_point_tree as t4
    on t3.level = 3 and t4.level=4 and t4.pid = t3.point_id and t4.tree_id = t3.tree_id
    join knowledge_tree as tree on tree.tree_id = t1.tree_id and tree.class=2) as t1 join
knowledge_point_relation as points_relation on t1.pid4 = points_relation.point_id join
(select t1.point_id,t1.item_id,item_content,answer,hint,remark,question_options,options,answers,
teach_item_type,difficulty,grade
    from item_point as t1 join item as t2 on t1.item_id = t2.item_id
    where t2.state=0 and t2.in_source=2 and t1.last_update_time < '{1}') as t2 on points_relation.base_point_id = t2.point_id
) t
where tree_id = {0}

"""

        self.__sql4 ='''
select subject,tree_id,pid1,pid2,pid3,pid4,name1,name2,name3,name4,
	t2.item_id,item_content,answer,hint,remark,question_options,options,answers,teach_item_type,difficulty,grade
from
(select tree.subject,tree.name,tree.tree_id,
    t1.name as name1,t2.name as name2,t3.name name3,t4.name as name4,
    t1.point_id as pid1,t2.point_id as pid2,t3.point_id as pid3,t4.point_id as pid4
    from knowledge_point_tree as t1 join knowledge_point_tree as t2
    on t1.level = 1 and t2.level=2 and t2.pid = t1.point_id and t1.tree_id = t2.tree_id
    join knowledge_point_tree as t3
    on t2.level = 2 and t3.level=3 and t3.pid = t2.point_id and t2.tree_id = t3.tree_id
    join knowledge_point_tree as t4
    on t3.level = 3 and t4.level=4 and t4.pid = t3.point_id and t4.tree_id = t3.tree_id
    join knowledge_tree as tree on tree.tree_id = t1.tree_id) as t1 join
(select t1.point_id,t1.item_id,item_content,answer,hint,remark,question_options,options,answers,
teach_item_type,difficulty,grade
    from item_point as t1 join item as t2 on t1.item_id = t2.item_id
    where t2.state=0 and t2.in_source=2 and t1.last_update_time < '{1}') as t2 on t1.pid4 = t2.point_id
where tree_id = {0}
'''

        self.__con = Config()
        self.__conn = self.__con.get_matrix_slave_con()
        self.pwd = os.path.dirname(__file__)
        self.father_path = os.path.abspath(os.path.dirname(self.pwd)+os.path.sep+".")

    def to_yester_day(self):
        today = datetime.datetime.now()
        yesterday = today-datetime.timedelta(days=1)
        today = today.strftime('%Y-%m-%d')
        yesterday = yesterday.strftime('%Y-%m-%d')
        return today, yesterday

    def init_data(self, tree_id):
        today, yesterday = self.to_yester_day()
        if tree_id in bus_tree:
            sql = self.__sql3.format(str(tree_id), today)
            df = pd.read_sql(sql, self.__conn)
        else:
            sql = self.__sql4.format(str(tree_id), today)
            df = pd.read_sql(sql, self.__conn)
        # df = df[['tree_id', 'teach_item_type', 'pid4', 'item_content', 'difficulty']]
        joblib.dump(df, self.father_path+'/Data1/' + str(tree_id) + 'raw_df.pkl')
        # df.to_excel(self.father_path+'/Data1/' + str(tree_id) + 'raw_df.xlsx')

    def update_data(self, tree_id):
        today, yesterday = self.to_yester_day()
        if tree_id in bus_tree:
            sql = self.__sql1.format(str(tree_id), yesterday, today)
            df = pd.read_sql(sql, self.__conn)
        else:
            sql = self.__sql2.format(str(tree_id), yesterday, today)
            df = pd.read_sql(sql, self.__conn)
        joblib.dump(df, self.father_path+'/Data1/' + str(tree_id) + 'add_df.pkl')
        # df.to_excel(self.father_path+'/Data1/' + str(tree_id) + 'add_df.xlsx')

    def update_all(self):
        #  高中生物9, 高中化学6, 高中物理4, 高中数学199, 初中化学164, 初中物理114, 初中数学209
        tree_ids = [9, 6, 4, 199, 164, 114, 209]
        logger.info('开始更新数据')
        for tree_id in tree_ids:  # 获取增量
            self.update_data(tree_id)
        df = joblib.load(self.father_path+'/Data1/' + str(tree_ids[0]) + 'add_df.pkl')  # 读取一棵树的更新
        logger.info(str(tree_ids[0])+'更新:'+str(len(df))+'条')
        for tree_id in tree_ids[1:]:  # 更新每棵树
            _df = joblib.load(self.father_path+'/Data1/' + str(tree_id) + 'add_df.pkl')
            logger.info(str(tree_id)+'更新:'+str(len(_df))+'条')
            frames = [df, _df]
            df = pd.concat(frames)
        joblib.dump(df, self.father_path+'/Data1/add_df.pkl')  # 所有更新的文件
        # df.to_excel(self.father_path+'/Data1/add_df.xlsx')


    def init_all(self):
        logger.info('开始下载所有数据')
        #  高中生物9, 高中化学6, 高中物理4, 高中数学199, 初中化学164, 初中物理114, 初中数学209
        tree_ids = [9, 6, 4, 199, 164, 114, 209]
        for tree_id in tree_ids:  # 获取增量
            self.init_data(tree_id)
        df = joblib.load(self.father_path+'/Data1/' + str(tree_ids[0]) + 'raw_df.pkl')  # 读取一棵树的更新
        logger.info(str(tree_ids[0])+'一共:'+str(len(df))+'条')
        for tree_id in tree_ids[1:]:  # 更新每棵树
            _df = joblib.load(self.father_path+'/Data1/' + str(tree_id) + 'raw_df.pkl')
            logger.info(str(tree_id)+'一共:'+str(len(_df))+'条')
            frames = [df, _df]
            df = pd.concat(frames)
        joblib.dump(df, self.father_path+'/Data1/raw_df.pkl')  # 所有更新的文件
        # df.to_excel(self.father_path+'/Data1/raw_df.xlsx')






