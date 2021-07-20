import urllib.request as ul
import json
import gspread
from oauth2client.service_account import ServiceAccountCredentials # pip install --upgrade google-api-python-client
import time
import pprint
pp = pprint.PrettyPrinter(indent=4)

# 입력값
prdtyear_start = "1970" # 제작년도 시작
prdtyear_end = "1971" # 제작년도 끝
sheet_name = "movie_info_1970s"

# Google Sheet API
scope = ['https://spreadsheets.google.com/feeds'] # 구글 스프레드시트에 접근하는 코드 
json_file_name = '/Users/seungjin/Documents/google_api/movie-20210630.json'
credentials = ServiceAccountCredentials.from_json_keyfile_name(json_file_name, scope)
gc = gspread.authorize(credentials)
spreadsheet_url = 'https://docs.google.com/spreadsheets/d/1RfF4-DFF7nBZXTDfpK4O_-d3E1SWC7gZMYoR59AxvyA/edit#gid=0'
############################################################################
# 영화관입장권통합전산망 오픈API 테스트
# http://www.kobis.or.kr/kobisopenapi/homepg/main/main.do
############################################################################

# 영화정보 가져오는 함수
def get_movie_info(prdtyear_start, prdtyear_end, items, page):
    key = "6613daf03feaf54e97b18efc72513c2f"
    url = "http://www.kobis.or.kr/kobisopenapi/webservice/rest/movie/searchMovieList.json?key={0}&prdtStartYear={1}&prdtEndYear={2}&itemPerPage={3}&curPage={4}".format(key, prdtyear_start, prdtyear_end, items, page)
    request = ul.Request(url)
    response = ul.urlopen(request)
    rescode = response.getcode()
    if(rescode == 200):
        data = response.read() # URL 주소로 요청한 데이터를 읽어온 뒤 data 라는 변수에 할당  
        print(">>>> [Success] Result Code : {0}".format(rescode))
    else:
        print(">>>> [Fail] Result Code : {0}".format(rescode))
    result = json.loads(data) # json 모듈에 내장된 loads() 함수를 이용하여 json 문자열을 python 객체로 변환한 뒤 result 변수에 저장
    pp.pprint(result) # 자료의 구조를 보기 위해 pprint() 함수를 실행. 
    movie_list = result['movieListResult']['movieList'] # kobis API에서 제공하는 json 자료의 구조를 분석한 결과 ['movieListResult'] 라는 리스트 자료 안에 ['movieList'] 리스트 자료가 있고, 그 안에 영화에 대한 세부 정보가 있음을 확인하였음.   
    tot_cnt = result['movieListResult']['totCnt'] 
    return [movie_list, tot_cnt] # 함수의 리턴 값은 앞서 변수로 지정한 movie_list, tot_cnt를 리스트 형태로 받는다.  


# 조건을 만족하는 총 영화 건수를 가져옴
# api 호출건당 최대 100건만 가능하므로 page수를 파악하여 호출건수 제어하기 위해 아래와 같이 코드를 설계함. 
a = get_movie_info(prdtyear_start, prdtyear_end, 1, 1)
tot_cnt = a[1]
print(">>> 총 영화수 : {0}".format(tot_cnt))
print('--------------------------/n') 

# 조건을 만족하는 전체 영화데이터 가져옴.
# 한번에 100건씩 pages 만큼 호출
items=100 # 페이지당 데이터 수
pages=round(tot_cnt/items)
column_cnt = 14 # 구글시트 데이터 항목 컬럼 수
# # 시트 불러오기
doc = gc.open_by_url(spreadsheet_url)
worksheet = doc.worksheet(sheet_name)
# # 시트 초기화
if worksheet.row_count > 3: worksheet.delete_rows(4, worksheet.row_count)
time.sleep(1)
tot_items = 0
for page in range(1, pages+1):
    print('>>> [INFO] Get Movie Info (page:{0})'.format(page))
    r = get_movie_info(prdtyear_start, prdtyear_end, items, page)
    movie_list = []   # 리스트를 초기화하는 이유 : for 문을 실행하면서 기존에 있던 리스트를 지우고 새로운 영화 정보를 넣기 위해서. 
    for m in r[0]:
        tot_items = tot_items + 1
        movie_list.append(
            [
                m['movieCd'],
                m['movieNm'],
                m['movieNmEn'],
                m['prdtYear'],
                m['openDt'],
                m['typeNm'],
                m['prdtStatNm'],
                m['nationAlt'],
                m['genreAlt'],
                m['repNationNm'],
                m['repGenreNm'],
                '' if not m['directors'] else m['directors'][0]['peopleNm'],
                '' if not m['companys'] else m['companys'][0]['companyCd'],
                '' if not m['companys'] else m['companys'][0]['companyNm'],
            ]
        )
    """ 
        (참고) 컬랙션형 데이터가 들어가 있는 형태.. 문서상에는 문자열이라 되어 있음
        'companys': [{'companyCd': '20060351', 'companyNm': '서울영화사'}],
        'directors': [{'peopleNm': '신상옥'}],
    """
    #pp.pprint(movie_list)
    worksheet.append_rows(movie_list)
    time.sleep(2)
    print(">>> [INFO] Upload Completed ... {0}/{1}/n".format(tot_items, tot_cnt))

# 시트 크기 맞춤
worksheet.resize(tot_cnt+3, column_cnt)
print(">>> Completed...")






