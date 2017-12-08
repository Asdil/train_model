#!/usr/bin/env python2
# -*- coding: utf-8 -*-

def wash_answer(answer):
    answer = answer.strip()  # 去除两边空格
    answer = answer.replace('.', '')  # 去除.
    answer = answer.replace(' ', '')  # 去除空格
    return str(answer)