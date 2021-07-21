import urllib.request as ul

prdtyear_start = 1965 
prdtyear_end = 1966 
items = 10 
page = 1
key = "7d6adcbd79ec916a9d400b3f76f3ddfd"
url = "http://www.kobis.or.kr/kobisopenapi/webservice/rest/movie/searchMovieList.json?key={0}&prdtStartYear={1}&prdtEndYear={2}&itemPerPage={3}&curPage={4}".format(key, prdtyear_start, prdtyear_end, items, page)
print(url)

