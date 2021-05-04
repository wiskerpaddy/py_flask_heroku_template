'''
theme
・「PythonからDB(SQL Server)を操作するアプリケーション(仮)」

index
・「theme」
・「index」
・「DB」
・「outline」
・「function」

DB
・「SeisanDB」：交通費精算用DB。交通費が発生した人、日付、金額等を記録する。主キーは「Kakei_id」。
・「KakeiDB」 ：家計簿用DB。収入、支出、人、項目名、日付を記録する。主キーは「id」。

outline
・アプリを起動すると結合したDBの中身を一覧で表示する。
・各列にはリンクがある。
・リンク押下すると日付の詳細を縦に一人分だけ表示する。

'''

from flask import Flask, request, render_template
import pyodbc

app = Flask(__name__)

def getConnection():
    driver='{SQL Server}'
    server = '任意'
    database = '任意'
    trusted_connection='yes'
    connection = pyodbc.connect('DRIVER='+driver+';SERVER='+server+';DATABASE='+database+';PORT=1433;Trusted_Connection='+trusted_connection+';')
    return connection

@app.route('/')
def list_dates():
    connection = getConnection()
    cur = connection.cursor()
    message = "日付一覧"

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

    select_ = "SELECT * "
    #select_ = "SELECT id, COALESCE(name,'名無しさん') AS name, COALESCE(incomes,0) AS incomes, COALESCE(expenses,0) AS expenses, COALESCE(travel_costs,0) AS travel_costs "
    from_ = "FROM SeisanDB LEFT JOIN KakeiDB ON KakeiDB.kakei_id = SeisanDB.id"
    where_ = ";"
    sql = select_ + from_ + where_
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

@app.route('/show/<int:id>')
def show_date(id):

    connection = getConnection()
    message = "Hello money " + str(id)
    #select_ = "SELECT id, COALESCE(name,'名無しさん') AS name, COALESCE(incomes,0) AS incomes, COALESCE(expenses,0) AS expenses, COALESCE(travel_costs,0) AS travel_costs "

    #select_ = "SELECT * "
    #from_ = "FROM SeisanDB LEFT JOIN KakeiDB ON KakeiDB.kakei_id = SeisanDB.id "
    #where_ = "WHERE SeisanDB.kakei_id = ?"

    #sql = "SELECT * FROM SeisanDB LEFT JOIN KakeiDB ON KakeiDB.kakei_id = SeisanDB.id WHERE SeisanDB.id = ?"
    #sql = select_ + from_ + where_
    #sql = "SELECT * FROM players LEFT JOIN jobs ON jobs.id = players.job_id WHERE players.id = %s"

    cur = connection.cursor()
    #pyodecでパラメータを渡す際には「%s」ではなく「?」を使う
    cur.execute("SELECT * FROM SeisanDB LEFT JOIN KakeiDB ON KakeiDB.kakei_id = SeisanDB.id WHERE SeisanDB.id = ?", id)
    row = cur.fetchone()

    cur.close()
    connection.close()

    return render_template('details.html', message = message, row = row)

if __name__ == "__main__":
    app.run()
