from subprocess import call
import multiprocessing



def func1():
    call(["python", "./WAMP/run.py"])

def func2():
    call(["python", "./Flask/run.py"])

if __name__ == '__main__':
    p1 = multiprocessing.Process(target=func1)
    p2 = multiprocessing.Process(target=func2)
    p1.start()
    p2.start()
