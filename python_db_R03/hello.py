from flask import Flask, render_template
import pyodbc

app = Flask(__name__)

def getConnection():
    driver='{SQL Server}'
    server = 'YUUKI-PC\SQLEXPRESS'
    database = 'test'
    trusted_connection='yes'
    connection = pyodbc.connect('DRIVER='+driver+';SERVER='+server+';DATABASE='+database+';PORT=1433;Trusted_Connection='+trusted_connection+';')
    return connection

@app.route('/')
def select_sql():
    connection = getConnection()
    cur = connection.cursor()
    message = "Hello world"

    #sql = SELECT name, travel_costs FROM test_table
    #sql = "DELETE FROM SeisanDB WHERE name = 'yuki'"
    #date型は''で囲まないとint型になる
    #sql  = "INSERT INTO SeisanDB(name,travel_costs,date) VALUES('yuki', 5000, '2021-05-01')"
    #sql = "SELECT * FROM SeisanDB LEFT JOIN KakeiDB ON KakeiDB.date = SeisanDB.date"
    #sql = "SELECT name,incomes,expenses,travel_costs FROM SeisanDB LEFT JOIN KakeiDB ON KakeiDB.kakei_date = SeisanDB.date"
    #sql = "SELECT id, COALESCE(family_name, first_name, '名無しさん') AS name FROM users;
    #COALESCE(nullを置き換える列,置き換える値)
    #sql = "SELECT COALESCE(name,'名無しさん'),COALESCE(expenses,0),COALESCE(travel_costs,0) FROM SeisanDB LEFT JOIN KakeiDB ON KakeiDB.kakei_date = SeisanDB.date"
    #sql = "SELECT COALESCE(SeisanDB.date),COALESCE(SeisanDB.name,'名無しさん'),COALESCE(incomes,0),COALESCE(expenses,0),COALESCE(travel_costs,0) FROM SeisanDB LEFT JOIN KakeiDB ON KakeiDB.kakei_date = SeisanDB.date"
    sql = "SELECT id, COALESCE(name,'名無しさん') AS name, COALESCE(incomes,0) AS incomes, COALESCE(expenses,0) AS expenses, COALESCE(travel_costs,0) AS travel_costs FROM SeisanDB LEFT JOIN KakeiDB ON KakeiDB.kakei_date = SeisanDB.date"
    '''
    cur.execute(sql)
    connection.commit()

    sql = "SELECT * FROM SeisanDB"
    '''
    cur.execute( sql )
    rows = cur.fetchall()

    cur.close()
    connection.close()
    return render_template('view.html', message = message, rows = rows)

if __name__ == "__main__":
    app.run()