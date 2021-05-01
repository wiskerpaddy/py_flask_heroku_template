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
    message = "Hello world"

    sql = "SELECT * FROM test_table"
    cursor = connection.cursor()
    cursor.execute( sql )
    rows = cursor.fetchall()

    cursor.close()
    connection.close()
    return render_template('view.html', message = message, rows = rows)

if __name__ == "__main__":
    app.run()