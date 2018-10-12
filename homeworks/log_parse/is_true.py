def is_true(line):
    
    pattern = '[*/*/*] "* *" *'
    def search(line, pattern, k):                                

        for i in range(len(line) - len(pattern) + 1):                   
            counter = 0 
            for j in range(len(pattern)):
                if pattern[j] == line[i + j]:
                    counter += 1
                    
            if counter == len(pattern):
                k = i + j
                return {'result': True, 'k': k}

        return {'result': False, 'k': k}

        
    def search_stars(line, pattern):                           
        k = 0
        arr = pattern.split('*')
        for i in range(len(arr)):
            if arr[i] == '':
                continue
            if not search(line[k:], arr[i], k)['result']:            
                return False      
        return True
    
    return search_stars(line, pattern)