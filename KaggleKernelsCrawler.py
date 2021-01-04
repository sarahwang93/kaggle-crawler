import requests
from bs4 import BeautifulSoup
from pyquery import PyQuery    
import re


def testsingle(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:39.0)'}
    res = requests.get(url=url ,headers=headers) 
    soup = BeautifulSoup(res.text,'html.parser')
    html = str(soup.body)
    pq = PyQuery(html)
    tag = pq('script.kaggle-component')
    testsen=  tag[1].text
    forknum = re.findall(r'forkCount\":(.*?),', testsen)[0]
    if int(forknum) > 0:
        return url + '\t' + forknum
    else:
        return



if __name__ == '__main__':
    inputurls= "/Users/sarahwang93/professional/archive/process_data/parent_url/parent_urls.csv"
    output = "forknum_12_21.txt"
    procenum=0
    print("text")
    with open(inputurls, 'r') as inputf, open(output, 'w') as outputf:
        for line in inputf:
            procenum+=1
            if procenum<=2106:
                continue
            if procenum%100==0:
                print("processed:"+str(procenum))
            temp = line.strip().split(",")
            url= "https://www.kaggle.com/"+temp[1]+'/'+temp[2]
            try:
                outputf.write(testsingle(url)+'\n')
                outputf.flush()
            except:
                print("skip\t"+url)

