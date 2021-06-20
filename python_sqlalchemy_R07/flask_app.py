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

#'SeisanDB' class
class SeisanDB(db.Model):
    __tablename__ = 'SeisanDB'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True,nullable=False)
    name = db.Column(db.String(200),nullable=False)
    travel_costs = db.Column(db.Integer,nullable=False)
    date = db.Column(db.DateTime, default=date,nullable=False)
    pjcode = db.Column(db.String(200),nullable=False)

# avoid to input inccorect 'travel_costs' value
def check_travel_costs_format(input_travelcosts):
    value_true_or_false = False
    try:
        int(input_travelcosts)
    except TypeError:
        value_true_or_false = True
    except ValueError:
        value_true_or_false = True
    return value_true_or_false

# avoid to input inccorect 'date' value
def check_date_format(input_date):
    value_true_or_false = False
    try:
        date.fromisoformat(input_date)
    except ValueError:
        value_true_or_false = True
    return value_true_or_false

# avoid input null and blank
def check_input_value(req_form_travel,req_form_date,req_form_name,req_form_pjcode):
    req_travel = req_form_travel
    req_date = req_form_date
    req_name = req_form_name
    req_pjcode = req_form_pjcode

    # avoid to input inccorect 'name' and 'pjcode' value
    def check_name_pjcode(req_name,req_pjcode):
        if not req_name:
            input_name = none_name
            if not req_pjcode:
                input_pjcode = none_pjcode
            else:
                input_pjcode = req_pjcode
        else:
            input_name = req_name
            if not req_pjcode:
                input_pjcode = none_pjcode
            else:
                input_pjcode = req_pjcode
        return input_name,input_pjcode

    # avoid input null and blank
    if not req_travel:
        input_travelcosts = none_travelcosts
        if not req_date:
            input_date = none_date
            input_name,input_pjcode = check_name_pjcode(req_name,req_pjcode)

        else:
            if check_date_format(req_date):
                input_date = none_date
                input_name,input_pjcode = check_name_pjcode(req_name,req_pjcode)
            else:
                input_date = req_date
                input_name,input_pjcode = check_name_pjcode(req_name,req_pjcode)
    else:
        if check_travel_costs_format(req_travel):
            input_travelcosts = none_travelcosts
            if check_date_format(req_date):
                input_date = none_date
                input_name,input_pjcode = check_name_pjcode(req_name,req_pjcode)
            else:
                input_date = req_date
                input_name,input_pjcode = check_name_pjcode(req_name,req_pjcode)
        else:
            input_travelcosts = req_travel
            if check_date_format(req_date):
                input_date = none_date
                input_name,input_pjcode = check_name_pjcode(req_name,req_pjcode)
            else:
                input_date = req_date
                input_name,input_pjcode = check_name_pjcode(req_name,req_pjcode)

    if input_name == none_name or input_travelcosts == none_travelcosts or input_date == none_date or input_pjcode == none_pjcode:
        message = '不正な値が書き込まれました。入力内容を確認してください。'
    else:
        message = '正常に書き込みました。'

    seisandb= SeisanDB(name=input_name,travel_costs=input_travelcosts,date=input_date,pjcode=input_pjcode)

    return seisandb,message

@app.route('/')
def select_sql():
    message = 'Hello SQLAlchemy'
    seisandb = SeisanDB.query.order_by(SeisanDB.id).all()
    return render_template('view.html', message = message, seisandb = seisandb)

@app.route('/result', methods=['POST'])
def result():

    seisandb, message = check_input_value(request.form['travelcosts'],request.form['date'],request.form['name'],request.form['pjcode'])
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
