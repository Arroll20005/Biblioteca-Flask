from flask import Flask, render_template, request, url_for, redirect, flash
from flask_mysqldb import MySQL
from MySQLdb import DataError



app = Flask(__name__)
# Conexion de bd
app.config['MYSQL_HOST']= ''
app.config['MYSQL_USER']= ''
app.config['MYSQL_PASSWORD']= ''
app.config['MYSQL_DB']= ''
mysql= MySQL(app)

# seetings
app.secret_key = 'mysecretkey'

# Temporal 
# Muestra tabla usuario hasta crear la vista principal
@app.route('/')
def index():
    cur = mysql.connection.cursor()
    cur.execute('select * from usuario')
    data = cur.fetchall()
    return render_template('usuario.html', usuario = data)

# ------------------------------------------------------------------------------------------------
# Tabla Usuario
@app.route('/usuario')
def indexusuario():
    cur = mysql.connection.cursor()
    cur.execute('select * from usuario')
    data = cur.fetchall()
    return render_template('usuario.html', usuario = data)

# AGREGA USUARIO
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

# EXTRAE DATOS DE USUARIO
@app.route('/edit_usuario/<id>')
def get_usuario(id):
    cur = mysql.connection.cursor()
    cur.execute('select * from usuario where usuario_id = %s', (id,))
    data = cur.fetchall()

    return render_template('edit-usuario.html', usuario = data[0])

# ACTUALIZA DATOS DE USUARIO
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

# ELIMINA USUARIO
@app.route('/delete_usuario/<string:id>')
def delete_usuario(id): 
    cur = mysql.connection.cursor()
    cur.execute('delete from usuario where usuario_id = %s', (id,))
    mysql.connection.commit()
    flash('Usuario eliminado correctamente')
    return redirect(url_for('indexusuario'))

# ------------------------------------------------------------------------------------------------
# TABLA AUTOR
@app.route('/autor')
def indexautor():
    cur = mysql.connection.cursor()
    cur.execute('select * from autor')
    data = cur.fetchall()
    return render_template('autor.html', autor = data)

# AGREGA AUTOR
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

# EXTRAE DATOS DE AUTOR
@app.route('/edit_autor/<id>')
def get_autor(id):
    cur = mysql.connection.cursor()
    cur.execute('select * from autor where autor_id = %s', (id,))
    data = cur.fetchall()
    return render_template('edit-autor.html', autor = data[0])

# ACTUALIZA AUTOR
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

# ELIMINA AUTOR
@app.route('/delete_autor/<string:id>')
def delete_autor(id):
    cur = mysql.connection.cursor()
    cur.execute('delete from autor where autor_id = %s', (id,))
    mysql.connection.commit()
    flash('Autor eliminado correctamente')
    return redirect(url_for('indexautor'))

# ------------------------------------------------------------------------------------------------
# TABLA LIBRO
@app.route('/libro')
def indexlibro():
    cur = mysql.connection.cursor()
    cur.execute("""
        select l.libro_id,
            l.titulo,
            l.anio_publicacion,
            a.nombre,
            a.apellido
        from libro l
        inner join autor a
            on l.autor_id = a.autor_id
    """)
    datalibro = cur.fetchall()

    cur.execute("""
        select autor_id,
            nombre,
            apellido
        from autor
    """)
    dataautor = cur.fetchall()
    return render_template('libro.html', libro = datalibro, autor = dataautor)

# AGREGA LIBRO
@app.route('/add_libro', methods=['POST'])
def add_libro():
    titulo = request.form['titulo'].strip()
    anio_publicacion = request.form['anio_publicacion'].strip()
    autor_id = request.form['autor_id'].strip()
    if not titulo or not anio_publicacion or not autor_id:
        flash('Todos los campos son obligatorios')
        return redirect(url_for('indexlibro'))
    # Controlardor de error para año ingresado
    try:
        cur = mysql.connection.cursor()
        cur.execute('insert into libro (titulo, anio_publicacion, autor_id) values (%s, %s, %s)', (titulo, anio_publicacion, autor_id))
        mysql.connection.commit()
        flash('Libro agregado correctamente', 'success')
    except DataError:
        flash('El año ingresado no es válido', 'danger')
    
    return redirect(url_for('indexlibro'))

# EXTRAE DATOS DE LIBRO
@app.route('/edit_libro/<id>')
def get_libro(id):
    cur = mysql.connection.cursor()
    cur.execute('select * from libro where libro_id =%s', (id,))
    datalibro = cur.fetchone()
    cur.execute('select * from autor')
    dataautor = cur.fetchall()

    return render_template('edit-libro.html', libro = datalibro, autor = dataautor)

# ACTUALIZA LIBRO
@app.route('/update_libro/<id>', methods = ['POST'])
def update_libro(id):
    titulo = request.form['titulo'].strip()
    anio_publicacion = request.form['anio_publicacion'].strip()
    autor_id = request.form['autor_id'].strip()
    if not titulo or not anio_publicacion or not autor_id:
        flash('Todos los campos son obligatorios')
        return redirect(url_for('indexlibro'))
    # Controlardor de error para año ingresado
    try:
        cur = mysql.connection.cursor()
        cur.execute("""
            update libro
            set titulo = %s, 
                anio_publicacion = %s,
                autor_id = %s
            where libro_id = %s
        """, (titulo, anio_publicacion, autor_id, id))
        mysql.connection.commit()
        flash('Libro actualizado correctamente', 'success')
    except DataError:
        flash('El año ingresado no es valido', 'danger')
    return redirect(url_for('indexlibro'))

# ELIMINA LIBRO
@app.route('/delete_libro/<string:id>')
def delete_libro(id):
    cur = mysql.connection.cursor()
    cur.execute('delete from libro where libro_id = %s', (id,))
    mysql.connection.commit()
    flash('Libro eliminado correctamente', 'success')
    return redirect(url_for('indexlibro'))

# ------------------------------------------------------------------------------------------------
# TABLA EJEMPLAR
# RUTA PRINCIPAL DE EJEMPLAR
@app.route('/ejemplar')
def indexejemplar():
    cur = mysql.connection.cursor()
    cur.execute("""
        select e.ejemplar_id,
            l.titulo,
            e.num_copia,
            e.estado
        from ejemplar e
        inner join libro l
            on e.libro_id = l.libro_id
    """)
    dataejemplar = cur.fetchall()
    cur.execute("""
        select libro_id,
            titulo
        from libro
    """)
    datalibro = cur.fetchall()
    return render_template('ejemplar.html', ejemplar=dataejemplar, libro = datalibro)

# Metodo extra para obtener la proxima copia denum_copia
@app.route('/get_next_copy/<int:libro_id>')
def get_next_copy(libro_id):
    cur = mysql.connection.cursor()
    cur.execute("""
        select coalesce(max(num_copia), 0) +1
        from ejemplar
        where libro_id = %s
    """, (libro_id,))

    siguiente_copia = cur.fetchone()[0]
    return {
        'siguiente_copia': siguiente_copia
    }

# RUTA PARA AGREGAR EJEMPLAR
@app.route('/add_ejemplar', methods=['POST'])
def add_ejemplar():
    libro_id = request.form['libro_id'].strip()
    if not libro_id:
        flash('Todos los campos son obligatorios', 'warning')
        return redirect(url_for('indexejemplar'))
    # CONTROL DE ERRORES
    try:
        cur = mysql.connection.cursor()
        cur.execute("""
            select coalesce(max(num_copia), 0)
            from ejemplar
            where libro_id = %s
    """, (libro_id,))
        ultima_copia = cur.fetchone()[0]
        nueva_copia = ultima_copia+1
        cur.execute('insert into ejemplar (libro_id, num_copia) values(%s, %s)', (libro_id, nueva_copia))
        mysql.connection.commit()
        flash('Ejemplar agregado correctamente', 'success')
    except Exception:
        mysql.connection.rollback()
        flash('No se pudo registar el ejemplar', 'danger')
    return redirect(url_for('indexejemplar'))

# RUTA PARA OBTENER DATOS
@app.route('/edit_ejemplar/<id>')
def get_ejemplar(id):
    cur = mysql.connection.cursor()
    cur.execute("""
        select
            e.ejemplar_id,
            l.titulo,
            e.num_copia,
            e.estado
        from ejemplar e
        inner join libro l
            on e.libro_id = l.libro_id
        where e.ejemplar_id = %s
    """, (id,))
    dataejemplar = cur.fetchone()
    return render_template('edit-ejemplar.html', ejemplar = dataejemplar)

# RUTA PARA ACTUALIZAR
@app.route('/update_ejemplar/<id>', methods = ['POST'])
def update_ejemplar(id):
    estado = request.form['estado'].strip()
    if not estado:
        flash('Debe seleccionar un estado', 'warning')
        return redirect(url_for('indexejemplar'))

    try:
        cur = mysql.connection.cursor()
        cur.execute('update ejemplar set estado = %s where ejemplar_id = %s', (estado, id))
        mysql.connection.commit()
        flash('Estado actualizado correctamente', 'success')
    except Exception:
        # USO DE ROLLBACK PARA DESHACER CAMBIOS
        mysql.connection.rollback()
        flash('No se pudo actualizar', 'danger')
    return redirect(url_for('indexejemplar'))

# RUTA PARA ELIMINAR
@app.route('/delete_ejemplar/<string:id>')
def delete_ejemplar(id):
    try:
        cur = mysql.connection.cursor()
        cur.execute('delete from ejemplar where ejemplar_id = %s', (id,))
        mysql.connection.commit()
        flash('Ejemplar eliminado correctamente', 'success')
    except Exception:
        mysql.connection.rollback()
        flash('No se pudo eliminar', 'danger')
    return redirect(url_for('indexejemplar'))

# ------------------------------------------------------------------------------------------------
# TABLA PRESTAMO
@app.route('/prestamo')
def indexprestamo():
    cur = mysql.connection.cursor()
    cur.execute("""
        select p.prestamo_id,
            u.nombre,
            u.apellido,
            l.titulo,
            e.num_copia,
            p.fecha_prestamo,
            p.fecha_devolucion
        from prestamo p
        inner join usuario u
            on p.usuario_id = u.usuario_id
        inner join ejemplar e
            on p.ejemplar_id = e.ejemplar_id 
        inner join libro l
            on e.libro_id = l.libro_id
    """)
    dataprestamo = cur.fetchall()
    cur.execute("""
        select usuario_id,
            nombre, 
            apellido
        from usuario
    """)
    datausuario = cur.fetchall()
    # PARA MOSTRAR A QUE LIBRO PERTENECE Y EVITAR PRESTAMOS NO DISPONIBLES (ES DECIR QUE HAYAN SIDO PRESTADOS)
    cur.execute("""
        select e.ejemplar_id,
            l.titulo,
            e.num_copia
        from ejemplar e
        inner join libro l
            on e.libro_id = l.libro_id
        where e.estado = 'Disponible'
    """)
    dataejemplar = cur.fetchall()
    return render_template('prestamo.html', prestamo = dataprestamo, usuario = datausuario, ejemplar = dataejemplar)

# AGREGAR PRESTAMO
@app.route('/add_prestamo', methods=['POST'])
def add_prestamo():
    usuario_id = request.form['usuario_id'].strip()
    ejemplar_id = request.form['ejemplar_id'].strip()
    fecha_prestamo = request.form['fecha_prestamo'].strip()
    if not usuario_id or not ejemplar_id or not fecha_prestamo:
        flash('Todos los campos son obligatorios', 'warning')
        return redirect(url_for('indexprestamo'))

    try:
        cur = mysql.connection.cursor()
        cur.execute('insert into prestamo (usuario_id, ejemplar_id, fecha_prestamo) values (%s, %s, %s)', (usuario_id, ejemplar_id, fecha_prestamo))
        # ACTUALIZACION PARA ESTADO DEL EJEMPLAR
        cur.execute("""
            update ejemplar
            set estado = 'Prestado'
            where ejemplar_id = %s
        """, (ejemplar_id,))

        mysql.connection.commit()
        flash('Prestamo agregado correctamente', 'success')
    except Exception:
        mysql.connection.rollback()
        flash('No se pudo registrar el prestamo', 'danger')
    return redirect(url_for('indexprestamo'))

# EXTRAER PRESTAMO PARA ACTUALIZAR
@app.route('/edit_prestamo/<id>')
def get_prestamo(id):
    cur = mysql.connection.cursor()
    cur.execute("""
        select p.prestamo_id,
            p.ejemplar_id,
            u.nombre,
            u.apellido,
            l.titulo,
            e.num_copia,
            p.fecha_prestamo,
            p.fecha_devolucion
        from prestamo p
        inner join usuario u
            on p.usuario_id = u.usuario_id
        inner join ejemplar e
            on p.ejemplar_id = e.ejemplar_id
        inner join libro l
            on e.libro_id = l.libro_id
        where p.prestamo_id = %s
    """, (id,))
    dataprestamo = cur.fetchone()
    return render_template('edit-prestamo.html', prestamo = dataprestamo)

# ACTUALIZAR PRESTAMO
@app.route('/update_prestamo/<id>', methods = ['POST'])
def update_prestamo(id):
    fecha_devolucion = request.form['fecha_devolucion'].strip()
    ejemplar_id = request.form['ejemplar_id'].strip()
    if not fecha_devolucion:
        flash('Debe seleccionar una fecha', 'warning')
        return redirect(url_for('indexprestamo'))

    try:
        cur = mysql.connection.cursor()

        # CONSULTA PARA VALIDAD LA FECHA DE DEVOLUCION NO SEA MENOR A LA DEL PRESTAMO
        cur.execute("""
            select fecha_prestamo
            from prestamo
            where prestamo_id = %s
        """, (id,))
        fecha_prestamo = str(cur.fetchone()[0])

        if fecha_devolucion < fecha_prestamo:
            flash('La fecha de devolucion no puede ser menor que la fecha del préstamo', 'danger')
            return redirect(url_for('indexprestamo'))

        cur.execute('update prestamo set fecha_devolucion = %s where prestamo_id = %s', (fecha_devolucion, id))
        # PARA ACTUALIZAR EL ESTADO DEL EJEMPLAR
        cur.execute("""
            update ejemplar
            set estado = 'Disponible'
            where ejemplar_id = %s
        """, (ejemplar_id,))
        mysql.connection.commit()
        flash('Devolucion registrada correctamente', 'success')
    except Exception:
        mysql.connection.rollback()
        flash('No se pudo registrar la devolucion', 'danger')
    return redirect(url_for('indexprestamo'))

# ELIMINAR PRESTAMO
@app.route('/delete_prestamo/<string:id>')
def delete_prestamo(id):
    try:
        cur = mysql.connection.cursor()
        cur.execute("""
            select ejemplar_id
            from prestamo
            where prestamo_id = %s
        """, (id,))
        ejemplar_id = cur.fetchone()[0]

        # ACTUALIZA EL ESTADO DEL EJEMPLAR ANTES DEL ELIMINAR
        # POR SI NO SE HA DEVUELTO
        #PEQEUÑO MANEJO DE ERROR
        cur.execute("""
            update ejemplar
            set estado = 'Disponible'
            where ejemplar_id = %s
        """, (ejemplar_id,))

        # ELIMINA EL REGISTRO DEL PRESTAMO
        cur.execute('delete from prestamo where prestamo_id = %s', (id,))
        mysql.connection.commit()
        flash('Prestamos eliminado correctamente', 'success')
    except Exception:
        mysql.connection.rollback()
        flash('No se pudo eliminar el prestamo', 'danger')
    return redirect(url_for('indexprestamo'))


if __name__ == '__main__': 
    app.run(port = 3000, debug= True)
