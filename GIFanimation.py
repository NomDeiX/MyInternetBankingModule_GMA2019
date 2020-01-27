import datetime
import os

path= "test.txt"
subor = open(path,"r+")
print(subor.readline())
subor.close()


#os.remove(subor)
