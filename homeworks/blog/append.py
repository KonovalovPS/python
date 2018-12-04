arr_names = []
arr_surnames = []
arr_fullnames = []

with open('names.txt', 'r') as names:
    for each in names:
        arr_names.append(each.strip('\n'))
        
with open('last_names.txt', 'r') as surnames:
    for each in surnames:
        arr_surnames.append(each.strip('\n').capitalize())
        
for i in range(1000):
    arr_fullnames.append(f'{arr_names[i]} {arr_surnames[i]}\n')
        
fullname = open('full_names.txt', 'w')

for each in arr_fullnames:
    fullname.write(each)

fullname.close()

print(arr_fullnames)