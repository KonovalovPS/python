
import argparse
import sys

k = 0

def output(line):
    print(line)

def tomato(line, pattern):                      #функция поиска строки(паттерна)                                 
    global k

    for i in range(len(line) - len(pattern) + 1):                   
        counter = 0
        
        for j in range(len(pattern)):
            if pattern[j] == line[i + j] or pattern[j] == '?':
                counter += 1
                
            if counter == len(pattern):
                k = i + j
                return True

def big_tomato(line, pattern):                  #функция поиска строки(паттерна)
    pattern = pattern.strip('*')                #с учетом звездочек
    if pattern == '':
        return True
    j = 0
    arr = pattern.split('*')
    for i in range(len(arr)):
        if not tomato(line[j:], arr[i]):
            return False
        j = k                
        
    return True
            

def grep(lines, params):
    count = 0
    end = 0
    before = max(params.before_context, params.context)
    after = max(params.after_context, params.context)
    appropriate = []                            #массив, содержащий индексы, подходящих строк
    output_lines = {}                           #словарь, в котором будут строки на выход
    output_index = 1
    
    for idx, line in enumerate(lines, start = 1):
		    
        line = line.rstrip()
        new_line = line
		
        if params.ignore_case == True:
            new_line = new_line.lower()
            params.pattern = params.pattern.lower()
            
        if params.invert == False:
              
            if big_tomato(new_line, params.pattern):
                appropriate.append(idx)
                for i in range(after + before + 1):
                    j = idx - before + i         
                    if j > 0 and j <= len(lines) and j > end:
                        output_index = j
                        output_lines[output_index] = lines[j - 1]
                end = j                         #переменная для того, чтобы не брать строки
                                                #из других блоков
        else:
          
            if  not big_tomato(new_line, params.pattern):
                appropriate.append(idx)
                for i in range(after + before + 1):
                    j = idx - before + i         
                    if j > 0 and j <= len(lines) and j > end:
                        output_index = j
                        output_lines[output_index] = lines[j - 1]
                        #output_lines.append(lines[j-1])
                end = j    
    
    if params.count == True:
        output(str(len(appropriate)))

    else: 
        for key in output_lines:   
            if params.line_number == True:
                decorator = ':'
                if key not in appropriate:
                    decorator = '-'
                decorator = str(key) + decorator
            else:
                decorator = ''
                    
            output(decorator + output_lines[key])
            
             
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

