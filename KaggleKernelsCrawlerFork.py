from datetime import datetime

import requests
from bs4 import BeautifulSoup
from pyquery import PyQuery
import re
import threading
from time import time, sleep
import multiprocessing
from multiprocessing import Pool, Process, Manager
from datetime import datetime
from kagglesingle import kagglesingle

global_lock = threading.Lock()


def read_write(inputurls, output, procenum):
    startPro = kagglesingle()
    while global_lock.locked():
        sleep(0.01)
        continue

    global_lock.acquire()

    with open(inputurls, 'r') as inputf, open(output, 'w') as outputf:
        for line in inputf:
            temp = line.split(",")
            url = "https://www.kaggle.com/" + temp[0] + '/' + temp[1].replace('\n', '')
            try:
                startCount = 0
                startString = ""
                visitedArr = []
                returnVal = [None] * 2
                outputf.write(str(startPro.testsingleurl(url, startCount, startString, visitedArr, returnVal)) + '\n')
                outputf.flush()
            except Exception as e:
                print(e)
                print("skip\t" + url)

    global_lock.release()


if __name__ == '__main__':
    manager = multiprocessing.Manager()
    tasks = manager.Queue()
    results = manager.Queue()

    # method1: use lock and open 10 thread to read and write
    '''
    inputurls= "urls.csv"
    output = "forkfromurl.txt"
    procenum=0


    threads = []

    for i in range(0,10):
        t = threading.Thread(target=read_write, args=("urls.csv", "forkfromurl.txt", 0))
        threads.append(t)
        t.start()
    [thread.join() for thread in threads]
    '''

    # method2: open 4 processes with process pool
    '''
    num_processes = 4
    pool = multiprocessing.Pool(processes=num_processes)
    processes = []

    new_process = multiprocessing.Process(target=read_write,args=("urls.csv", "forkfromurl.txt", 0))
    processes.append(new_process)
    new_process.start()
    '''

    # method3 open process pool to open 8 threads read and write in parallel
    print("Start at:", datetime.now())
    start = datetime.now()
    pool = Pool(8)
    df_collection = pool.apply(read_write, args=("test_set_1.csv", "forkfromurl_test_1.txt", 0))
    pool.close()
    pool.join()
    print("End at:", datetime.now())
