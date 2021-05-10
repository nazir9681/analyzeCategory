from flask import Flask, render_template, flash, Response, redirect, url_for
from werkzeug.utils import secure_filename
import math
import os
import random
from flask import request, jsonify
from flaskext.mysql import MySQL
mysql = MySQL()

app = Flask(__name__)


app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
path = os.getcwd()
UPLOAD_FOLDER = os.path.join(path, 'static/uploads')

if not os.path.isdir(UPLOAD_FOLDER):
    os.mkdir(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

baseUrl = 'http://127.0.0.1:5000/static/uploads/'
app.secret_key = "secret key"
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = '!@#123Qwe'
app.config['MYSQL_DATABASE_DB'] = 'mahattatest'

mysql = MySQL(app)

@app.route('/')
def home():
   return render_template('index.html')

@app.route('/insertCategory', methods=['POST'])
def insertCategory():
   response = {}
   response['status'] = 'false'
   if request.method == "POST":

      # flash("Data Inserted Successfully")
      categoryname = request.form['categoryname']
      categorytitle = request.form['categorytitle']
      cur = mysql.get_db().cursor()
      cur.execute("INSERT INTO category (categoryname, categorytitle) VALUES (%s, %s)", (categoryname, categorytitle))
      mysql.get_db().commit()
      cur.close()
      response['status']= 'true'
   return response

@app.route('/categoryPagination', methods=['POST'])
def categoryPagination():
   limit = 5
   if request.method == "POST":
      if request.form['page_no']:
         page_no = request.form['page_no']
      else:
         page_no = 1

   page_no = int(page_no)
   offset = (page_no-1) * limit

   cur = mysql.get_db().cursor()
   cur.execute("SELECT  * FROM category LIMIT %s, %s",(offset,limit))
   data = cur.fetchall()
   cur.close()

   curpag = mysql.get_db().cursor()
   num_rows = curpag.execute("SELECT  * FROM category")
   curpag.close()

   output1="<table class='table text-center'><thead><tr><th scope='col'>ID</th><th scope='col'>Category</th><th scope='col'>Title</th><th scope='col'>Subcategory</th><th scope='col'>Action</th></tr></thead><tbody>"
   output2 = ""
   for row in data:
      output2= output2 + " " +"<tr><td>{id:}</td><td>{category:}</td><td>{title:}</td><td><a href='/subcategory/{category:}/{id:}'>Subcategory</a></td><td><button type='button' class='btn btn-danger' onclick='deleteCategory({id:})'>Delete</button></td></tr>".format(id=row[0], category=row[1], title=row[2])
   output3="</tbody></table>"

   totalPage = math.ceil(num_rows/limit)

   output4="<ul class='pagination justify-content-center' style='margin:20px 0'>"

   output5 = ""
   for x in range(1, totalPage+1):
      if x == page_no:
         active = "active"
      else:
         active = ""
      output5= output5 + " " +"<li class='page-item {active:}'><a class='page-link' id='{i:}' href=''>{i:}</a></li>".format(active=active, i=x)
   

   output = output1 + output2 + output3 + output4 + output5
   return output

@app.route('/subcategoryPagination', methods=['POST'])
def subcategoryPagination():
   limit = 5
   if request.method == "POST":
      catid = request.form['id']
      categoryname = request.form['categoryname']
      if request.form['page_no']:
         page_no = request.form['page_no']
      else:
         page_no = 1

   page_no = int(page_no)
   offset = (page_no-1) * limit

   cur = mysql.get_db().cursor()
   cur.execute("SELECT  * FROM subcategory WHERE categoryid=%s LIMIT %s, %s",(catid,offset,limit))
   data = cur.fetchall()
   cur.close()

   curpag = mysql.get_db().cursor()
   num_rows = curpag.execute("SELECT  * FROM subcategory WHERE categoryid=%s",(catid))
   curpag.close()
   
   output1 = "<table class='table text-center my-5'><thead><tr><th scope='col'>ID</th><th scope='col'>SubCategory</th><th scope='col'>SubTitle</th><th scope='col'>Products</th><th scope='col'>Action</th></tr></thead><tbody>"
   output2 = ""
   for row in data:
      output2= output2 + " " +"<tr><td>{id:}</td><td>{subcategory:}</td><td>{subtitle:}</td><td><a href='/products/{catName:}/{subcategory:}/{catId:}/{id:}'> Products</a></td><td><button type='button' class='btn btn-danger' onclick='deleteSubcategory({id:})'>Delete</button></td></tr>".format(id=row[0], subcategory=row[1], subtitle=row[2], catName=categoryname, catId=catid)
   
   output3="</tbody></table>"

   totalPage = math.ceil(num_rows/limit)

   output4="<ul class='pagination justify-content-center' style='margin:20px 0'>"

   output5 = ""
   for x in range(1, totalPage+1):
      if x == page_no:
         active = "active"
      else:
         active = ""
      output5= output5 + " " +"<li class='page-item {active:}'><a class='page-link' id='{i:}' href=''>{i:}</a></li>".format(active=active, i=x)
   

   output = output1 + output2 + output3 + output4 + output5
   return output

@app.route('/productPagination', methods=['POST'])
def productPagination():
   limit = 5
   if request.method == "POST":
      catid = request.form['catid']
      subid = request.form['subid']
      if request.form['page_no']:
         page_no = request.form['page_no']
      else:
         page_no = 1

   page_no = int(page_no)
   offset = (page_no-1) * limit

   cur = mysql.get_db().cursor()
   cur.execute("SELECT  * FROM products WHERE catid=%s AND subid=%s LIMIT %s, %s",(catid,subid,offset,limit))
   data = cur.fetchall()
   cur.close()

   curpag = mysql.get_db().cursor()
   num_rows = curpag.execute("SELECT  * FROM products WHERE catid=%s AND subid=%s",(catid,subid))
   curpag.close()

   output1 = "<table class='table text-center'><thead><tr><th scope='col'>ID</th><th scope='col'>Name</th><th scope='col'>Price</th><th scope='col'>Product Images</th><th scope='col'>Action</th></tr></thead><tbody id='table-data'>"
   output2 = ""
   for row in data:
      output2 = output2 + " " +"<tr><td>{id:}</td><td>{name:}</td><td>{price:}</td><td><button type='button' class='btn btn-primary' onclick='seeImages({id:})'>All Images</button></td><td><button type='button' class='btn btn-danger' onclick='deleteProduct({id:})'>Delete</button></td></tr>".format(id=row[0], name=row[1], price=row[2])

   output3="</tbody></table>"

   totalPage = math.ceil(num_rows/limit)

   output4="<ul class='pagination justify-content-center' style='margin:20px 0'>"

   output5 = ""
   for x in range(1, totalPage+1):
      if x == page_no:
         active = "active"
      else:
         active = ""
      output5= output5 + " " +"<li class='page-item {active:}'><a class='page-link' id='{i:}' href=''>{i:}</a></li>".format(active=active, i=x)
   

   output = output1 + output2 + output3 + output4 + output5
   return output

@app.route('/subcategory/<catname>/<int:id>')
def subcategory(catname,id):
   context= {}

   cur = mysql.get_db().cursor()
   cur.execute("SELECT  * FROM subcategory WHERE categoryid=%s",id)
   data = cur.fetchall()
   cur.close()
   
   # print(id)
   context['catId'] = id
   context['catName'] = catname
   context['subcatdata'] = data
   return render_template('subcategory.html',context=context)

@app.route('/insertSubcategory', methods=['POST'])
def insertSubcategory():
   response = {}
   response['status'] = 'false'
   if request.method == "POST":

   #   flash("Data Inserted Successfully")
      subcategoryname = request.form['subcategoryname']
      subcategorytitle = request.form['subcategorytitle']
      categoryid = request.form['categoryid']
      cur = mysql.get_db().cursor()
      cur.execute("INSERT INTO subcategory (subcategoryname, subcategorytitle, categoryid) VALUES (%s, %s, %s)", (subcategoryname, subcategorytitle, categoryid))
      mysql.get_db().commit()
      cur.close()
      response['status']= 'true'

   return response

@app.route('/products/<catname>/<subcatname>/<int:catid>/<int:subid>')
def products(catname,subcatname,catid,subid):
   context= {}
   context['catId'] = catid
   context['subcatId'] = subid
   context['catName'] = catname
   context['subcatName'] = subcatname
   return render_template('product.html',context=context)

@app.route('/insertProduct', methods=['GET','POST'])
def insertProduct():
   if request.method == 'POST':
      name = request.form['name']
      price = request.form['price']
      catid = request.form['catid']
      subid = request.form['subid']

      if 'files[]' not in request.files:
         data = 'No file part'
         return data

      files = request.files.getlist('files[]')

      for check in files:
         if check and allowed_file(check.filename):
            data = "success"
         else :
            data = "failure"

      if data == "success":
         cur = mysql.get_db().cursor()
         cur.execute("INSERT INTO products (name, price, catid, subid) VALUES (%s, %s, %s, %s)", (name, price, catid, subid))
         mysql.get_db().commit()
         lastId = cur.lastrowid
         cur.close()
      
      else:
         data = "file type not allowed"
         return data

      for file in files:
         
         if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filename = str(random.randint(1111,9999)) + filename
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            cur = mysql.get_db().cursor()
            cur.execute("INSERT INTO productimages (productid, images, catid, subid) VALUES (%s, %s, %s, %s)", (lastId, filename, catid, subid))
            mysql.get_db().commit()
            cur.close()

      referrer = request.referrer
      return redirect(referrer)

@app.route('/productImages', methods=['POST'])
def productImages():
   if request.method == "POST":
      id = request.form['id']

   cur = mysql.get_db().cursor()
   cur.execute("SELECT  * FROM productimages WHERE productid=%s",(id))
   data = cur.fetchall()
   cur.close()

   output1 = "<div class='modal fade' id='exampleModal' tabindex='1' role='dialog' aria-labelledby='exampleModalLabel' s><div class='modal-dialog' role='document'><div class='modal-content'><div class='modal-header'><h5 class='modal-title' id='exampleModalLabel'>Product Images</h5><button type='button' class='close' data-dismiss='modal' aria-label='Close'><span aria-hidden='true'>&times;</span></button></div><div class='modal-body'>"

   output2 = ""
   for row in data:
      output2 = output2 + " " +"<img src='{url:}' height='100' width='100'>".format(url=baseUrl + row[2])


   output3 =  "</div><div class='modal-footer'><button type='button' class='btn btn-secondary' data-dismiss='modal'>Close</button></div></div></div></div>"

   output = output1 + output2 + output3
   allt = "<button type='button' class='btn btn-primary' data-toggle='modal' data-target='#exampleModal' data-whatever='@mdo'>tre</button>"
   return output

@app.route('/removeproducts', methods=['POST'])
def removeproducts():
   response = {}

   if request.method == "POST":
      productid = request.form['id']

   cur = mysql.get_db().cursor()
   cur.execute("SELECT  * FROM productimages WHERE productid=%s",(productid))
   data = cur.fetchall()
   cur.close()

   for row in data:
      os.unlink(os.path.join(app.config['UPLOAD_FOLDER'],row[2]))

   cur = mysql.get_db().cursor()
   cur.execute("DELETE FROM productimages WHERE productid=%s",(productid))
   mysql.get_db().commit()
   cur.close()

   cur = mysql.get_db().cursor()
   cur.execute("DELETE FROM products WHERE id=%s",(productid))
   mysql.get_db().commit()
   cur.close()
   response['status']= 'true'

   return response

@app.route('/removesubCategory', methods=['POST'])
def removesubCategory():
   response = {}

   if request.method == "POST":
      subid = request.form['id']

   cur = mysql.get_db().cursor()
   cur.execute("SELECT  * FROM productimages WHERE subid=%s",(subid))
   data = cur.fetchall()
   cur.close()

   for row in data:
      os.unlink(os.path.join(app.config['UPLOAD_FOLDER'],row[2]))

   cur = mysql.get_db().cursor()
   cur.execute("DELETE FROM productimages WHERE subid=%s",(subid))
   mysql.get_db().commit()
   cur.close()

   cur = mysql.get_db().cursor()
   cur.execute("DELETE FROM products WHERE subid=%s",(subid))
   mysql.get_db().commit()
   cur.close()

   cur = mysql.get_db().cursor()
   cur.execute("DELETE FROM subcategory WHERE id=%s",(subid))
   mysql.get_db().commit()
   cur.close()

   response['status']= 'true'

   return response

@app.route('/removeCategory', methods=['POST'])
def removeCategory():
   response = {}

   if request.method == "POST":
      catid = request.form['id']

   cur = mysql.get_db().cursor()
   cur.execute("SELECT  * FROM productimages WHERE catid=%s",(catid))
   data = cur.fetchall()
   cur.close()

   for row in data:
      os.unlink(os.path.join(app.config['UPLOAD_FOLDER'],row[2]))

   cur = mysql.get_db().cursor()
   cur.execute("DELETE FROM productimages WHERE catid=%s",(catid))
   mysql.get_db().commit()
   cur.close()

   cur = mysql.get_db().cursor()
   cur.execute("DELETE FROM products WHERE catid=%s",(catid))
   mysql.get_db().commit()
   cur.close()

   cur = mysql.get_db().cursor()
   cur.execute("DELETE FROM subcategory WHERE categoryid=%s",(catid))
   mysql.get_db().commit()
   cur.close()

   cur = mysql.get_db().cursor()
   cur.execute("DELETE FROM category WHERE id=%s",(catid))
   mysql.get_db().commit()
   cur.close()

   response['status']= 'true'

   return response

if __name__ == '__main__':
   app.run(debug = True)