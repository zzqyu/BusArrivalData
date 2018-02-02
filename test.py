from DriveData import DriveData
from BusLocation import BusLocation
from RouteStation import RouteStation ##정류장 목록
import datetime
import time


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
	"33-2" : "233000126", "50-1": "241483004", "50-1(대광1차)": "241483010", "2000B": "233000264", 
	"2000A" : "233000263", "8155": "233000139", "9801": "241005320", "9802": "241005300"
	}
routeStationList = {}
for no in routeList.keys():
	rs = RouteStation(routeList[no])
	routeStationList[no]=rs.getStationNames()

while True:
	print(datetime.datetime.now())
	for no in routeList.keys():
		
		dd = DriveData(routeList[no])
		if not dd.isConnectInternet():
			print("인터넷 확인하세요!")
			break
		locaList = dd.getBusLocations()
		if len(locaList)>0:
			print(no, "번")
			for bl in locaList:
				cbl = BusLocation(bl)
				seq = int(cbl.getStationSeq())
				print(cbl.getAll(), end=" ")
				print(routeStationList[no][seq])
		
	print("\n20초 대기....")
	for i in range(20):
		print (i+1)
		time.sleep(1)



