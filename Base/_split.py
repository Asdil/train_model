# !/usr/bin/env python2
# -*- coding: utf-8 -*-
import pandas as pd
def split_words(words):
            # 将文字分开
    words = words.split(' ')
    return words
def _split(df, item):
    df.loc[:, item] = pd.Series(index=df.index,
                                data=df[item].apply(split_words))
    return df