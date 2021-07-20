<h1> Open API를 이용한 영화 데이터 활용

ㅤ

<h2> 1. Open API를 활용하기


ㅤ

본고는 Python 프로그래밍 언어를 통해 영화 아카이브 자료를 효율적으로 활용하는 하나의 방법을 제시하는 데 목적을 두고 있다. 따라서 이번 발표는 영화사 연구와 관련된 개인적인 문제의식을 정교화하고 연구 방법론을 고민하기보다 연구에 필요한 데이터를 수집, 활용, 응용, 공유하는 방법론에 대한 고민을 다룰 것이다. 본 발표는 크게 두 부분으로 구성되는데, 첫 번째는 영화진흥위원회에서 제공하는 Open API를 이용하여 영화 상영과 관련된 데이터를 수집하는 방법이고, 두 번째는 영상자료원의 웹페이지 스크랩핑을 이용하여 필요한 영화 자료를 수집하는 방법이다.        




<h2> 2. 영화진흥위원회 영화상영정보 데이터베이스 활용   

`API(Application Programming Interface)`란 응용 프로그램(application) 소프트웨어를 구측하고 정의하기 위한 프로토콜 세트로, 운영 체제(OS)와 소프트웨어 사이, 네트워트 다바이스와 서버 사이, 혹은 서비스 플랫폼들 사이에서 이루어지는 커뮤니케이션을 위한 규약으로 활용된다.  

각각의 운영 체제에서는 해당 OS에서 작동하는 어플리케이션을 만들고 데이터를 저장하기 위해 API를  

컴퓨터와 컴퓨터가 인터넷을 통해서 의사소통을 하는 시대 
다양한 기기에서 서버에 있는 데이터를 읽고 쓰기 위해서는 서버에서 제공하는 웹 API를 통해서 처리할 수 있다. 


네트워크에서 기기들 간의 의사소통을 하는 규격 사항을 HTTP라고 하는데, 이런 웹 API를 어떻게 만들 것인지를 정의하는 것이 있는데, SOAP은 모든 네트워크의 요청과 반응을 XML이라는 데이터 포맷에 저장하여 주고 받는  

근래에는 `REST` 가 보편적으로 많이 사용된다. `REST`는 `Post`, `Get`, `Put`, `Delete` 메소드로 구성되는데, 이는 각각 데이터를 생성하기, 읽기, 업데이트하기, 삭제하기를 의미한다. `Get`을 이용해서 서버에 원하는 데이터를 `Request` (요청)하면, 서버로부터 해당 데이터를 `json`이라는 포맷으로 받아오게 된다. 
ㅤ


ㅤ

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

