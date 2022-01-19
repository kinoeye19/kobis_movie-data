import requests
import xmltodict
import json
import pandas as pd


titles = ['지옥의전선', '애혼', '회상', '사라토가본선(本線)']

for title in titles:
    key = "43B10JREK6A14GM0X5C5"
    url = "http://api.koreafilm.or.kr/openapi-data2/wisenut/search_api/search_xml2.jsp?collection=kmdb_new2&detail=N&title={0}&ServiceKey={1}".format(title, key)
    res = requests.get(url)
    if res.status_code == 200:
        content = requests.get(url).content
        dict = xmltodict.parse(content)
        jsonString = json.dumps(dict['Search']['Result'], ensure_ascii=False)
        jsonObj = json.loads(jsonString)
        for item in jsonObj['Row']:
            df = pd.DataFrame(jsonObj['Row'])
        print(">>>> [Success] Result Code : {0}".format(res.status_code))
        print(df.info())
        
    else:
        print(">>>> [Fail] Result Code : {0}".format(res.status_code))





#     print(item['title'])



