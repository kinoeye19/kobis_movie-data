import urllib.request as ul
import json
import gspread
from oauth2client.service_account import ServiceAccountCredentials # pip install --upgrade google-api-python-client
import time
import pprint
pp = pprint.PrettyPrinter(indent=4)

# 입력값
prdtyear_start = "1960" # 제작년도 시작
prdtyear_end = "1961" # 제작년도 끝
sheet_name = "c"

# Google Sheet API
scope = ['https://spreadsheets.google.com/feeds']
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
    key = "7d6adcbd79ec916a9d400b3f76f3ddfd"
    url = "http://www.kobis.or.kr/kobisopenapi/webservice/rest/movie/searchMovieList.json?key={0}&prdtStartYear={1}&prdtEndYear={2}&itemPerPage={3}&curPage={4}".format(key, prdtyear_start, prdtyear_end, items, page)
    # url = "http://www.kobis.or.kr/kobisopenapi/webservice/rest/movie/searchMovieList.json?key={0}&prdtStartYear={1}&prdtEndYear={2}&itemPerPage={3}&curPage={4}".format(key, prdtyear_start, prdtyear_end, items, page)
    request = ul.Request(url)
    response = ul.urlopen(request)
    rescode = response.getcode()
    if(rescode == 200):
        data = response.read()
        print(">>>> [Success] Result Code : {0}".format(rescode))
    else:
        print(">>>> [Fail] Result Code : {0}".format(rescode))
    result = json.loads(data) 
    # pp.pprint(result)
    movie_list = result['movieListResult']['movieList']
    tot_cnt = result['movieListResult']['totCnt']
    return [movie_list, tot_cnt]


# 조건을 만족하는 총 영화 건수를 가져옴
# api 호출건당 최대 100건만 가능하므로 page수를 파악하여 호출건수 제어하기 위함 (토탈 카운터를 알아야 호출할 페이지를 알아야 함 가져오기 위함)
a = get_movie_info(prdtyear_start, prdtyear_end, 1, 1)
tot_cnt = a[1]
print(">>> 총 영화수 : {0}".format(tot_cnt))
print('--------------------------\n') 

# 시트 불러오기
doc = gc.open_by_url(spreadsheet_url)
worksheet = doc.worksheet(sheet_name)
# 시트 초기화
if worksheet.row_count > 3: worksheet.delete_rows(4, worksheet.row_count)


# 조건을 만족하는 전체 영화데이터 가져옴.
# 한번에 100건씩 pages 만큼 호출
items=100 # 페이지당 데이터 수
pages=round(tot_cnt/items)
column_cnt = 14 # 구글시트 데이터 항목 컬럼 수


time.sleep(1)
tot_items = 0
for page in range(1, pages+1):
    print('>>> [INFO] Get Movie Info (page:{0})'.format(page))
    r = get_movie_info(prdtyear_start, prdtyear_end, items, page)
    movie_info_list = []   
    for m in r[0]:
        tot_items = tot_items + 1
        movie_info_list.append(
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
    worksheet.append_rows(movie_info_list)
    time.sleep(2)
    print(">>> [INFO] Upload Completed ... {0}/{1}\n".format(tot_items, tot_cnt))

# 시트 크기 맞춤
worksheet.resize(tot_cnt+3, column_cnt)
print(">>> Completed...")






