from html.entities import html5
from pyexpat import model
from flask import Flask, render_template, request, redirect, url_for, flash
from flaskext.mysql import MySQL
import pymysql
import sqlalchemy

app = Flask(__name__)
app.secret_key = "Secret Key"
  
mysql = MySQL()
import aws_credentials as rds  


# MySQL configurations
conn = pymysql.connect(
        host= rds.host, #endpoint link
        port = rds.port, # 3306
        user = rds.user, # admin
        password = rds.password, #adminadmin
        db = rds.db, #test
        
        )

        
@app.route('/')
def Index():
    cur = conn.cursor(pymysql.cursors.DictCursor)
    cur.execute('SELECT * FROM studenttable')
    data = cur.fetchall()
    cur.close()
    return render_template('index.html', students = data)


@app.route('/insert', methods=['POST'])
def insert():
    #conn = mysql.connect()
    cur = conn.cursor(pymysql.cursors.DictCursor)
    if request.method == 'POST':
        id = request.form['id']
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        dob = request.form['dob']
        address = request.form['address']
        ug = request.form['ug']
        pg = request.form['pg']
        cur.execute("INSERT INTO studenttable (id,name,email,phone,dob,address,ug,pg) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)", (id,name,email,phone,dob,address,ug,pg))
        conn.commit()
        flash('Information Added successfully')
        return redirect(url_for('Index'))

 


@app.route('/update', methods=['POST'])
def update(id):
    if request.method == 'POST':
        numid = request.form['id']

        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        dob = request.form['dob']
        address = request.form['address']
        ug = request.form['ug']
        pg = request.form['pg']
        #conn = mysql.connect()
        cur = conn.cursor(pymysql.cursors.DictCursor)
        cur.execute("""
        UPDATE studenttable 
        SET name = %s, email = %s, phone = %s, dob = %s, 
        address = %s, ug = %s, pg = %s, WHERE id = %s 
        """, (name,email,phone,dob,address, ug, pg, numid))
        flash('Info Updated Successfully')
        conn.commit()
        return redirect(url_for('Index'))
 

@app.route('/delete', methods = ['GET', 'POST'])
def delete(id):
    #conn = mysql.connect()
    id = request.form['id']

    cur = conn.cursor(pymysql.cursors.DictCursor)
    cur.execute('DELETE FROM studenttable WHERE id = {0}'.format(id))
    conn.commit()
    flash('Info Removed Successfully')
    return redirect(url_for('Index'))
 
# starting the app
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000, debug=True)
