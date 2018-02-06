from DriveData import DriveData
from BusLocation import BusLocation
from RouteStation import RouteStation ##정류장 목록
from DBControl import DBControl ##DB
from Holiday import Holiday
import time
from datetime import datetime
from os import path
import sys

## 노선번호:노선ID
routeList = {
	"1" : "233000048", "1-1": "233000051", "2": "233000013", "2-1": "233000052", 
	"2-2" : "233000035", "2-3": "233000030", "2-4": "233000029", "3": "233000028", 
	"3-1" : "233000027", "4": "233000015", "4-1": "233000038", "5-2": "233000019", 
	"5-4" : "233000021", "6": "233000040", "6-2": "233000043", "6-3": "233000045", 
	"7" : "233000058", "8": "233000046", "8-1": "233000057", "8-2": "233000049", 
	"8-3" : "233000047", "9": "233000025", "11": "233000041", "11-2": "233000060", 
	"11-4" : "233000062", "11-5": "233000059", "14": "233000024", "15": "233000022", 
	"16" : "233000034", "17": "233000044", "18": "233000036", "19": "233000026", 
	"20" : "233000079", "21": "233000080", "23": "233000085", "24": "233000081", 
	"25" : "233000094", "26": "233000095", "27": "233000096", "33-1": "233000010", 
	"33-2" : "233000126", "2000B": "233000264",  "2000A" : "233000263",
	"8155": "233000139", "9801": "241005320", "9802": "241005300"
	}	
##노선번호:정류장목록
routeStationList = {}
for no in routeList.keys():
	rs = RouteStation(routeList[no])
	routeStationList[no]=rs.getStationNames()
	

##DB
##객체생성
server = "서버주소"
serverPort = "int 포트번호" 
dbc = DBControl(server, "root", "비번", "busarrivaldb", serverPort)
#dbc = DBControl("localhost", "root", "005410", "busarrivaldb")
while True:##하루에 1번 작동하는 루프(날짜바뀔때)
	try:
		now = datetime.now()	
		date = str(datetime.date(now))
		weekday = str(datetime.weekday(now))
		isHoliday = Holiday().isHoliday(date.replace("-", ""))
		
		##오늘날짜 테이블있는지 확인
		if not dbc.isThisTable(DBControl.dateToTableName(date)):
			##없으면 만든다
			dbc.createTable(DBControl.dateToTableName(date))
		##오늘날짜 카운트 있는지 확인	
		if not dbc.isThisTable(DBControl.dateToTableName(date)+"count"):
			##없으면 만든다
			dbc.createCountTable(DBControl.dateToTableName(date))
		else:##있으면 실제 row수와 기록을 맞춘다
			dbc.updateRowViaTable(DBControl.dateToTableName(date))
		##row가져오기
		curCount = int(dbc.getRowViaTable(DBControl.dateToTableName(date)))

			
		preLocaList=[]
		nowLocaList=[]

	
		##하루종일 도는 루프 (날짜 바뀌면 빠짐)
		while True:
			##현재시간 프린트
			now = datetime.now()
			print(now)
			curTime = str(datetime.time(now))
			if  "00:00" in curTime.split('.')[0] :
				time.sleep(60)
				break
			elif  datetime(now.year, now.month, now.day, 1, 0, 0, 0)< now <datetime(now.year, now.month, now.day, 5, 0, 0, 0):
				time.sleep((5-now.hour)*3600 + (60-now.minute)*60) ## 01시부터 05시까지 슬립
			##모든 노선을 조회하는 루프
			for no in routeList.keys():
				##조회할 노선의 버스위치 목록
				dd = DriveData(routeList[no])
				if not dd.isConnectInternet():
					print("인터넷 확인하세요!")
					sys.exit()
				locaList = dd.getBusLocations()
				
				if len(locaList)>0:
					print(no, "번")
					##조회한 노선의 모든 버스위치를 출력하는 루프 
					for bl in locaList:
						cbl = BusLocation(bl)
						##정류장순서
						seq = int (cbl.getStationSeq() )
						##버스 및 현재 정류장정보 출력
						locaInfo =  cbl.getAll()
						nowLocaList.append(locaInfo)
						stationName = routeStationList[no][seq]
						if (not locaInfo in preLocaList) and (not "(경유)" in stationName) :
							print("[seq]", seq, "[id]", cbl.getStationId(), end = "" )
							print("[name]", stationName)
							dbc.addData(DBControl.dateToTableName(date), ( str(curCount),  stationName,  cbl.getStationId(), curTime, no, cbl.getRouteId(), cbl.getPlateNo(), cbl.getEndBus(), weekday, str(int(isHoliday))  ) )
							dbc.incRowViaTable(DBControl.dateToTableName(date))
							curCount+=1	
			preLocaList = nowLocaList[:]
			nowLocaList = []
			print("\n25초 대기....")
			for i in range(25):
				print (i+1)
				time.sleep(1)
	except Exception as e :
		ferr = open("error-"+str(now).replace(".", "_")[1]+".txt", 'w')
		ferr.write(str(e)+"\n")
		print(e)
		ferr.close()


