from html.entities import html5
from pyexpat import model
from flask import Flask, render_template, request, redirect, url_for, flash
from flaskext.mysql import MySQL
import pymysql

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
    """ cur = conn.cursor(pymysql.cursors.DictCursor)
    cur.execute('SELECT * FROM table')
    data = cur.fetchall()
    cur.close() """
    return render_template('index.html')


@app.route('/insert', methods=['POST'])
def insert():
    #conn = mysql.connect()
    cur = conn.cursor(pymysql.cursors.DictCursor)
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        dob = request.form['dob']
        address = request.form['address']
        ug = request.form['ug']
        pg = request.form['pg']
        cur.execute("INSERT INTO table (name,email,phone,dob,address,ug,pg) VALUES (%s,%s,%s,%s,%s,%s,%s)" % (name,email,phone,dob,address,ug,pg))
        conn.commit()
        flash('Information Added successfully')
        return redirect(url_for('index.html'))

 
@app.route('/update/<id>', methods=['POST'])
def update(id):
    if request.method == 'POST':
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
            UPDATE table
            SET name = %s,
                email = %s,
                phone = %s,
                dob = %s,
                address = %s,
                ug = %s,
                pg = %s,
            WHERE id = %s
        """, (name,email,phone,dob,address, ug, pg))
        flash('Info Updated Successfully')
        conn.commit()
        return redirect(url_for('index.html'))
 
@app.route('/delete/<string:id>', methods = ['POST','GET'])
def delete(id):
    #conn = mysql.connect()
    cur = conn.cursor(pymysql.cursors.DictCursor)
  
    cur.execute('DELETE FROM table WHERE id = {0}'.format(id))
    conn.commit()
    flash('Info Removed Successfully')
    return redirect(url_for('index.html'))
 
# starting the app
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000, debug=True)
