from flask import Flask, render_template,request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.engine import URL
from datetime import date
import pyodbc

app = Flask(__name__)

#SQL server DB information
driver='{SQL Server}'
server = '任意'
database = '任意'
trusted_connection='yes' #windows authentication

#replace other value
none_name = '名無し'
none_travelcosts = '0'
none_date = '99991231'
none_pjcode = '99999999'

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
    pjcode = db.Column(db.String(200),nullable=False)

# avoid to input inccorect travel_costs value
def check_travel_costs_format(input_travelcosts):
    value_true_or_false = False
    try:
        int(input_travelcosts)
    except TypeError as tperror:
        value_true_or_false = True
    except ValueError as valerror:
        value_true_or_false = True
    return value_true_or_false

# avoid to input inccorect date value
def check_date_format(input_date):
    value_true_or_false = False
    try:
        date.fromisoformat(input_date)
    except ValueError as valerror:
        value_true_or_false = True
    return value_true_or_false

@app.route('/')
def select_sql():
    message = 'Hello SQLAlchemy'
    seisandb = SeisanDB.query.all()
    return render_template('view.html', message = message, seisandb = seisandb)

@app.route('/result', methods=['POST'])
def result():
    # avoid input null and blank
    if not request.form['travelcosts']:
        input_travelcosts = none_travelcosts
        if not request.form['date']:
            input_date = none_date
            if not request.form['name']:
                input_name = none_name
                if not request.form['pjcode']:
                    input_pjcode = none_pjcode
                else:
                    input_pjcode = request.form['pjcode']
            else:
                input_name = request.form['name']
                if not request.form['pjcode']:
                    input_pjcode = none_pjcode
                else:
                    input_pjcode = request.form['pjcode']
        else:
            if check_date_format(request.form['date']):
                input_date = none_date
                if not request.form['name']:
                    input_name = none_name
                    if not request.form['pjcode']:
                        input_pjcode = none_pjcode
                    else:
                        input_pjcode = request.form['pjcode']
                else:
                    input_name = request.form['name']
                    if not request.form['pjcode']:
                        input_pjcode = none_pjcode
                    else:
                        input_pjcode = request.form['pjcode']
            else:
                input_date = request.form['date']
                if not request.form['name']:
                    input_name = none_name
                    if not request.form['pjcode']:
                        input_pjcode = none_pjcode
                    else:
                        input_pjcode = request.form['pjcode']
                else:
                    input_name = request.form['name']
                    if not request.form['pjcode']:
                        input_pjcode = none_pjcode
                    else:
                        input_pjcode = request.form['pjcode']
    else:
        if check_travel_costs_format(request.form['travelcosts']):
            input_travelcosts = none_travelcosts
            if check_date_format(request.form['date']):
                input_date = none_date
                if not request.form['name']:
                    input_name = none_name
                    if not request.form['pjcode']:
                        input_pjcode = none_pjcode
                    else:
                        input_pjcode = request.form['pjcode']
                else:
                    input_name = request.form['name']
                    if not request.form['pjcode']:
                        input_pjcode = none_pjcode
                    else:
                        input_pjcode = request.form['pjcode']
            else:
                input_date = request.form['date']
                if not request.form['name']:
                    input_name = none_name
                    if not request.form['pjcode']:
                        input_pjcode = none_pjcode
                    else:
                        input_pjcode = request.form['pjcode']
                else:
                    input_name = request.form['name']
                    if not request.form['pjcode']:
                        input_pjcode = none_pjcode
                    else:
                        input_pjcode = request.form['pjcode']
        else:
            input_travelcosts = request.form['travelcosts']
            if check_date_format(request.form['date']):
                input_date = none_date
                if not request.form['name']:
                    input_name = none_name
                    if not request.form['pjcode']:
                        input_pjcode = none_pjcode
                    else:
                        input_pjcode = request.form['pjcode']
                else:
                    input_name = request.form['name']
                    if not request.form['pjcode']:
                        input_pjcode = none_pjcode
                    else:
                        input_pjcode = request.form['pjcode']
            else:
                input_date = request.form['date']
                if not request.form['name']:
                    input_name = none_name
                    if not request.form['pjcode']:
                        input_pjcode = none_pjcode
                    else:
                        input_pjcode = request.form['pjcode']
                else:
                    input_name = request.form['name']
                    if not request.form['pjcode']:
                        input_pjcode = none_pjcode
                    else:
                        input_pjcode = request.form['pjcode']

    if input_name == none_name or input_travelcosts == none_travelcosts or input_date == none_date or input_pjcode == none_pjcode:
        message = '不正な値が書き込まれました。入力内容を確認してください。'
    else:
        message = '正常に書き込みました。'

    seisandb= SeisanDB(name=input_name,travel_costs=input_travelcosts,date=input_date,pjcode=input_pjcode)
    db.session.add(seisandb)
    db.session.commit()

    return render_template('result.html', message = message, seisandb = seisandb)

@app.route('/show/<int:id>')
def show_date(id):
    message = "Hello id " + str(id)
    seisandb = SeisanDB.query.get(id)
    return render_template('result.html', message = message, seisandb = seisandb)

@app.route('/delete/<int:id>')
def delete(id):
    message = 'id' + str(id) + 'の行を削除しました。'

    seisandb_dl = SeisanDB.query.get(id)
    db.session.delete(seisandb_dl)
    db.session.commit()

    return render_template('delete_result.html', message = message)

if __name__ == '__main__':
    #app.run(debug=True)
    app.run()
