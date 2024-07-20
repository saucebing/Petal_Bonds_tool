f = open('Cards2.md', 'r')
for line in f.readlines():
    columns = line.split('|')
    if len(columns) <= 1:
        continue
    else:
        card_id = columns[1]
        if card_id == '编号' or '---' in card_id:
            continue
        else:
            title_zh = columns[2]
            title_en = columns[3]
            print('%s,%s,%s,%s' % (title_en, card_id, title_zh, title_en))
