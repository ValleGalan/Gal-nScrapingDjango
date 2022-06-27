//preguntar si esta seguro de eliminar el elemento
(function () {

    const btnEliminacion = document.querySelectorAll(".btnEliminacion");

    btnEliminacion.forEach(btn => {
        btn.addEventListener('click', (e) => {
            const confirmacion = confirm('¿Seguro de eliminar ?');
            if (!confirmacion) {
                e.preventDefault();
            }
        });
    });
    
})();
 