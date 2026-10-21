from flask import Flask, render_template
from flask_mysqldb import MySQL



app = Flask(__name__)
app.config['MYSQL_HOST']= 'localhost'
app.config['MYSQL_USER']= ''
app.config['MYSQL_PASSWORD']= ''
app.config['MYSQL_DB']= ''
mysql= MySQL()


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add-autor', method=['POST'])
def add_book():
    return 'book'

@app.route('/update-autor')
def add_book():
    return 'book'

@app.route('/delete-autor')
def add_book():
    return 'book'




@app.route('/add-book')
def add_book():
    return 'book'

@app.route('/update-book')
def add_book():
    return 'book'

@app.route('/delete-book')
def add_book():
    return 'book'


if __name__ == 'main': 
    app.run(port = 3000, debug= True)
