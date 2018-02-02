from urllib.request import Request, urlopen
from urllib.parse import urlencode, quote_plus
from xml.etree.ElementTree import fromstring

class DriveData:
	##조회할 노선 아이디를 받는다.
	def __init__(self, routeId):
		## xml url
		DriveData.url = 'http://openapi.gbis.go.kr/ws/rest/buslocationservice'
		## 인증키
		DriveData.key = "zRuxSFejoJKPbOZdUuxyIUWJF7R56lxvA5LbRwxQWj8IVxCG2F6aYImQvUJIdzvjM3EDvvYQfrQyIirNaYWkqA%3D%3D"
		self.routeId = routeId
		self.xmlStr = "" ##xml문자열 담을 변수
		self.root = None ##최상위 항목 담을 변수
		
		##xml요청 주소에 넘길 인자 세팅
		queryParams = '?' + urlencode({quote_plus('serviceKey') : "KEYKEY", quote_plus('routeId') : self.routeId })
		queryParams = queryParams.replace("KEYKEY", DriveData.key)
		
		##xml문서 받아와 str으로 xmlStr에 담는다.
		request = Request(self.url + queryParams)
		request.get_method = lambda: 'GET'
		self.xmlStr = DriveData.binToUtf8(urlopen(request).read())
		self.root = fromstring(self.xmlStr)
		
	## 본 정보의 루트태그 msgBody의 유무 체크
	def isSuccess(self):
		return self.root.find("msgBody")!=None
		
	## xml문서의 루트태그 리턴
	def getRoot(self):
		return self.root
		
	## xml문서에서 본 정보(버스위치)리스트 리턴
	def getBusLocations(self):
		return self.root.find("msgBody").getchildren()
		
	## binary data to utf-8
	def binToUtf8(data):
		# 바이너리 데이터를 utf-16으로 디코딩한다
		# 수직 탭을 삭제한다
		return data.decode("utf-8").replace(u"\u000B", u"")
		
		
##테스트코드
if __name__ == "__main__" :
	dd = DriveData("233000010")
	print (dd.getBusLocations()[0].findtext("plateNo"))


