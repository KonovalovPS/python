def is_true(line):
    
    pattern = '[*/*/*] "* *://*.*" * *'
    def search(line, pattern, k):                                

        for pat_position in range(len(line) - len(pattern) + 1):                   
            counter = 0 
            for each in range(len(pattern)):
                if pattern[each] == line[pat_position + each]:
                    counter += 1
                    
            if counter == len(pattern):
                k = pat_position + each
                return {'result': True, 'k': k}

        return {'result': False, 'k': k}

        
    def search_stars(line, pattern):                           
        k = 0
        arr = pattern.split('*')
        for index in range(len(arr)):
            if arr[index] == '':
                continue
            if not search(line[k:], arr[index], k)['result']:            
                return False      
        return True
    
    return search_stars(line, pattern)