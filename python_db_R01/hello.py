from flask import Flask, render_template
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
def select_sql():
    connection = getConnection()
    cur = connection.cursor()
    message = "Hello world"

    #sql = SELECT name, money FROM test_table
    #sql = "DELETE FROM test_table WHERE name = 'yuki'"
    #date型は''で囲まないとint型になる
    #sql  = "INSERT INTO test_table(name,money,date) VALUES('yuki', 5000, '2021-05-01')"
    sql = "DELETE FROM test_table WHERE name = 'yuki'"
    cur.execute(sql)
    connection.commit()

    sql = "SELECT * FROM test_table"

    cur.execute( sql )
    rows = cur.fetchall()

    cur.close()
    connection.close()
    return render_template('view.html', message = message, rows = rows)

if __name__ == "__main__":
    app.run()
