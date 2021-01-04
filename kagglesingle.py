import requests
from bs4 import BeautifulSoup
from pyquery import PyQuery
import re


def testsingle(url, count, outputstr, visited):
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:39.0)'}
    try:
        res = requests.get(url=url, headers=headers)
    except ConnectionError:
        return
    soup = BeautifulSoup(res.text, 'html.parser')
    html = str(soup.body)
    pq = PyQuery(html)
    tag = pq('script.kaggle-component')
    testsen = tag[1].text
    forknum = re.findall(r'forkCount\":(.*?),', testsen)[0]
    forkParent = re.findall(r'forkParent\":(.*?),', testsen)[0]
    fork_parent_info = re.findall(r'forkParent\":(.*?)}', testsen)[0]
    # when fork parent is private the forkParentID is 0
    count += 1
    while (True):
        if forkParent == 'null':
            outputstr += url + " " + " forknum: " + forknum + " " + "level: " + str(count) + " "
            visited.append(url)
            break
        else:
            if re.findall(r'kernelId\":(.*?),', fork_parent_info)[0] != '0':
                fork_parent_url = re.findall(r'url\":(.*?),', fork_parent_info)[0]
                fork_parent_url_combine = "https://www.kaggle.com" + fork_parent_url.replace('\"', '')
                if fork_parent_url == "":
                    return
                else:
                    if fork_parent_url_combine not in visited:
                            visited.append(fork_parent_url_combine)
                            outputstr += fork_parent_url_combine + " forknum: " + forknum + " level: " + str(count) + " "
                            testsingle(fork_parent_url_combine, count, outputstr, visited)
                    else:
                        pass

        break
    print(visited)


if __name__ == '__main__':
    startStr = ""
    singleUrl = "https://www.kaggle.com/snsinha0305/higher-lb-score-by-tuning-mloss-around-6-811"
    startCount = 0
    visitedarr = []
    print("test: " + str(testsingle(singleUrl, startCount, startStr, visitedarr)))

