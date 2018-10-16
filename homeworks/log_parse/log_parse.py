# -*- encoding: utf-8 -*-
from collections import defaultdict, Counter
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
    
def del_www(url):
    if url[:4] == 'www.':
        url = url[4:]
    return url
    
def get_response_time(s):
    return int(s.split()[-1])
    
def is_it_a_file(s):
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
    most_slowly = defaultdict(lambda: [0, 0])
    f = open('log.log')
    counter = Counter()
    for line in f:
        if is_true.is_true(line): 
            time = get_time(line)
            type = get_type(line)
            url = get_url(line)   
            response_time = get_response_time(line)
            is_file = is_it_a_file(line)
            if ignore_www:
                url = del_www(url)
            
            if (start_at == None or time >= start_at) and\
            (stop_at == None or time <= stop_at) and\
            url not in ignore_urls and\
            (type == request_type or request_type == None) and\
            (ignore_files == False or is_file == False):
                counter[url] += 1
                most_slowly[url][0] += 1
                most_slowly[url][1] += response_time
                
    if slow_queries == True:
        for each in most_slowly:
            output_arr.append(most_slowly[each][1] // most_slowly[each][0])
        output_arr = sorted(output_arr, reverse = True)[:5] 
    else:    
        for elem, count in counter.most_common(5):
            output_arr.append(count)   
            
    print(output_arr)

parser()