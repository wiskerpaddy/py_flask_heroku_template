from flask import Flask, render_template,request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.engine import URL
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import pyodbc

app = Flask(__name__)

#SQL server DB information
driver='{SQL Server}'
server = '任意'
database = '任意'
trusted_connection='yes' #windows authentication

# an connection_string, which the Session will use for connection
# resources, typically in module scope
connection_string ='DRIVER='+driver+';SERVER='+server+';DATABASE='+database+';PORT=1433;Trusted_Connection='+trusted_connection+';'
db_uri = URL.create("mssql+pyodbc", query={"odbc_connect": connection_string})
app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
db = SQLAlchemy(app)

#SeisanDB class
class SeisanDB(db.Model):
    __tablename__ = 'SeisanDB'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(200))
    travel_costs = db.Column(db.Integer)
    date = db.Column(db.DateTime, default=datetime.date)

@app.route('/')
def select_sql():
    message = "Hello SQLAlchemy"

    seisandb = SeisanDB.query.all()

    return render_template('view.html', message = message, seisandb = seisandb)

@app.route("/result", methods=["POST"])
def result():
    #id
    input_name = request.form["name"]
    input_travelcosts = request.form["travelcosts"]
    input_date = request.form["date"]
    '''
    SeisanDB.name = input_name
    SeisanDB.travel_costs = input_travelcosts
    SeisanDB.date = input_date
    '''
    seisandb_up = SeisanDB(name=input_name,travel_costs=input_travelcosts,date=input_date)
    db.session.add(seisandb_up)
    db.session.commit()

    return render_template("result.html", name = input_name, travelcosts = input_travelcosts, date = input_date)

if __name__ == "__main__":
    app.run()
