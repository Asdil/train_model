#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Mar  9 18:27:23 2017

@author: xidong.zhang@wenba100.com
"""

from sklearn.externals import joblib
import codecs
import ConfigParser
import os
import mysql.connector
import sys
sys.path.append("..")
from log.loggerfactory import logger


class Config(object):
    abs_path = os.path.dirname(__file__)
    matrix_conf_path = abs_path + "/matrix.ini"
    stop_words_path = abs_path + "/stop_words.txt"
    matrix_tree_ids_path = abs_path + "/tree_id.txt"
    
    @classmethod
    def write_tree_ids(cls,tree_ids):
        f = codecs.open(cls.matrix_tree_ids_path,encoding='utf-8',mode='w')
        f.write(tree_ids)

    
    @classmethod
    def get_matrix_slave_con(cls):
        conf = ConfigParser.ConfigParser()
        conf.read(cls.matrix_conf_path)
        mysql_config = dict(conf.items('mysql_slave'))
        try:
            con = mysql.connector.connect(**mysql_config)
            return con
        except mysql.connector.Error as e:
            raise e
        
    @classmethod
    def get_matrix_host(cls):
        conf = ConfigParser.ConfigParser()    
        conf.read(cls.matrix_conf_path)
        matrix_host = conf.get('matrix','host')
        return matrix_host
    @classmethod
    def get_stop_words(cls):
        f = codecs.open(cls.stop_words_path,encoding='utf-8')  
        stop_words = f.readlines()
        return stop_words
    @classmethod
    def get_matrix_tree_ids(cls):
        f = codecs.open(cls.matrix_tree_ids_path,encoding='utf-8')
        tree_ids = f.readlines()
        tree_ids = map(int,map(unicode.strip,tree_ids))
        f.close()
        return tree_ids
    @classmethod
    def get_model(cls):
        tree_ids = Config.get_matrix_tree_ids()
        model = {}
        for tree_id in tree_ids:            
            try:
                model[tree_id] = cls.get_modelByTreeId(tree_id)
            except Exception,e:
                continue
        return model
    
    @classmethod
    def get_modelByTreeId(cls,tree_id):
            model_file_path = cls.abs_path + '/model/{tree_id}'.format(tree_id = tree_id)
            try:
                model = None
                model = joblib.load(model_file_path)
                logger.debug('load tree_id {0} model'.format(tree_id))
                return model                 
            except Exception,e:
                raise e
    

        
        

        
        
        
        
        
        
        
        
