from threading import Thread
import time
flag=0
def fun():
        print('fun')

funThread=Thread(target=fun)
def ev():
    c=0
    while True:
        global flag
        if flag==1:
            end=time.time()
            print((end-start)%60)
            yield 'stop'
        yield c
        c+=2
        if(c==20):
            flag=1
            start=time.time()
            #Thread(target=fun).start()
            funThread.start()

gen=ev()
while True:
    time.sleep(5)
    temp=next(gen) #bs
    print(temp)
    if(temp=='stop'):
        break