import requests
from bs4 import BeautifulSoup 
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pprint 
import time
import math

prodStartYear ='1958'
prodEndYear = '1959'
sheetname = 'kmdb_mv_censor_list_kor'


scope = ['https://spreadsheets.google.com/feeds']
json_file_name = '/Users/seungjin/Documents/google_api/movie-20210630.json'
credentials = ServiceAccountCredentials.from_json_keyfile_name(json_file_name, scope)
gc = gspread.authorize(credentials) 
spreadsheet_url = 'https://docs.google.com/spreadsheets/d/1BtT-SrZEuXupHA7GRJ6ABwcg2Dh_fe6lXJ-6TskYWNs/edit#gid=0'



def get_items_cntNum(startCount, prodStartYear, prodEndYear):
    url = 'https://www.kmdb.or.kr/db/have/detailSearch/censorSearch?_csrf=5149a247-b5d3-4711-ab75-cd288c64cf98&collection=kmCENSOR&tabName=sojangTab&startCount={0}&storedPosition=&censorName=&censorNameSelect=AND&releatedMovieName=&releatedMovieNameSelect=AND&movieMemberName=&movieMemberType=director&movieMemberTypeSelect=AND&companyName=&contentName=&prodStartYear={1}&prodEndYear={2}'.format(startCount, prodStartYear, prodEndYear)
    res = requests.get(url)
    res.raise_for_status()
    soup = BeautifulSoup(res.text, "lxml")
    # data_rows = soup.find("table", attrs={"class":"data-table medium transform-m"}).find("tbody").find_all("tr")
    count = soup.find("div", attrs={"class":"result-block-tt noline"}).find("span", attrs={"class":"em weighty"}).get_text()
    return(count)
            
     
items_cntNum = get_items_cntNum(0, prodStartYear, prodEndYear)
startCounts = math.floor(int(items_cntNum)/10)*10
print(">>> startCount 최대값 = {0}".format(startCounts))
print('--------------------------\n')


items = 100 # 페이지당 데이터 수
pages = math.ceil(startCounts/items)
column_cnt = 5 # 구글시트 데이터 항목 컬럼 수

doc = gc.open_by_url(spreadsheet_url)
worksheet = doc.worksheet(sheetname)

if worksheet.row_count > 2: worksheet.delete_rows(3, worksheet.row_count)
time.sleep(2)
tot_items = 0
for startCount in range(0, startCounts+10, 10):
    print('>>> [INFO] Get Movie Censor Info (startCount:{0})'.format(startCount))
    url = 'https://www.kmdb.or.kr/db/have/detailSearch/censorSearch?_csrf=5149a247-b5d3-4711-ab75-cd288c64cf98&collection=kmCENSOR&tabName=sojangTab&startCount={0}&storedPosition=&censorName=&censorNameSelect=AND&releatedMovieName=&releatedMovieNameSelect=AND&movieMemberName=&movieMemberType=director&movieMemberTypeSelect=AND&companyName=&contentName=&prodStartYear={1}&prodEndYear={2}'.format(startCount, prodStartYear, prodEndYear)
    res = requests.get(url)
    res.raise_for_status()
    soup = BeautifulSoup(res.text, "lxml")
            
    data_rows = soup.find("table", attrs={"class":"data-table medium transform-m"}).find("tbody").find_all("tr")
    
    for row in data_rows:
        columns = row.find_all("td")
        
            # "td" 요소가 하나 또는 그 이하를 빼주는 코드 > 불필요한 공백을 없애기 위해, 각각의 "tr"들 사이의 차이를 고려. 
        if len(columns) <= 1: # 의미 없는 data는 skip 
            continue     
        
        data = [column.get_text().strip() for column in columns]
        # print(type(data)) 
        tot_items = tot_items + 1
        movie_censor_list = [data]   
        worksheet.append_rows(movie_censor_list)
    time.sleep(10)
    print(">>> [INFO] Upload Completed ... {0}/{1}\n".format(tot_items, int(items_cntNum)))
        # print(movie_censor_list)
     
    
    
    