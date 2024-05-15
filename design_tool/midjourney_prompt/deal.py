#!/usr/bin/python3
# -*- coding: UTF-8 -*-
f = open('card.md', 'r', encoding="utf-8")
lines = f.readlines()
occupation_ind = -1
card_ind = 0
for line in lines:
    line = line.strip()
    if line == "":
        continue
    else:
        line_list = line.split('|')
        name_zh = line_list[1].strip()
        name_en = line_list[2].strip().replace(' ', '_')
        origin_prompt = line_list[-2].strip()
        if name_zh.strip() == '卡牌名称（中文）':
            occupation_ind += 1
            if occupation_ind == 11: #中立牌
                occupation_ind = 90
            card_ind = 0
            print('')
            print('')
            print('')
            print('')
            continue
        elif name_zh.strip() == ':----':
            continue
        else:
            prompt01 = origin_prompt + ' In 2D-anime cute in anime style. Anime style, anime style, cute, super cute, very cute, super cute, super cute, anime style, anime style. anime background, close up, anime aesthetic, anime composition, anime aesthetic, anime composition, anime aesthetic, anime composition, anime aesthetic, anime composition, anime aesthetic, anime composition, anime aesthetic, anime composition, anime aesthetic, anime composition, anime aesthetic, anime composition, anime aesthetic, anime composition, anime aesthetic, anime composition, anime aesthetic, anime composition, anime aesthetic, anime composition --ar 856:830'
            fname01 = '%02d%04d_1_%s.png' % (occupation_ind, card_ind, name_en)
            prompt00 = origin_prompt + ' In 2D-anime cute in anime style. Anime style, anime style, cute, super cute, very cute, super cute, super cute, anime style, anime style. anime background, close up, anime aesthetic, anime composition, anime aesthetic, anime composition, anime aesthetic, anime composition, anime aesthetic, anime composition, anime aesthetic, anime composition, anime aesthetic, anime composition, anime aesthetic, anime composition, anime aesthetic, anime composition, anime aesthetic, anime composition, anime aesthetic, anime composition, anime aesthetic, anime composition, anime aesthetic, anime composition --ar 856:1200 --zoom 1'
            fname00 = '%02d%04d_0_%s.png' % (occupation_ind, card_ind, name_en)
            print(f'prompt01 = {prompt01}')
            print(f'fname01 = {fname01}')
            print(f'prompt00 = {prompt00}')
            print(f'fname00 = {fname00}')
            print('')
            card_ind += 1
