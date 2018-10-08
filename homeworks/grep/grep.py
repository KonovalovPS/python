
import argparse
import sys

def output(line):
    print(line)

    
def search(line, pattern, k, params):                      #функция поиска строки(паттерна)                                 

    for i in range(len(line) - len(pattern) + 1):                   
        counter = 0
        
        for j in range(len(pattern)):
            if pattern[j] == line[i + j] or pattern[j] == '?':
                counter += 1
                
        if counter == len(pattern):
            k = i + j
            return {'result': True, 'k': k}

    return {'result': False, 'k': k}

    
def search_stars(line, pattern, params):                  #функция поиска строки(паттерна)
                                                          #с учетом звездочек 
    if params.ignore_case == True:
        line = line.lower()
        pattern = pattern.lower()
        
    pattern = pattern.strip('*')                            
    if pattern == '':
        return True
    k = 0
    arr = pattern.split('*')
    for i in range(len(arr)):
        if arr[i] == '':
            continue
        if not search(line[k:], arr[i], k, params)['result']:            
            if params.invert == False:
                return False      
            if params.invert == True:
                return True
    
    if params.invert == True:
        return False
    return True

    
def grep(lines, params):
    before = max(params.before_context, params.context)
    after = max(params.after_context, params.context)

    main_counter = 0                                
    dic = {}                                   
    after_count = 1                 #переменная, позволяющая добавить after количество строк
                                    #после подходящей под описание строки
    last_true_idx = 0
    for idx, line in enumerate(lines, start = 1):
    
        after_count -= 1
            
        line = line.rstrip()
        
        dic.update({idx: line})     
        if len(dic) > before + 1:
            dic.pop(idx - before - 1)
        
        if search_stars(line, params.pattern, params):      
            for each in dic:
                if each > last_true_idx:
                    if params.line_number == True:
                        decorator = ':'
                        if each != idx:
                            decorator = '-'
                        decorator = str(each) + decorator
                    else:
                        decorator = ''
                    main_counter += 1
                    if params.count == False:
                        output(decorator + dic[each])
            after_count = after + 1
            last_true_idx = idx
            
        if 0 < after_count <= after:
            if params.line_number == True:
                decorator = '-'
                decorator = str(idx) + decorator
            else:
                decorator = ''
            output(decorator + dic[idx])
            last_true_idx += 1 

    if params.count == True:
        output(str(main_counter))
    
    
def parse_args(args):
    parser = argparse.ArgumentParser(description='This is a simple grep on python')
    parser.add_argument(
        '-v', action="store_true", dest="invert", default=False, help='Selected lines are those not matching pattern.')
    parser.add_argument(
        '-i', action="store_true", dest="ignore_case", default=False, help='Perform case insensitive matching.')
    parser.add_argument(
        '-c',
        action="store_true",
        dest="count",
        default=False,
        help='Only a count of selected lines is written to standard output.')
    parser.add_argument(
        '-n',
        action="store_true",
        dest="line_number",
        default=False,
        help='Each output line is preceded by its relative line number in the file, starting at line 1.')
    parser.add_argument(
        '-C',
        action="store",
        dest="context",
        type=int,
        default=0,
        help='Print num lines of leading and trailing context surrounding each match.')
    parser.add_argument(
        '-B',
        action="store",
        dest="before_context",
        type=int,
        default=0,
        help='Print num lines of trailing context after each match')
    parser.add_argument(
        '-A',
        action="store",
        dest="after_context",
        type=int,
        default=0,
        help='Print num lines of leading context before each match.')
    parser.add_argument('pattern', action="store", help='Search pattern. Can contain magic symbols: ?*')
    return parser.parse_args(args)


def main():
    params = parse_args(sys.argv[1:])
    grep(sys.stdin.readlines(), params)



if __name__ == '__main__':
    main()

