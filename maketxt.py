import os

files = os.listdir(r'./科幻小说')

f = open('./科幻小说.txt', 'a+')
for file in files:
    book_id = file.split('.')[0]
    print(book_id)
    f.write(book_id+'\n')
f.close()



# f = open('./科学.txt', 'r')
# ls = f.read().splitlines()
# for id in ls:
#     print(id)