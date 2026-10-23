from flask import Flask, render_template, request, url_for, redirect, flash
from flask_mysqldb import MySQL



app = Flask(__name__)
# Conexion de bd
app.config['MYSQL_HOST']= ''
app.config['MYSQL_USER']= ''
app.config['MYSQL_PASSWORD']= ''
app.config['MYSQL_DB']= ''
mysql= MySQL(app)

# seetings
app.secret_key = 'mysecretkey'

@app.route('/usuario')
def indexusuario():
    cur = mysql.connection.cursor()
    cur.execute('select * from usuario')
    data = cur.fetchall()
    return render_template('usuario.html', usuario = data)

@app.route('/add_usuario', methods=['POST'])
def add_usuario():
    if request.method == 'POST':
        # strip para evitar errores de espaciado
        nombre = request.form['nombre'].strip()
        apellido = request.form['apellido'].strip()
        email = request.form['email'].strip()
        # Validacion para evitar campos vacios
        if not nombre or not apellido or not email:
            flash('Todos los campos son obligatorios')
            return redirect(url_for('indexusuario'))

        cur = mysql.connection.cursor()
        cur.execute('insert into usuario (nombre, apellido, email) values (%s, %s, %s)', (nombre, apellido, email))
        mysql.connection.commit()
        flash('Usuario agregado correctamente')
        
        return redirect(url_for('indexusuario'))
        
@app.route('/edit_usuario/<id>')
def get_usuario(id):
    cur = mysql.connection.cursor()
    cur.execute('select * from usuario where usuario_id = %s', (id,))
    data = cur.fetchall()

    return render_template('edit-usuario.html', usuario = data[0])

@app.route('/update_usuario/<id>', methods = ['POST'])
def update_usuario(id):
    if request.method == 'POST':
        nombre = request.form['nombre'].strip()
        apellido = request.form['apellido'].strip()
        email = request.form['email'].strip()
        if not nombre or not apellido or not email:
            flash('Todos los campos son obligatorios')
            return redirect(url_for('indexusuario'))

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
        return redirect(url_for('indexusuario'))


@app.route('/delete_usuario/<string:id>')
def delete_usuario(id): 
    cur = mysql.connection.cursor()
    cur.execute('delete from usuario where usuario_id = %s', (id,))
    mysql.connection.commit()
    flash('Usuario eliminado correctamente')
    return redirect(url_for('indexusuario'))

@app.route('/autor')
def indexautor():
    cur = mysql.connection.cursor()
    cur.execute('select * from autor')
    data = cur.fetchall()
    return render_template('autor.html', autor = data)

@app.route('/add_autor', methods=['POST'])
def add_autor():
        nombre = request.form['nombre'].strip()
        apellido = request.form['apellido'].strip()
        nacionalidad = request.form['nacionalidad'].strip()
        if not nombre or not apellido or not nacionalidad:
            flash('Todos los campos son obligatorios')
            return redirect(url_for('indexautor'))

        cur = mysql.connection.cursor()
        cur.execute('insert into autor (nombre, apellido, nacionalidad) values (%s, %s, %s)', (nombre, apellido, nacionalidad))
        mysql.connection.commit()
        flash('Autor agregado correctamente')
        return redirect(url_for('indexautor'))

@app.route('/edit_autor/<id>')
def get_autor(id):
    cur = mysql.connection.cursor()
    cur.execute('select * from autor where autor_id = %s', (id,))
    data = cur.fetchall()
    return render_template('edit-autor.html', autor = data[0])

@app.route('/update_autor/<id>', methods = ['POST'])
def update_autor(id):
    nombre = request.form['nombre'].strip()
    apellido = request.form['apellido'].strip()
    nacionalidad = request.form['nacionalidad'].strip()
    if not nombre or not apellido or not nacionalidad:
        flash('Todos los campos son obligatorios')
        return redirect(url_for('indexautor'))

    cur = mysql.connection.cursor()
    cur.execute("""
        update autor
        set nombre = %s,
            apellido = %s,
            nacionalidad = %s
        where autor_id = %s
    """, (nombre, apellido, nacionalidad, id))
    mysql.connection.commit()
    flash('Autor actualizado correctamente')
    return redirect(url_for('indexautor'))

@app.route('/delete_autor/<string:id>')
def delete_autor(id):
    cur = mysql.connection.cursor()
    cur.execute('delete from autor where autor_id = %s', (id,))
    mysql.connection.commit()
    flash('Autor eliminado correctamente')
    return redirect(url_for('indexautor'))




if __name__ == '__main__': 
    app.run(port = 3000, debug= True)
