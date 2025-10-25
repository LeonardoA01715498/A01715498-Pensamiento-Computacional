function cerrar(event){
    event.target.closest(".persona").style.display="none";
}
document.addEventListener('DOMContentLoaded', () => {
    const mensajeExito = document.getElementById('mensajeExito');
    const forms = document.querySelectorAll('form');

    forms.forEach(form => {
        form.addEventListener('submit', function(event) {
            event.preventDefault();
            console.log("Formulario enviado, iniciando proceso AJAX...");

            const currentForm = event.target;

            
            // 1. Identificar el div.display
            const displayDiv = currentForm.querySelector('.display');
            
            // 2. Identificar el contenedor padre que queremos ocultar (div.personaX)
            // Usamos .closest() para encontrar el ancestro más cercano que tenga una clase 
            // que empiece con "persona" (persona1, persona2, etc.)
            const contenedorEvento = displayDiv ? displayDiv.closest('div[class^="persona"]') : null;

            // ... (Resto del código para obtener el botón y el formData) ...
            
            const submitButton = document.activeElement;
            const formData = new FormData(currentForm);
            
            if (submitButton && submitButton.name === 'hora' && submitButton.value) {
                formData.append(submitButton.name, submitButton.value);
            } else {
                console.error("No se pudo obtener el valor del botón 'hora' para AJAX.");
                alert("Error interno: No se detectó la hora para enviar.");
                return;
            }

            // 4. Enviar los datos del formulario a Flask
            fetch(currentForm.action, {
                method: currentForm.method, 
                body: formData
            })
            .then(response => {
                if (response.ok) {
                    
                    // 3. ¡CAMBIO CLAVE! Ocultar el bloque del evento completo (div.personaX)
                    if (contenedorEvento) {
                        contenedorEvento.classList.add('persona-oculta'); // Esto oculta el div.personaX
                    }

                    // Mostrar el mensaje de éxito
                    mensajeExito.classList.remove('hidden');
                    
                    setTimeout(() => {
                        mensajeExito.classList.add('hidden');
                        
                        // Recarga la página para mostrar los datos actualizados
                        window.location.reload();
                    }, 3000); 
                    
                } else {
                    // Manejar errores de Flask (400, 500)
                    console.error('Error al guardar el evento. Código:', response.status);
                    alert('Error al guardar el evento. Revisa la consola de Flask.');
                }
            })
            .catch(error => {
                console.error('Error de red:', error);
                alert('Error de conexión.');
            });
        });
    });
});