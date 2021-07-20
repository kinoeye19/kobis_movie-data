<h1> Open API를 이용한 영화 데이터 활용


<h2> 영화진흥위원회 영화상영정보 데이터베이스 활용



영화관입장권통합전산망 오픈API 테스트
http://www.kobis.or.kr/kobisopenapi/homepg/main/main.do

REST 방식으로 호출하여 

> 시작코드 
```python
import urllib.request as ul
import json
import gspread
from oauth2client.service_account import ServiceAccountCredentials # pip install --upgrade google-api-python-client
import time
import pprint
pp = pprint.PrettyPrinter(indent=4)

```

