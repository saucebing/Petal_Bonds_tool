#!/usr/bin/python3
# -*- coding: UTF-8 -*-
f = open('Cards.md', 'r', encoding="utf-8")
lines = f.readlines()
for line in lines:
    line = line.strip()
    if line == "":
        continue
    else:
        line_list = line.split('|')
        number = line_list[1].strip()
        name_zh = line_list[2].strip()
        name_en = line_list[3].strip()
        if number.strip() == '编号':
            continue
        elif name_zh.strip() == ':----':
            continue
        else:
            print('"%s",%s,"%s","%s"' % (name_en, number, name_zh, name_en))
