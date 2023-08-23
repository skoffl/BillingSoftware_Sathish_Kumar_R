from flask import Flask, render_template, request
from flask_mysqldb import MySQL

app=Flask(__name__)
app.config['MYSQL_HOST']='localhost'
app.config['MYSQL_USER']='root'
app.config['MYSQL_PASSWORD']=''
app.config['MYSQL_DB']='user'

mysql=MySQL(app)
@app.route('/')
def h():
    return render_template('login.html')

@app.route('/login' ,methods = ['POST', 'GET'])
def user():
    return render_template('new6.html')

@app.route('/submit', methods = ['POST', 'GET'])
def login():
    if request.method == 'GET':
        return "Login via the login Form"
     
    if request.method == 'POST':
        cursor = mysql.connection.cursor()
        company = (request.form.get('companyName'))
        product = request.form.get('productName')
        proid=request.form.get('productID')
        item = request.form.get('item')
        rate = int(request.form.get('productRate'))
        quantity = int(request.form.get('availableQuantity'))
        print((company,product,rate,quantity,proid))
        
        # cursor.execute("select * from productdetails where productid=%s",(proid))
        # x=cursor.fetchall()

        # if not x:
        #     cursor.execute('insert into productdetails (Company,product,Productname,productID,rate,quantity) values(%s,%s,%s,%s,%s,%s)',(company,product,item,proid,int(rate),int(quantity)))
        #     mysql.connection.commit()
        # else:
        #     cursor.execute('update productdetails set avl=avl+%s where productid=%s',(quantity,proid))
        #     mysql.connection.commit()
        cursor.execute('insert into productdetails(Company,product,Productname,productID,rate,quantity,avl) values(%s,%s,%s,%s,%s,%s,%s) on duplicate key update avl=avl+%s',(company,product,item,proid,rate,quantity,quantity,quantity))
        cursor.execute('insert into sales(productID,product,Productname,rate,quantity) values(%s,%s,%s,%s,%s) on duplicate key update quantity=quantity+%s',(proid,product,item,rate,quantity,quantity))
        #'insert into user (Company,product,rate,quantity) values(%s,%s,%s,%s)',(company,product,int(rate),int(quantity))
        # cursor.execute('update amount set cash=cash-%s',(val))
        cursor.execute('SELECT * FROM productdetails')
        data = cursor.fetchall()
        mysql.connection.commit()
        cursor.close()
        return render_template('example.html', output_data = data)

if __name__=="__main__":
    app.debug = True
    app.run()