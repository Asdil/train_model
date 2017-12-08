#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
 File Name: preprocess.py
 Author: Kerry
 Mail: yuyao90@gmail.com
 Created Time: 2017年2月24日
 Description: 对题库数据进行预处理工作
"""

import re
import HTMLParser
import cgi
import sys
reload(sys)
sys.setdefaultencoding('utf8')
import latex

# 带音标字符。
phoneticSymbol = {
    "ā": "a",
    "á": "a",
    "ǎ": "a",
    "à": "a",
    "ē": "e",
    "é": "e",
    "ě": "e",
    "è": "e",
    "ō": "o",
    "ó": "o",
    "ǒ": "o",
    "ò": "o",
    "ī": "i",
    "í": "i",
    "ǐ": "i",
    "ì": "i",
    "ū": "u",
    "ú": "u",
    "ǔ": "u",
    "ù": "u",
    "ü": "v",
    "ǘ": "v",
    "ǚ": "v",
    "ǜ": "v",
    "ń": "n",
    "ň": "n",
    "": "m"
}


class MyHtmlParser(HTMLParser.HTMLParser):
    def __init__(self):
        self.fed = []
        HTMLParser.HTMLParser.__init__(self)

    def handle_starttag(self, tag, attrs):
        if tag == 'br' or tag == 'p' or tag == 'img' or tag == 'td' or tag == 'label' or tag == 'div' or tag == 'tex':
            self.fed.append(' ')

    def handle_endtag(self, tag):
        if tag == 'br' or tag == 'p' or tag == 'img' or tag == 'td' or tag == 'label' or tag == 'div' or tag == 'tex':
            self.fed.append(' ')

    def handle_entityref(self, ref):
        self.fed.append(self.unescape('&' + ref + ';'))

    def handle_data(self, d):
        d = HTMLParser.HTMLParser().unescape(d)
        self.fed.append(d)

    def get_data(self):
        return ''.join(self.fed)


def _process_latex(m):
    latex_str = m.group(1)
    # 处理转义
    latex_str = latex_str.replace(r"\\", "\\")
    regRight = re.compile(r'\\right}')
    latex_str = regRight.sub(r'\\right\\}', latex_str)
    regBegin = re.compile(r'\\begin{[a-z]+}({[a-z]+})?')
    latex_str = regBegin.sub(r' ', latex_str)
    regEnd = re.compile(r'\\end{[a-z]+}')
    latex_str = regEnd.sub(r' ', latex_str)
    try:
        latex_str = latex.parse(latex_str)
    except Exception as err:
        print str(err)
    # 处理公式里面的大于和小于号
    latex_str = cgi.escape(latex_str)
    return latex_str


def _clean_some_symbols(m):
    latex_str = m.group(0)
    latex_str = re.sub('{|}', '', latex_str)
    return latex_str


def remove_script_style(origin_str):
    reg_script = re.compile(r'<script[^>]*?>.*?</script>', re.IGNORECASE | re.S)
    reg_style = re.compile(r'<style[^>]*?>.*?</style>', re.IGNORECASE | re.S)
    origin_str = reg_script.sub(' ', origin_str)
    target_str = reg_style.sub(' ', origin_str)
    return target_str


def process_latex(origin_str):
    """
    处理latex标签
    """
    reg_latex = re.compile(r'<tex>(.*?)</tex>', re.UNICODE | re.DOTALL)
    target_str = reg_latex.sub(_process_latex, origin_str.encode('utf-8'))
    reg_sin = re.compile(r's{in|si{n|c{os|co{s|c{tan|ct{an|cta{n|c{tg|ct{g|c{ot|co{t|t{an|ta{n|t{g|l{n|l{og|lo{g|l{im|li{m', re.IGNORECASE)
    target_str = reg_sin.sub(_clean_some_symbols, target_str)
    target_str = re.sub(r'\\{|\\}', ' ', target_str)
    target_str = re.sub(r'\^|_|{|}', '', target_str)
    try:
        target_str = '<tex>' + target_str.decode('utf8') + '</tex>'
    except:
        print '[decode error]' + origin_str.encode('utf8')
        target_str = origin_str
    return target_str


def remove_html_labels(origin_str):
    parser = MyHtmlParser()
    parser.feed(origin_str)
    return parser.get_data().strip()


def remove_phonetic_symbol(origin_str):
    pinyinPattern = re.compile('|'.join(phoneticSymbol.keys()))
    target_str = pinyinPattern.sub(lambda x: phoneticSymbol[x.group()], origin_str)
    return target_str


def remove_option_flag(origin_str):
    subEx = re.compile(ur'\b([a-zA-Z])(．|\.)', re.U)
    target_str = subEx.sub(r'\1 ', origin_str)
    return target_str


def remove_symbols(origin_str):
    subSign = re.compile(ur',|，', re.S | re.U)
    target_str = subSign.sub(' ', origin_str)
    target_str = re.sub(ur'\^|_|＿', '', target_str)
    return target_str


def process_synonym(src):
    # src = src.replace(u'α', 'a')
    # src = src.replace(u'β', 'b')
    # src = src.replace(u'ρ', 'p')
    # src = src.replace(u'ω', 'w')
    # src = src.replace(u'γ', 'v')
    # src = src.replace(u'ν', 'v')
    # src = src.replace(u'÷', '+')
    # src = src.replace(u'＋', '+')
    # src = src.replace(u'＝', '=')
    # src = src.replace(u'－', '-')
    # src = src.replace(u'×', 'x')
    # src = src.replace(u'≤', '<')
    # src = src.replace(u'≥', '>')
    # src = src.replace(u'＞', '>')
    # src = src.replace(u'＜', '<')
    return src


def strip_continuous_dashes(origin_src):
    regEx = re.compile(ur'-{3,}', re.U)
    target_src = regEx.sub(' ', origin_src)
    return target_src


def preprocess(origin_str):
    target_str = remove_script_style(origin_str)
    target_str = process_latex(target_str)
    target_str = remove_html_labels(target_str)
    target_str = remove_phonetic_symbol(target_str)
    target_str = remove_option_flag(target_str)
    target_str = remove_symbols(target_str)
    target_str = process_synonym(target_str)
    target_str = strip_continuous_dashes(target_str)
    return target_str
