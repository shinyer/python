import os

path = os.getcwd()
print(path)
old_name = os.listdir(path)
print(old_name)
for i in old_name:
    print(i[15:])
    if (i[-4:]) == '.JPG':
        os.rename(i,i[15:])
        os.chdir(path)


