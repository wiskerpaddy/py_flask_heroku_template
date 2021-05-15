from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import pyodbc
from sqlalchemy.engine import URL

app = Flask(__name__)

driver='{SQL Server}'
server = '任意'
database = '任意'
trusted_connection='yes'

connection_string ='DRIVER='+driver+';SERVER='+server+';DATABASE='+database+';PORT=1433;Trusted_Connection='+trusted_connection+';'
db_uri = URL.create("mssql+pyodbc", query={"odbc_connect": connection_string})
app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
db = SQLAlchemy(app)

class SeisanDB(db.Model):
    __tablename__ = '任意'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Text())
    travel_costs = db.Column(db.Integer)
    date = db.Column(db.DateTime, default=datetime.date)

@app.route('/')
def select_sql():
    message = "Hello SQLAlchemy"

    seisandb = SeisanDB.query.all()

    return render_template('view.html', message = message, seisandb = seisandb)

if __name__ == "__main__":
    app.run()