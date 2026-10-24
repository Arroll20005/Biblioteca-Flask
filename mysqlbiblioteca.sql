create database flaskbiblioteca;
use flaskbiblioteca;

create table usuario (
usuario_id int auto_increment primary key,
nombre varchar(100) not null,
apellido varchar(100) not null,
email varchar(100) not null unique);

create table autor (
autor_id int auto_increment primary key,
nombre varchar(100) not null, 
apellido varchar(100) not null,
nacionalidad varchar(50));

create table libro(
libro_id int auto_increment primary key,
titulo varchar(255) not null,
anio_publicacion year,
autor_id int not null,
constraint fk_libro_autor
foreign key (autor_id)
references autor(autor_id)
on update cascade
on delete restrict);

create table ejemplar(
ejemplar_id int auto_increment primary key,
libro_id int not null,
num_copia int not null,
estado enum(
'Disponible',
'Prestado')
not null default 'Disponible',
constraint fk_ejemplar_libro
foreign key(libro_id)
references libro(libro_id)
on update cascade
on delete cascade,
constraint uq_libro_copia
unique (libro_id, num_copia));

create table prestamo (
prestamo_id int auto_increment primary key, 
usuario_id int not null,
ejemplar_id int not null, 
fecha_prestamo date not null,
fecha_devolucion date,
constraint fk_prestamo_usuario
foreign key (usuario_id)
references usuario(usuario_id)
on update cascade
on delete restrict,

constraint fk_prestamo_Ejemplar
foreign key (ejemplar_id)
references ejemplar(ejemplar_id)
on update cascade
on delete restrict,

constraint chk_fechas
check (
fecha_devolucion is null
or fecha_devolucion >= fecha_prestamo));


select * from usuario;
select * from autor;
select * from libro;
select * from ejemplar;
select * from prestamo;
d;

