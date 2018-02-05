from urllib.request import Request, urlopen
from urllib.parse import urlencode, quote_plus
from xml.etree.ElementTree import fromstring
from PublicValue import *

class Holiday:
	##조회할 노선 아이디를 받는다.
	def __init__(self):
		## xml url
		Holiday.url = HOLIDAY_URL
		## 인증키
		Holiday.key = PRIVATE_KEY
		self.solYear = '2018'
		self.solMonth = '02'
		self.xmlStr = "" ##xml문자열 담을 변수
		self.root = None ##최상위 항목 담을 변수
		self.isOnInternet = True ## 인터넷연결여부 
		
		##xml요청 주소에 넘길 인자 세팅
		queryParams = '?' + urlencode({ quote_plus('serviceKey') : 'KEYKEY', quote_plus('solYear') : self.solYear, quote_plus('solMonth') : self.solMonth })
		queryParams = queryParams.replace("KEYKEY", Holiday.key)
		
		##xml문서 받아와 str으로 xmlStr에 담는다.
		request = Request(self.url + queryParams)
		request.get_method = lambda: 'GET'
		try:
			self.xmlStr = binToUtf8(urlopen(request).read())
			self.root = fromstring(self.xmlStr)
		except:
			self.isOnInternet = False
		
	## 본 정보의 루트태그 msgBody의 유무 체크
	def isSuccess(self):
		if not self.isOnInternet:
			return False
		return self.root.find("body")!=None
		
	## xml문서의 루트태그 리턴
	def getRoot(self):
		if not self.isOnInternet:
			return None
		return self.root
		
	## xml문서에서 본 정보(버스위치)리스트 리턴
	def getItems(self):
		if not self.isOnInternet:
			return []
		return self.root.find("body").find("items").findall("item")
	def isHoliday(self, date):
		hDate = []
		for i in self.getItems():
			hDate.append(i.findtext("locdate"))
		return date in hDate
	
		
##테스트코드
if __name__ == "__main__" :
	result = Holiday().isHoliday("20180216")
	print(str(int(result)))
#[0].findtext("locdate")

