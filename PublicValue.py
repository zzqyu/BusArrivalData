from DBControl import DBControl ##DB

BUS_LOCATION_URL = 'http://openapi.gbis.go.kr/ws/rest/buslocationservice'
ROUTE_STATION_URL = 'http://openapi.gbis.go.kr/ws/rest/busrouteservice/station'
PRIVATE_KEY = "zRuxSFejoJKPbOZdUuxyIUWJF7R56lxvA5LbRwxQWj8IVxCG2F6aYImQvUJIdzvjM3EDvvYQfrQyIirNaYWkqA%3D%3D"
PUBLIC_KEY = "1234567890"
KEY = PUBLIC_KEY
HOLIDAY_URL = "http://apis.data.go.kr/B090041/openapi/service/SpcdeInfoService/getRestDeInfo"

## binary data to utf-8
def binToUtf8(data):
	# 바이너리 데이터를 utf-16으로 디코딩한다
	# 수직 탭을 삭제한다
	return data.decode("utf-8").replace(u"\u000B", u"")

def getRouteList():
	dbc = DBControl("localhost", "root", "비번", "busarrivaldb")
	result=dbc.resultSql("select routeName, routeId From routeInfo;")
	routeList={}
	for row in result:
		if '50-1' in str(row):
			continue
		routeList[row['routeName']] = row['routeId']
	return routeList