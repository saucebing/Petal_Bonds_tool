#!/usr/local/bin/python3
# -*-coding:utf-8 -*-
import os, sys, time, subprocess, tempfile, re
import timeit
from collections import Counter, OrderedDict
import pickle
import random
import bidict
import json

out_temp = [None] * 1024
fileno = [None] * 1024

def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

def exec_cmd(cmd, index = 0, wait = True, vm_id = 0):
    global out_temp, fileno
    print('[VM%d]: CMD: ' % vm_id, cmd)
    out_temp[index] = tempfile.SpooledTemporaryFile()
    fileno[index] = out_temp[index].fileno()
    p1 = subprocess.Popen(cmd, stdout = fileno[index], stderr = fileno[index], shell=True)
    if wait:
        p1.wait()
    out_temp[index].seek(0)
    return p1

def parallel_cmd(cmd, num, wait = True):
    global out_temp, fileno
    p = []
    for i in range(0, num):
        out_temp[i] = tempfile.SpooledTemporaryFile()
        fileno[i] = out_temp[i].fileno()
        real_cmd = '%s %d' % (cmd, i)
        print('CMD: ', real_cmd)
        p.append(subprocess.Popen(real_cmd, stdout = fileno[i], stderr = fileno[i], shell=True))
    for i in range(0, num):
        if wait:
            p[i].wait()
        out_temp[i].seek(0)
    return p

def find_str(pattern, string):
    pat = re.compile(pattern)
    return pat.findall(string)[0]

def find_list(pattern, lst):
    pat = re.compile(pattern)
    return [item for item in lst if pat.findall(item)]

def find_list_2(pattern, lst):
    pat = re.compile(pattern)
    return [pat.findall(item)[0] for item in lst if pat.findall(item)]

def split_str(string, char=' '):
    return list(filter(lambda x:x, string.split(char)))

def b2s(s):
    return str(s, encoding = 'utf-8')

def get_res(index = 0):
    global out_temp, fileno
    return b2s(out_temp[index].read())

def transform(a, a_min, a_max, b_min, b_max):
    return (a - a_min) / (a_max - a_min) * (b_max - b_min) + b_min

def transform_list(a, a_min, a_max, b_min, b_max):
    return [transform(item, a_min, a_max, b_min, b_max) for item in a]

def cvalue(a):
    c = int(256 * a - 1)
    res = '#%02x%02x%02x' % (c, c, c)
    return res

def cvalue_list(a):
    return [cvalue(item) for item in a]

def sync_file(ind):
    cmd = 'scp -r /root/vmm_control test%d:/root/' % ind
    exec_cmd(cmd)
    print(get_res())

class color:
    black = '\033[0;30m'
    red = '\033[0;31m'
    green = '\033[0;32m'
    yellow = '\033[0;33m'
    blue = '\033[0;34m'
    purple = '\033[0;35m'
    dark_green = '\033[0;36m'
    white = '\033[0;37m'
    grey = '\033[90m'
    l_red = '\033[91m' #fail
    l_green = '\033[92m'
    l_yellow = '\033[93m' #warn
    l_blue = '\033[94m' #blue
    l_purple = '\033[95m'
    l_dark_green = '\033[96m'
    end = '\033[0m'
    bold = '\033[1m'
    underline = '\033[4m'

    b_black = '\033[0;40m'
    b_read = '\033[0;41m'
    b_green = '\033[0;42m'
    b_yellow = '\033[0;43m'
    b_blue = '\033[0;44m'
    b_purple = '\033[0;45m'
    b_dark_green = '\033[0;46m'
    b_white = '\033[0;47m'
    b_grey = '\033[100m'
    b_l_red = '\033[101m' #fail
    b_l_green = '\033[102m'
    b_l_yellow = '\033[103m' #warn
    b_l_blue = '\033[104m' #blue
    b_l_purple = '\033[105m'
    b_l_dark_green = '\033[106m'

    beg1 = green + bold
    beg2 = blue + bold
    beg3 = green + bold
    beg4 = blue + bold
    beg5 = yellow + bold
    beg6 = white
    beg7 = red + bold

def expression_to_string(expression):
    final = ''
    ind = 1
    params = bidict.bidict({})
    for it in expression.split('+'):
        it = it.strip()
        if '"' not in it:
            final += '$%d' % ind
            params[ind] = it
            ind += 1
        else:
            final += it[1:-1]
    return final, params

def expression_to_string_ref(expression, params_ref):
    final = ''
    for it in expression.split('+'):
        it = it.strip()
        if '"' not in it:
            ind = params_ref.inverse[it]
            final += '$%d' % ind
        else:
            final += it[1:-1]
    return final

def main():
    ind = 0
    ress = []
    string_map = OrderedDict({})
    for parent_dir,subdirs,files in os.walk('/server/api/'):
        for f in files:
            fpath = os.path.join(parent_dir, f)
            if not 'node_modules' in fpath and fpath[-3:] == '.js':
                #if ind == 10:
                #    break
                print(fpath)
                f1 = open(fpath, 'r')
                content = f1.read()
                f1.close()
                pattern = '(config.lang_select\(\{"en": (.*?), "zh": (.*?)\}\))'
                pat = re.compile(pattern)
                res = pat.findall(content)
                for item in res:
                    origin = item[0]
                    string1, params = expression_to_string(item[1])
                    string2 = expression_to_string_ref(item[2], params)
                    params = dict(params)
                    print(f'origin: {origin}')
                    print(f'string1: {string1}, params1: {params}')
                    print(f'string2: {string2}, params2: {params}')
                    final = f'config.translate(req?.jwt?.language || req?.body?.language, "{string1}", ' + '{'
                    final += ', '.join(['%s: %s' % (key, params[key]) for key in params])
                    final += "})"
                    print(f'replace: {final}')
                    string_map[string1] = {"English (en)": string1, "Chinese (Simplified) (zh)": string2}
                    content = content.replace(origin, final)
                if not len(res) == 0:
                    f2 = open(fpath, 'w')
                    f2.write(content)
                    f2.close()
                    print(f'{color.red}Writed: {fpath}{color.end}')
                print('\n\n\n\n\n')
                #print(res)
                ress += res
                ind += len(res)
    #print(ress)
    print(ind)
    #json_map = json.dumps(string_map, indent=4, separators=(',', ':'), ensure_ascii=False)
    #f = open('language_map.json', 'w')
    #f.write(json_map)
    #f.close()

if __name__ == "__main__":
    main()
