# !/usr/bin/env python2
# -*- coding: utf-8 -*-
# 清洗数据数据
from replace_latex_format import remove_latex_keyword
from filter_latex_html import preprocess
from addtion_replace import replace_other


def filter_latex_html(words):
    words = str(words)  # 以防万一转换成str格式
    words = remove_latex_keyword(words)  # 过滤公式
    words = preprocess(words)  # 过滤latex和html
    words = replace_other(words)  # 清除一些关键词
    return words