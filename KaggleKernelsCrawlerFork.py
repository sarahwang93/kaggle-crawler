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

global_lock = threading.Lock()

def testsingle(url,count,outputstring):
    fork_parent_url_combine = ''
    count += 1
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:39.0)'}
    res = requests.get(url=url, headers=headers)
    soup = BeautifulSoup(res.text, 'html.parser')
    html = str(soup.body)
    pq = PyQuery(html)
    tag = pq('script.kaggle-component')
    testsen = tag[1].text
    forknum = re.findall(r'forkCount\":(.*?),', testsen)[0]
    forkParent = re.findall(r'forkParent\":(.*?),', testsen)[0]
    if forkParent == 'null':
        outputstring += url + " " + " forknum: " + forknum + " " + "level: " + str(count)
        return
    else:
        # print("test" + forkParent)
        fork_parent_info = re.findall(r'forkParent\":(.*?)}', testsen)[0]
        # when fork parent is private the forkParentID is 0
        if re.findall(r'kernelId\":(.*?),', fork_parent_info)[0] != '0':
            fork_parent_url = re.findall(r'url\":(.*?),', fork_parent_info)[0]
            fork_parent_url_combine = "https://www.kaggle.com" + fork_parent_url.replace('\"', '')
            if fork_parent_url == '':
                pass
            else:
                outputstring += fork_parent_url_combine + " forknum: " + forknum + " level: " + str(count)
                testsingle(fork_parent_url_combine, count, outputstring)
    return outputstring

def read_write(inputurls, output, procenum):
    while global_lock.locked():
        sleep(0.01)
        continue

    global_lock.acquire()

    with open(inputurls, 'r') as inputf, open(output, 'w') as outputf:
        for line in inputf:
            temp = line.split(",")
            url = "https://www.kaggle.com/" + temp[0] + '/' + temp[1].replace('\n', '')
            try:
                outputstr = ""
                startcount = 0
                outputf.write(str(testsingle(url, startcount, outputstr)) + '\n')
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
