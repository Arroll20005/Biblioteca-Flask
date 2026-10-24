
// PARA MOSTRAR MENSAJE DE CONFIRMACION DE DELETE
const btnDelete = document.querySelectorAll('.btn-delete')

if (btnDelete){
    const btnArray = Array.from(btnDelete);
    btnArray.forEach((btn) =>{
        btn.addEventListener('click', (e) =>{
            if (!confirm('Estas seguro de querer eliminar?')){
                e.preventDefault();
            }
        });
    });
}

// PARA TABLA EJEMPLAR
// AL SELECCIONE EL TITULO DEL LIBRO SE CONSULTA LA PROXIMA COPIA A PRODUCIRSE
// PARA MANTENER UN ORDEN EN LA CREACION DE COPIAS DE LIBROS
document.addEventListener('DOMContentLoaded', () => {

    const libro = document.getElementById('libro_id');
    const siguienteCopia = document.getElementById('siguiente_copia');

    if (!libro || !siguienteCopia) {
        return;
    }

    libro.addEventListener('change', function () {

        const libroId = this.value;

        if (!libroId) {
            siguienteCopia.value = 'Seleccione un libro';
            return;
        }

        fetch(`/get_next_copy/${libroId}`)
            .then(response => response.json())
            .then(data => {
                siguienteCopia.value =
                    `Copia #${data.siguiente_copia}`;
            })
            .catch(error => {
                console.error(error);
                siguienteCopia.value = 'Error al consultar';
            });

    });

});