<h1> Open API를 이용한 영화 데이터 활용

ㅤ

<h2> 1. Open API를 활용하기


ㅤ

API(Application Programming Interface)란 어플리케이션 소프트웨어를 구측하고 정의하기 위한 프로토콜 세트로, 소프트웨어 간, 인터넷 서비스 간, 커뮤니케이션을 위한 규약으로 활용된다.  

ㅤ


ㅤ
<h2> 2. 영화진흥위원회 영화상영정보 데이터베이스 활용   

***

[영화관입장권통합전산망 오픈API 테스트](http://www.kobis.or.kr/kobisopenapi/homepg/main/main.do)

REST 방식으로 호출하여 

> 시작코드 
```python
import urllib.request as ul
import json
import gspread
from oauth2client.service_account import ServiceAccountCredentials 
# pip install --upgrade google-api-python-client
import time
import pprint
pp = pprint.PrettyPrinter(indent=4)

```

