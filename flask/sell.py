from distutils import debug
from flask import Flask, render_template, request
from flask_mysqldb import MySQL

app=Flask(__name__)
app.config['MYSQL_HOST']='localhost'
app.config['MYSQL_USER']='root'
app.config['MYSQL_PASSWORD']=''
app.config['MYSQL_DB']='user'

mysql=MySQL(app)
@app.route('/')
def entry():
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM productdetails')
    data = cursor.fetchall()
    mysql.connection.commit()
    cursor.close()
    return render_template('sales.html',output_data=data)

@app.route('/add' , methods = ['POST', 'GET'])
def adding():
    cursor = mysql.connection.cursor()
    proid=request.form.get('productID')
    product=request.form.get('productName')
    item=request.form.get('item')
    rate=int(request.form.get('productRate'))
    qty=int(request.form.get('availableQuantity'))
    total=rate*qty
    cursor.execute('insert into sales(productID,product,Productname,rate,quantity) values(%s,%s,%s,%s,%s) on duplicate key update quantity=quantity+%s',(proid,product,item,rate,qty,qty))
    cursor.execute('update productdetails set avl=avl-%s where productid=%s',(qty,proid))
    # on duplicate key update total=total+%s
    cursor.execute('SELECT * FROM productdetails')
    data = cursor.fetchall()
    mysql.connection.commit()
    
    print(total)
    return render_template('sales.html',output_data=data)

@app.route('/finish',methods = ['POST', 'GET'])
def finish():
    cursor=mysql.connection.cursor()
    proid=request.form.get('productID')
    product=request.form.get('productName')
    item=request.form.get('item')
    rate=int(request.form.get('productRate'))
    qty=int(request.form.get('availableQuantity'))
    cursor.execute('insert into sales(productID,product,Productname,rate,quantity) values(%s,%s,%s,%s,%s) on duplicate key update quantity=quantity+%s',(proid,product,item,rate,qty,qty))
    cursor.execute('update productdetails set avl=avl-%s where productid=%s',(qty,proid))
    cursor.execute('SELECT * FROM productdetails')
    data = cursor.fetchall()
    mysql.connection.commit()
    return render_template('bill.html',output_data=data)

if __name__=="__main__":
    app.run(debug==True)
