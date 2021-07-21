import urllib.request as ul
import json
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pprint
pp = pprint.PrettyPrinter(indent=4)



############################################################################
# 구글시트 연동 테스트
############################################################################
scope = ['https://spreadsheets.google.com/feeds']
json_file_name = 'C:\\Users\\user\\Documents\\google_cloud_api\\movie-20210630-4e8dfa406085.json'
credentials = ServiceAccountCredentials.from_json_keyfile_name(json_file_name, scope)
gc = gspread.authorize(credentials)
spreadsheet_url = 'https://docs.google.com/spreadsheets/d/1BtT-SrZEuXupHA7GRJ6ABwcg2Dh_fe6lXJ-6TskYWNs/edit#gid=0'

# 문서 불러오기
doc = gc.open_by_url(spreadsheet_url)
worksheet = doc.worksheet('movie_data')

# # 읽기 - 셀
# cell_data = worksheet.acell('B3').value
# print(type(cell_data))
# print(cell_data)
# print('--------------------------\n')

# 읽기 - 범위
row_data = worksheet.row_values(3)
print(type(row_data))
print(row_data)
print('--------------------------\n')

# # 읽기 - 범위
# range_list = worksheet.range('A1:D3')
# for cell in range_list:
#     print(cell.value)

# # 쓰기 - 셀
# worksheet.update_acell('B1', 'b1 updated')

# # 쓰기 - 행 추가
# worksheet.append_row(['new1', 'new2', 'new3', 'new4'])

# # 쓰기 - 특정 행 추가
# worksheet.insert_row(['new1', 'new2', 'new3', 'new4'], 10)

# # 쓰기 - 시트 크기 맞추기
# worksheet.resize(10,4)

# # 쓰기 - 삭제
# worksheet.delete_rows(2, worksheet.row_count)
