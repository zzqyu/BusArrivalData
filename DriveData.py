﻿from urllib.request import Request, urlopen
from urllib.parse import urlencode, quote_plus
from xml.etree.ElementTree import fromstring
from PublicValue import *

class DriveData:
	##조회할 노선 아이디를 받는다.
	def __init__(self, routeId):
		## xml url
		DriveData.url = BUS_LOCATION_URL
		## 인증키
		DriveData.key = KEY
		self.routeId = routeId
		self.xmlStr = "" ##xml문자열 담을 변수
		self.root = None ##최상위 항목 담을 변수
		self.isOnInternet = True ## 인터넷연결여부 
		
		##xml요청 주소에 넘길 인자 세팅
		queryParams = '?' + urlencode({quote_plus('serviceKey') : "KEYKEY", quote_plus('routeId') : self.routeId })
		queryParams = queryParams.replace("KEYKEY", DriveData.key)
		
		##xml문서 받아와 str으로 xmlStr에 담는다.
		request = Request(self.url + queryParams)
		request.get_method = lambda: 'GET'
		try:
			self.xmlStr = binToUtf8(urlopen(request).read())
			self.root = fromstring(self.xmlStr)
		except:
			self.isOnInternet = False
			
	def isConnectInternet(self):
		return self.isOnInternet
		
	## 본 정보의 루트태그 msgBody의 유무 체크
	def isSuccess(self):
		if not self.isOnInternet:
			return False
		return self.root.find("msgBody")!=None
		
	## xml문서의 루트태그 리턴
	def getRoot(self):
		if not self.isOnInternet:
			return None
		return self.root
		
	## xml문서에서 본 정보(버스위치)리스트 리턴
	def getBusLocations(self):
		if not self.isSuccess():
			return []
			
		aList = self.root.find("msgBody").getchildren()
		##정류장 순서 기준을 정렬
		sorted(aList, key = lambda x: int(x.findtext("stationSeq")))
		return aList

		
##테스트코드
if __name__ == "__main__" :
	dd = DriveData("233000010")
	print (dd.getBusLocations()[0].findtext("plateNo"))


