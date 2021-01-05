import requests
from bs4 import BeautifulSoup
from pyquery import PyQuery
import re


class kagglesingle:
    def testsingleurl(self, url, count, outputstr, visited, return_arr):
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

        if url not in visited:
            visited.append(url)
        else:
            pass

        if forkParent == 'null':
            outputstr += url + " " + " forknum: " + forknum + " " + "level: " + str(count) + " "
            if len(visited) == count:
                print(outputstr)
                return_arr[0] = visited[0]
                return_arr[1] = count
            return return_arr
        else:
            if re.findall(r'kernelId\":(.*?),', fork_parent_info)[0] != '0':
                fork_parent_url = re.findall(r'url\":(.*?),', fork_parent_info)[0]
                fork_parent_url_combine = "https://www.kaggle.com" + fork_parent_url.replace('\"', '')
                if fork_parent_url == "":
                    pass
                else:
                    # TO-DO: how to end recursive call from here
                    if fork_parent_url_combine not in visited:
                        outputstr += url + " forknum: " + forknum + " level: " + str(count) + " "
                        if count <= len(visited):
                            self.testsingleurl(fork_parent_url_combine, count, outputstr, visited, return_arr)

            return return_arr


if __name__ == '__main__':
    test_url = kagglesingle()
    startStr = ""
    returnArr = [None] * 2
    singleUrl = "https://www.kaggle.com/snsinha0305/higher-lb-score-by-tuning-mloss-around-6-811"
    startCount = 0
    visitedArr = []
    print("test: " + str(test_url.testsingleurl(singleUrl, startCount, startStr, visitedArr, returnArr)))
    print(visitedArr)
