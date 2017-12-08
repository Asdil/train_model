#!/usr/bin/env python2
# -*- coding: utf-8 -*-
#  额外过滤一些公式
import re

def replace_other(html):
    html = html.replace('\\', ' ')
    html = html.replace('(', ' ')
    html = html.replace(')',' ')
    html = html.replace('↵', ' ')
    html = html.replace('cr&', ' & ')
    html = html.replace('f x', ' fx ')
    html = html.replace('g x', ' gx ')
    html = html.replace('logx', ' logx ')
    html = html.replace('mathrm', 'mathrm ')
    html = html.replace('cos', 'cos ')
    html = html.replace('sin', 'sin ')
    html = html.replace('sqrt', 'sqrt ')
    html = html.replace(' mol ', ' ')
    html = html.replace(' L ', ' ')
    # html = html.replace('②', ' ')
    # html = html.replace('①', ' ')
    # html = html.replace('③', ' ')
    # html = html.replace('④', ' ')
    # html = html.replace('⑤', ' ')
    # html = html.replace('⑥', ' ')
    # html = html.replace('⑦', ' ')
    # html = html.replace('⑧', ' ')
    html = html.replace('<', ' ')
    html = html.replace('>', ' ')
    num = re.compile(' [0-9]+ ')
    html = num.sub(' ', html)
    return html
