import pyodbc
app = Flask(__name__)

print("世界の皆さん、こんにちは")

def login():
	driver='{SQL Server}'
	server = 'YUUKI-PC\SQLEXPRESS'
	database = 'test'
	trusted_connection='yes'

	#Windows認証
	connect= pyodbc.connect('DRIVER='+driver+';SERVER='+server+';DATABASE='+database+';PORT=1433;Trusted_Connection='+trusted_connection+';')

    sql = "SELECT * FROM test_table"
	cursor = connect.cursor()
	cursor.execute( sql )
	rows = cursor.fetchall()
	#pprint.pprint( rows )

	cursor.close()
	connect.close()

'''MYSQLの場合
connection = pymysql.connect(
        host='localhost',
        db='mydb',
        user='root',
        password='',
        charset='utf8',
        cursorclass=pymysql.cursors.DictCursor
    )

sql = "SELECT * FROM players"
cursor = connection.cursor()
cursor.execute(sql)
players = cursor.fetchall()

cursor.close()
connection.close()
'''
for row in rows:
    print(rows["name"])