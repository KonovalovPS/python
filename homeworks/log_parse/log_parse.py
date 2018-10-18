# -*- encoding: utf-8 -*-
from collections import defaultdict, Counter
from dateutil.parser import parse
import re
import datetime

def del_www(url):
    if url[:4] == 'www.':
        url = url[4:]
    return url    
    
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
        
        elements = re.findall(r'(\d+/.+/\d{4} \d{2}:\d{2}:\d{2})] "(\S+) .+://(\S+) .+" \d+ (\d+)', line)
        if not len(elements) or len(elements[0]) != 4:
            continue
            
        time = parse(elements[0][0])
        req_type = elements[0][1]
        url = elements[0][2]
        response_time = int(elements[0][3])

        is_file = False
        if url[-1] != '/' and re.findall(r'\.\w{3,4}', url[-5:]):
            is_file = True
            
        if ignore_www:
            url = del_www(url)
            
        if (start_at == None or time >= parse(start_at)) and\
        (stop_at == None or time <= parse(stop_at)) and\
        url not in ignore_urls and\
        (req_type == request_type or request_type == None) and\
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
    return output_arr  

parser()