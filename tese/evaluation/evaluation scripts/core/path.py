import os

path = 'Results/segmentino'
mylist = os.listdir(path)
print(len(mylist))
for i in range(0, len(mylist)-1):
    if mylist[i] == 'Aggregate':
        print('ALERT')
        mylist.pop(i)
print(len(mylist))
