from flask import Flask, render_template, request, url_for, redirect, flash
from flask_mysqldb import MySQL



app = Flask(__name__)
# Conexion de bd
app.config['MYSQL_HOST']= '127.0.0.1'
app.config['MYSQL_USER']= 'root'
app.config['MYSQL_PASSWORD']= '_Vlol0521'
app.config['MYSQL_DB']= 'flaskbiblioteca'
mysql= MySQL(app)

# seetings
app.secret_key = 'mysecretkey'

@app.route('/')
def index():
    cur = mysql.connection.cursor()
    cur.execute('select * from usuario')
    data = cur.fetchall()
    return render_template('index.html', usuario = data)

@app.route('/add_usuario', methods=['POST'])
def add_usuario():
    if request.method == 'POST':
        nombre = request.form['nombre'].strip()
        apellido = request.form['apellido'].strip()
        email = request.form['email'].strip()
        if not nombre or not apellido or not email:
            flash('Todos los campos son obligatorios')
            return redirect(url_for('index'))

        cur = mysql.connection.cursor()
        cur.execute('insert into usuario (nombre, apellido, email) values (%s, %s, %s)', (nombre, apellido, email))
        mysql.connection.commit()
        flash('Usuario agregado correctamente')
        
        return redirect(url_for('index'))
        
@app.route('/edit/<id>')
def get_usuario(id):
    cur = mysql.connection.cursor()
    cur.execute('select * from usuario where usuario_id = %s', (id,))
    data = cur.fetchall()

    return render_template('edit-usuario.html', usuario = data[0])

@app.route('/update/<id>', methods = ['POST'])
def update_usuario(id):
    if request.method == 'POST':
        nombre = request.form['nombre'].strip()
        apellido = request.form['apellido'].strip()
        email = request.form['email'].strip()
        if not nombre or not apellido or not email:
            flash('Todos los campos son obligatorios')
            return redirect(url_for('index'))

        cur = mysql.connection.cursor()
        cur.execute("""
            update usuario
            set nombre = %s,
                apellido = %s,
                email = %s
            where usuario_id =%s
        """, (nombre, apellido, email, id))
        mysql.connection.commit()
        flash('Usuario actualizado correctamente')
        return redirect(url_for('index'))



@app.route('/delete/<string:id>')
def delete_usuario(id): 
    cur = mysql.connection.cursor()
    cur.execute('delete from usuario where usuario_id = %s', (id,))
    mysql.connection.commit()
    flash('Usuario eliminado correctamente')
    return redirect(url_for('index'))


if __name__ == '__main__': 
    app.run(port = 3000, debug= True)
