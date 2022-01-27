from flask import Flask, render_template, request, redirect, url_for, flash
from flaskext.mysql import MySQL
import pymysql

app = Flask(__name__)
app.secret_key = "Cairocoders-Ednalan"
  
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
    cur.execute('SELECT * FROM registration')
    data = cur.fetchall()
  
    cur.close()
    return render_template('Index', registration = data)
"""
@app.route('/Index1')
def Index1():
    # conn = mysql.connect()
    cur = conn.cursor(pymysql.cursors.DictCursor)
    cur.execute('SELECT * FROM registration')
    data = cur.fetchall()
  
    cur.close()
    return render_template('index.html', registration = data)

@app.route('/Index2')
def Index2():
   # conn = mysql.connect()
    cur = conn.cursor(pymysql.cursors.DictCursor)
    cur.execute('SELECT * FROM registration')
    data = cur.fetchall()
    cur.close()
    return render_template('index.html',registration = data)
"""
@app.route('/add_registration', methods=['POST'])
def add_registration():
    #conn = mysql.connect()
    cur = conn.cursor(pymysql.cursors.DictCursor)
    if request.method == 'POST':
        name = request.form['name']
        gender = request.form['optradio']
        rollno = request.form['rollno']
        email = request.form['email'] 
        address = request.form['address']
        phone = request.form['phone']
        course = request.form['course']
        sem = request.form['sem']
        cur.execute("INSERT INTO registration (name,gender,rollno,email,address,phone,course,sem) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)", (name,gender,rollno,email,address,phone,course,sem))
        conn.commit()
        flash('Information Added successfully')
        return redirect(url_for('Index'))

 
@app.route('/update/<id>', methods=['POST'])
def update_registration(id):
    if request.method == 'POST':
        name = request.form['name']
        gender = request.form['optradio']
        rollno = request.form['rollno']
        email = request.form['email'] 
        address = request.form['address']
        phone = request.form['phone']
        course = request.form['course']
        sem = request.form['sem']
        #conn = mysql.connect()
        cur = conn.cursor(pymysql.cursors.DictCursor)
        cur.execute("""
            UPDATE registration
            SET name = %s,
                gender = %s,
                rollno = %s,
                email = %s,
                address = %s,
                phone = %s,
                course = %s,
                sem = %s
            WHERE id = %s
        """, (name,gender,rollno,email,address,phone,course,sem,id))
        flash('Info Updated Successfully')
        conn.commit()
        return redirect(url_for('Index'))
 
@app.route('/delete/<string:id>', methods = ['POST','GET'])
def delete_registration(id):
    #conn = mysql.connect()
    cur = conn.cursor(pymysql.cursors.DictCursor)
  
    cur.execute('DELETE FROM registration WHERE id = {0}'.format(id))
    conn.commit()
    flash('Info Removed Successfully')
    return redirect(url_for('Index'))
 
# starting the app
if __name__ == "__main__":
    app.run(debug=True)
