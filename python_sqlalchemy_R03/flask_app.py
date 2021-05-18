from flask import Flask, render_template,request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.engine import URL
from datetime import date
from flaskext.markdown import Markdown
import pyodbc

app = Flask(__name__)
Markdown(app)

#SQL server DB information
driver='{SQL Server}'
server = 'YUUKI-PC\SQLEXPRESS'
database = 'test'
trusted_connection='yes' #windows authentication

# an connection_string, which the Session will use for connection
# resources, typically in module scope
connection_string ='DRIVER='+driver+';SERVER='+server+';DATABASE='+database+';PORT=1433;Trusted_Connection='+trusted_connection+';'
db_uri = URL.create('mssql+pyodbc', query={'odbc_connect': connection_string})
app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
db = SQLAlchemy(app)

#SeisanDB class
class SeisanDB(db.Model):
    __tablename__ = 'SeisanDB'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True,nullable=False)
    name = db.Column(db.String(200),nullable=False)
    travel_costs = db.Column(db.Integer,nullable=False)
    date = db.Column(db.DateTime, default=date,nullable=False)

#chaeck type
def type_condition(v):
    if type(v) is str:
        return type(v) is str
    elif type(v) is int:
        return type(v) is int
    elif type(v) is date:
        return type(v) is date
    else:
        return type(v) is None

@app.route('/')
def select_sql():
    message = 'Hello SQLAlchemy'

    seisandb = SeisanDB.query.all()

    return render_template('view.html', message = message, seisandb = seisandb)

@app.route('/result', methods=['POST'])
def result():
    #id
    input_name = request.form.get('name')
    if (input_name is None) or (input_name == ''):
        input_name == '名無し'

    input_travelcosts = request.form.get('travelcosts')
    if (input_travelcosts is None) or (input_travelcosts == ''):
        input_travelcosts == 0

    input_date = request.form.get('date')
    if (input_date is None) or (input_date == ''):
        input_date == date.today()

    seisandb_up = SeisanDB(name=input_name,travel_costs=input_travelcosts,date=input_date)
    db.session.add(seisandb_up)
    db.session.commit()

    return render_template('result.html', name = input_name, travelcosts = input_travelcosts, date = input_date)

@app.route('/delete/<int:id>')
def delete(id):
    message = 'id' + str(id) + 'の行を削除しました。'

    seisandb_dl = SeisanDB.query.get(id)
    db.session.delete(seisandb_dl)
    db.session.commit()

    return render_template('delete_result.html', message = message)

if __name__ == '__main__':
    app.run(debug=True)