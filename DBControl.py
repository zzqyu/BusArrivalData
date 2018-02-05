import pymysql
from datetime import datetime
class DBControl:
	def __init__(self, _host, _id, _pw, _dbname, _port=3306):
		#self.con = pymysql.connect(host, port, id, pw, dbname, charset='utf8')
		self.con = pymysql.connect(host=_host, port=_port, user=_id, password=_pw, database=_dbname, charset='utf8')
		self.cur = self.con.cursor(pymysql.cursors.DictCursor)
		self.tableTitle=("id", "stationName","stationID","arrTime","routeNo","routeID","endBus","weekday","holiday")
		self.tableItemLen = (7, 40, 10, 16, 20, 10, 2,2,2)
		self.cur.execute("set names utf8")
	def __del__(self):
		self.con.close()
		
	##테이블생성
	def createTable(self, tableName):
		sql = "create table " + tableName + " ("
		for i in range(len(self.tableTitle)):
			sql+=(self.tableTitle[i] + " varchar(" + str(self.tableItemLen[i]) + ") not null,")
		sql+="primary key(id) );"
		print("[테이블생성 sql]", sql)
		self.cur.execute(sql)
		self.con.commit()
		
	##테이블확인
	def isThisTable(self, tableName):
		self.cur.execute("show tables like '%s'" % tableName)
		printstr =str(self.cur.fetchall())
		print("[]", printstr)
		return tableName in printstr
		
	##count테이블생성
	def createCountTable(self, tableName):
		self.cur.execute( "create table "+tableName+"count (count char(7) not null);")
		self.cur.execute( "insert into " + tableName + "count (count) values ('%s');" % self.getRowViaSql(tableName))
		self.con.commit()
		
	##row 	
	def getRowViaSql(self, tableName):
		self.cur.execute( "select count(*) from %s;" % tableName)
		answer = self.cur.fetchall()
		print("[getRowViaSql]", answer)
		return list(answer[0].values())[0]
	def getRowViaTable(self, tableName):
		self.cur.execute("select * from " + tableName + "count")
		answer = self.cur.fetchall()
		print("[getRowViaTable]", answer)
		return list(answer[0].values())[0]
	def updateRowViaTable(self, tableName):
		curRow = self.getRowViaTable(tableName)
		realRow = self.getRowViaSql(tableName)
		self.cur.execute("update " + tableName + "count set count='%s' where count='%s';" % (realRow, curRow))
	
	def incRowViaTable(self, tableName):
		curRow = int(self.getRowViaTable(tableName))
		sql = "update " + tableName + "count set count='%d' where count='%d';" % (curRow+1, curRow)
		print("[incRowViaTable]", sql)
		self.cur.execute(sql)
	
	##데이터추가
	def addDate(self, tableName, data):
		if len(self.tableTitle) != len(data):
			return False
			
		sql = "insert into " + tableName + " ("
		for i in self.tableTitle:
			sql+=(i+",")
			
		sql=sql[:-1] + ") values ("
		#sql+="\b) values ("
		for i in data:
			sql+=("'%s'," % i)
		#sql+="\b) ;"
		sql=sql[:-1] + ") ;"
		print("[데이터추가 sql]", sql)
		self.cur.execute(sql)
		self.con.commit()
		return True
		
	def dateToTableName(date):
		return "data"+date.replace("-", "")
		
if __name__ == "__main__":
	now = datetime.now()	
	date = str(datetime.date(now))
	localhost = "localhost"
	server = "106.251.162.106"
	serverPort = 11636
	#dbc = DBControl(server, "root", "005410", "test", serverPort)
	#print(dbc.getRowViaSql("date20180201"))
	dbc = DBControl(server, "root", "005410", "busarrivaldb", serverPort)
	#print(dbc.isThisTable(DBControl.dateToTableName(date)))
	#dbc.createTable(DBControl.dateToTableName(date))
	#print(dbc.isThisTable(DBControl.dateToTableName(date)+"count"))
	#dbc.createCountTable(DBControl.dateToTableName(date))
	#print(dbc.getRowViaSql(DBControl.dateToTableName(date)))
	dbc.cur.execute("insert into data20180205 (id,stationName,stationID,arrTime,routeNo,routeID,endBus,weekday,holiday) values ('3','장안6리','233001419','18:14:08.423130','1','233000048','0','0','1') ;")
	dbc.con.commit()