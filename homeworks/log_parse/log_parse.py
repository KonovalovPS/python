# -*- encoding: utf-8 -*-
import collections
from dateutil.parser import parse
import is_true      #функция из первого ДЗ, чтобы отсеять строки не являющиеся записями об обращении к серверу
import datetime

def get_time(s):
    return parse(s[s.index('[') + 1 : s.index(']')])
    
def get_url(s):
    start = s.index('://')
    s = s[ start + 3 : s.index(' ', start)]
    if '?' in s:
        s = s[: s.index('?')]
    return s
    
def get_type(s):
    start = s.index('"')
    return s[start + 1 : s.index(' ', start)]
    
def del_www(s):
    idx = s.index('://')
    if 'www' in s[idx + 3: idx + 6]:
        s = '{}{}'.format(s[ :idx + 3], s[idx + 7:])
    return s
    
def response_time(s):
    return int(s.split()[-1])
    
def is_file(s):
    if get_url(s)[-1] == '/':
        return False
    return True

def parser(
    ignore_files=False,
    ignore_urls=[],
    start_at=None,
    stop_at=None,
    request_type=None,
    ignore_www=False,
    slow_queries=False
):

    output_arr = [] 
    arr = []  #массив урлов, удовлетворяющих условиям
    most_slowly = collections.defaultdict(lambda: [0, 0])
    f = open('log.log')
    for line in f:
        if is_true.is_true(line):
            if (start_at == None or get_time(line) >= start_at) and\
            (stop_at == None or get_time(line) <= stop_at) and\
            get_url(line) not in ignore_urls and\
            (get_type(line) in ignore_urls or ignore_urls == []) and\
            (ignore_files == False or is_file(line) == False):
                if ignore_www == True:
                    line = del_www(line)
                arr.append(get_url(line))
                most_slowly[get_url(line)][0] += 1
                most_slowly[get_url(line)][1] += response_time(line)   
    if slow_queries == True:
        for each in most_slowly:
            output_arr.append(most_slowly[each][1] // most_slowly[each][0])
        output_arr = sorted(output_arr, reverse = True)    
    else:
        counter = collections.Counter(arr)
        for elem, count in counter.most_common(5):
            output_arr.append(count)  
    print(output_arr[:5])    

parser()