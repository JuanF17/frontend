document.addEventListener('DOMContentLoaded', function() {
    const solicitudForm = document.getElementById('solicitud-form');
    if (solicitudForm) {
        solicitudForm.addEventListener('submit', async function(e) {
            e.preventDefault();
            
            const formData = new FormData(this);
            
            try {
                const response = await fetch('/api/solicitar-credito/', {
                    method: 'POST',
                    body: formData
                });

                const result = await response.json();
                
                if (!response.ok) {
                    throw new Error(result.detail || 'Error al enviar la solicitud');
                }

                alert(`Solicitud enviada exitosamente. Su número de solicitud es: ${result.id}`);
                this.reset();
            } catch (error) {
                console.error('Error:', error);
                alert('Error al enviar la solicitud: ' + error.message);
            }
        });
    }

    // Función para mostrar el modal de agregar
    window.showAddModal = function() {
        document.getElementById('modalTitle').textContent = 'Agregar Celular';
        document.getElementById('celular-id').value = '';
        document.getElementById('celularForm').reset();
        document.getElementById('celularModal').style.display = 'block';
    }

    // Función para cerrar el modal
    window.closeModal = function() {
        document.getElementById('celularModal').style.display = 'none';
    }

    // Función para editar celular
    window.editarCelular = function(celularId) {
        const row = document.querySelector(`tr[data-id="${celularId}"]`);
        if (!row) return;

        document.getElementById('modalTitle').textContent = 'Editar Celular';
        document.getElementById('celular-id').value = celularId;
        
        // Llenar el formulario con los datos actuales
        const cells = row.cells;
        document.getElementById('marca').value = cells[1].textContent;
        document.getElementById('modelo').value = cells[2].textContent;
        document.getElementById('precio').value = cells[3].textContent.replace('$', '');
        document.getElementById('stock').value = cells[4].textContent;
        document.getElementById('pantalla').value = cells[5].textContent;
        document.getElementById('procesador').value = cells[6].textContent;
        document.getElementById('ram').value = cells[7].textContent;
        document.getElementById('almacenamiento').value = cells[8].textContent;
        document.getElementById('camara').value = cells[9].textContent;

        document.getElementById('celularModal').style.display = 'block';
    }

    // Función para eliminar celular
    window.eliminarCelular = async function(celularId) {
        if (!confirm('¿Está seguro de eliminar este celular?')) return;

        try {
            const response = await fetch(`/api/celulares/${celularId}`, {
                method: 'DELETE'
            });

            if (!response.ok) {
                const error = await response.json();
                throw new Error(error.detail || 'Error al eliminar el celular');
            }

            // Eliminar la fila de la tabla
            const row = document.querySelector(`tr[data-id="${celularId}"]`);
            if (row) row.remove();

            alert('Celular eliminado correctamente');
        } catch (error) {
            console.error('Error:', error);
            alert(error.message);
        }
    }

    // Manejar el envío del formulario
    document.getElementById('celularForm').addEventListener('submit', async function(e) {
        e.preventDefault();

        const celularId = document.getElementById('celular-id').value;
        const data = {
            marca: document.getElementById('marca').value,
            modelo: document.getElementById('modelo').value,
            precio: parseFloat(document.getElementById('precio').value),
            stock: parseInt(document.getElementById('stock').value),
            pantalla: document.getElementById('pantalla').value,
            procesador: document.getElementById('procesador').value,
            ram: document.getElementById('ram').value,
            almacenamiento: document.getElementById('almacenamiento').value,
            camara: document.getElementById('camara').value
        };

        try {
            const url = celularId ? 
                `/api/celulares/${celularId}` : 
                '/api/celulares/';
            
            const response = await fetch(url, {
                method: celularId ? 'PUT' : 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(data)
            });

            if (!response.ok) {
                const error = await response.json();
                throw new Error(error.detail || 'Error al procesar la solicitud');
            }

            const responseData = await response.json();

            if (celularId) {
                // Actualizar la fila existente
                const row = document.querySelector(`tr[data-id="${celularId}"]`);
                if (row) {
                    row.cells[1].textContent = data.marca;
                    row.cells[2].textContent = data.modelo;
                    row.cells[3].textContent = `$${data.precio.toFixed(2)}`;
                    row.cells[4].textContent = data.stock;
                    row.cells[5].textContent = data.pantalla;
                    row.cells[6].textContent = data.procesador;
                    row.cells[7].textContent = data.ram;
                    row.cells[8].textContent = data.almacenamiento;
                    row.cells[9].textContent = data.camara;
                }
            } else {
                // Agregar nueva fila
                const tbody = document.querySelector('#celulares-table tbody');
                const newRow = tbody.insertRow();
                newRow.setAttribute('data-id', responseData.id);
                
                newRow.innerHTML = `
                    <td>${responseData.id}</td>
                    <td>${data.marca}</td>
                    <td>${data.modelo}</td>
                    <td>$${data.precio.toFixed(2)}</td>
                    <td>${data.stock}</td>
                    <td>${data.pantalla}</td>
                    <td>${data.procesador}</td>
                    <td>${data.ram}</td>
                    <td>${data.almacenamiento}</td>
                    <td>${data.camara}</td>
                    <td class="action-buttons">
                        <button class="edit-btn" onclick="editarCelular('${responseData.id}')">Editar</button>
                        <button class="delete-btn" onclick="eliminarCelular('${responseData.id}')">Eliminar</button>
                    </td>
                `;
            }

            alert(celularId ? 'Celular actualizado correctamente' : 'Celular agregado correctamente');
            closeModal();
        } catch (error) {
            console.error('Error:', error);
            alert(error.message);
        }
    });

    // Agregar estas funciones para el CRUD de clientes

    // Función para mostrar el modal de agregar cliente
    window.showAddClienteModal = function() {
        document.getElementById('clienteModalTitle').textContent = 'Agregar Cliente';
        document.getElementById('cliente-id').value = '';
        document.getElementById('clienteForm').reset();
        document.getElementById('clienteModal').style.display = 'block';
    }

    // Función para cerrar el modal de cliente
    window.closeClienteModal = function() {
        document.getElementById('clienteModal').style.display = 'none';
    }

    // Función para editar cliente
    window.editarCliente = function(clienteId) {
        const row = document.querySelector(`#clientes-table tr[data-id="${clienteId}"]`);
        if (!row) return;

        document.getElementById('clienteModalTitle').textContent = 'Editar Cliente';
        document.getElementById('cliente-id').value = clienteId;
        
        // Llenar el formulario con los datos actuales
        const cells = row.cells;
        document.getElementById('nombre').value = cells[1].textContent;
        document.getElementById('apellido').value = cells[2].textContent;
        document.getElementById('dni').value = cells[3].textContent;
        document.getElementById('email').value = cells[4].textContent;
        document.getElementById('telefono').value = cells[5].textContent;
        document.getElementById('direccion').value = cells[6].textContent;
        document.getElementById('historial_crediticio').value = cells[7].textContent !== 'N/A' ? 
            cells[7].textContent : '';

        document.getElementById('clienteModal').style.display = 'block';
    }

    // Función para eliminar cliente
    window.eliminarCliente = async function(clienteId) {
        if (!confirm('¿Está seguro de eliminar este cliente?')) return;

        try {
            const response = await fetch(`/api/clientes/${clienteId}`, {
                method: 'DELETE'
            });

            if (!response.ok) {
                const error = await response.json();
                throw new Error(error.detail || 'Error al eliminar el cliente');
            }

            // Eliminar la fila de la tabla
            const row = document.querySelector(`#clientes-table tr[data-id="${clienteId}"]`);
            if (row) row.remove();

            alert('Cliente eliminado correctamente');
        } catch (error) {
            console.error('Error:', error);
            alert(error.message);
        }
    }

    // Manejar el envío del formulario de cliente
    document.getElementById('clienteForm').addEventListener('submit', async function(e) {
        e.preventDefault();

        const clienteId = document.getElementById('cliente-id').value;
        const data = {
            nombre: document.getElementById('nombre').value,
            apellido: document.getElementById('apellido').value,
            dni: document.getElementById('dni').value,
            email: document.getElementById('email').value,
            telefono: document.getElementById('telefono').value,
            direccion: document.getElementById('direccion').value,
            historial_crediticio: document.getElementById('historial_crediticio').value || null
        };

        try {
            const url = clienteId ? 
                `/api/clientes/${clienteId}` : 
                '/api/clientes/';
            
            const response = await fetch(url, {
                method: clienteId ? 'PUT' : 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(data)
            });

            if (!response.ok) {
                const error = await response.json();
                throw new Error(error.detail || 'Error al procesar la solicitud');
            }

            const responseData = await response.json();

            if (clienteId) {
                // Actualizar la fila existente
                const row = document.querySelector(`tr[data-id="${clienteId}"]`);
                if (row) {
                    row.cells[1].textContent = data.nombre;
                    row.cells[2].textContent = data.apellido;
                    row.cells[3].textContent = data.dni;
                    row.cells[4].textContent = data.email;
                    row.cells[5].textContent = data.telefono;
                    row.cells[6].textContent = data.direccion;
                    row.cells[7].textContent = data.historial_crediticio ? 
                        parseFloat(data.historial_crediticio).toFixed(2) : 'N/A';
                }
            } else {
                // Agregar nueva fila
                const tbody = document.querySelector('#clientes-table tbody');
                const newRow = tbody.insertRow();
                newRow.setAttribute('data-id', responseData.id);
                
                newRow.innerHTML = `
                    <td>${responseData.id}</td>
                    <td>${data.nombre}</td>
                    <td>${data.apellido}</td>
                    <td>${data.dni}</td>
                    <td>${data.email}</td>
                    <td>${data.telefono}</td>
                    <td>${data.direccion}</td>
                    <td>${data.historial_crediticio ? parseFloat(data.historial_crediticio).toFixed(2) : 'N/A'}</td>
                    <td class="action-buttons">
                        <button class="edit-btn" onclick="editarCliente('${responseData.id}')">Editar</button>
                        <button class="delete-btn" onclick="eliminarCliente('${responseData.id}')">Eliminar</button>
                    </td>
                `;
            }

            alert(clienteId ? 'Cliente actualizado correctamente' : 'Cliente agregado correctamente');
            closeClienteModal();
        } catch (error) {
            console.error('Error:', error);
            alert(error.message);
        }
    });

    // Agregar estas funciones para el CRUD de solicitudes

    // Función para mostrar el modal de agregar solicitud
    window.showAddSolicitudModal = function() {
        document.getElementById('solicitudModalTitle').textContent = 'Agregar Solicitud';
        document.getElementById('solicitud-id').value = '';
        document.getElementById('solicitudForm').reset();
        document.getElementById('solicitudModal').style.display = 'block';
    }

    // Función para cerrar el modal de solicitud
    window.closeSolicitudModal = function() {
        document.getElementById('solicitudModal').style.display = 'none';
    }

    // Función para editar solicitud
    window.editarSolicitud = function(solicitudId) {
        try {
            const row = document.querySelector(`#solicitudes-table tr[data-id="${solicitudId}"]`);
            if (!row) {
                throw new Error('No se encontró la fila de la solicitud');
            }

            document.getElementById('solicitudModalTitle').textContent = 'Editar Solicitud';
            document.getElementById('solicitud-id').value = solicitudId;
            
            // Obtener los IDs del cliente y celular de los atributos data-*
            const clienteId = row.getAttribute('data-cliente-id');
            const celularId = row.getAttribute('data-celular-id');
            
            // Llenar el formulario con los datos actuales
            const cells = row.cells;
            
            // Seleccionar el cliente y celular correctos en los dropdowns
            document.getElementById('cliente_id').value = clienteId;
            document.getElementById('celular_id').value = celularId;
            
            // Extraer y limpiar el plazo (quitar la palabra "meses")
            const plazoText = cells[3].textContent;
            const plazo = plazoText.replace(' meses', '');
            document.getElementById('plazo_meses').value = plazo;
            
            // Extraer y limpiar el ingreso mensual (quitar el símbolo $)
            const ingresoText = cells[4].textContent;
            const ingreso = ingresoText.replace('$', '').trim();
            document.getElementById('ingreso_mensual').value = ingreso;
            
            // Establecer el estado
            const estado = cells[5].textContent.toLowerCase();
            document.getElementById('estado').value = estado;

            // Mostrar el modal
            document.getElementById('solicitudModal').style.display = 'block';

            // Debug - mostrar los valores que se están cargando
            console.log('Datos cargados:', {
                id: solicitudId,
                clienteId: clienteId,
                celularId: celularId,
                plazo: plazo,
                ingreso: ingreso,
                estado: estado
            });

        } catch (error) {
            console.error('Error al cargar datos de la solicitud:', error);
            alert('Error al cargar los datos de la solicitud: ' + error.message);
        }
    }

    // Función para eliminar solicitud
    window.eliminarSolicitud = async function(solicitudId) {
        if (!confirm('¿Está seguro de eliminar esta solicitud?')) return;

        try {
            const response = await fetch(`/api/solicitudes/${solicitudId}`, {
                method: 'DELETE'
            });

            if (!response.ok) {
                const error = await response.json();
                throw new Error(error.detail || 'Error al eliminar la solicitud');
            }

            // Eliminar la fila de la tabla
            const row = document.querySelector(`#solicitudes-table tr[data-id="${solicitudId}"]`);
            if (row) row.remove();

            alert('Solicitud eliminada correctamente');
        } catch (error) {
            console.error('Error:', error);
            alert(error.message);
        }
    }

    // Actualiza el manejador del formulario de solicitud
    document.getElementById('solicitudForm').addEventListener('submit', async function(e) {
        e.preventDefault();

        const solicitudId = document.getElementById('solicitud-id').value;
        const data = {
            cliente_id: parseInt(document.getElementById('cliente_id').value),
            celular_id: parseInt(document.getElementById('celular_id').value),
            plazo_meses: parseInt(document.getElementById('plazo_meses').value),
            ingreso_mensual: parseFloat(document.getElementById('ingreso_mensual').value),
            estado: document.getElementById('estado').value
        };

        console.log('Datos a enviar:', data);  // Debug

        try {
            const url = solicitudId ? 
                `/api/solicitudes/${solicitudId}` : 
                '/api/solicitudes/';
            
            const response = await fetch(url, {
                method: solicitudId ? 'PUT' : 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(data)
            });

            const responseData = await response.json();
            console.log('Respuesta del servidor:', responseData);  // Debug

            if (!response.ok) {
                throw new Error(responseData.detail || 'Error al procesar la solicitud');
            }

            if (solicitudId) {
                // Actualizar la fila existente
                const row = document.querySelector(`tr[data-id="${solicitudId}"]`);
                if (row) {
                    const clienteSelect = document.getElementById('cliente_id');
                    const celularSelect = document.getElementById('celular_id');
                    const clienteText = clienteSelect.options[clienteSelect.selectedIndex].text;
                    const celularText = celularSelect.options[celularSelect.selectedIndex].text;

                    row.cells[1].textContent = clienteText;
                    row.cells[2].textContent = celularText;
                    row.cells[3].textContent = `${data.plazo_meses} meses`;
                    row.cells[4].textContent = `$${data.ingreso_mensual.toFixed(2)}`;
                    row.cells[5].textContent = data.estado;
                }
            } else {
                location.reload(); // Solo recargar si es una nueva solicitud
            }

            alert(solicitudId ? 'Solicitud actualizada correctamente' : 'Solicitud creada correctamente');
            document.getElementById('solicitudModal').style.display = 'none';
        } catch (error) {
            console.error('Error completo:', error);
            alert('Error al procesar la solicitud: ' + error.message);
        }
    });

    // Agregar esta función para manejar el envío del formulario de solicitud
    document.getElementById('solicitud-form').addEventListener('submit', async function(e) {
        e.preventDefault();
        
        const formData = new FormData(e.target);
        
        try {
            const response = await fetch('/api/solicitar-credito/', {
                method: 'POST',
                body: formData
            });

            if (!response.ok) {
                const error = await response.json();
                throw new Error(error.detail || 'Error al enviar la solicitud');
            }

            const result = await response.json();
            alert(`Solicitud enviada exitosamente. Su número de solicitud es: ${result.id}`);
            e.target.reset();
        } catch (error) {
            console.error('Error:', error);
            alert('Error al enviar la solicitud: ' + error.message);
        }
    });

    // Agregar estas funciones para manejar la aprobación/rechazo de solicitudes
    window.aprobarSolicitud = async function(solicitudId) {
        try {
            const response = await fetch(`/api/solicitudes/${solicitudId}/estado`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ estado: 'aprobado' })
            });

            if (!response.ok) {
                const error = await response.json();
                throw new Error(error.detail || 'Error al aprobar la solicitud');
            }

            // Remover la fila de la tabla de pendientes
            const row = document.querySelector(`#solicitudes-pendientes-table tr[data-id="${solicitudId}"]`);
            if (row) {
                row.remove();
            }
            alert('Solicitud aprobada correctamente');
        } catch (error) {
            console.error('Error:', error);
            alert('Error al aprobar la solicitud: ' + error.message);
        }
    }

    window.rechazarSolicitud = async function(solicitudId) {
        try {
            const response = await fetch(`/api/solicitudes/${solicitudId}/estado`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ estado: 'rechazado' })
            });

            if (!response.ok) {
                const error = await response.json();
                throw new Error(error.detail || 'Error al rechazar la solicitud');
            }

            // Remover la fila de la tabla de pendientes
            const row = document.querySelector(`#solicitudes-pendientes-table tr[data-id="${solicitudId}"]`);
            if (row) {
                row.remove();
            }
            alert('Solicitud rechazada correctamente');
        } catch (error) {
            console.error('Error:', error);
            alert('Error al rechazar la solicitud: ' + error.message);
        }
    }

    async function actualizarEstadoSolicitud(solicitudId, estado) {
        try {
            const response = await fetch(`/api/solicitudes/${solicitudId}/estado`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ estado: estado })
            });

            if (!response.ok) {
                const error = await response.json();
                throw new Error(error.detail || 'Error al actualizar el estado');
            }

            // Remover la fila de la tabla de pendientes
            const row = document.querySelector(`#solicitudes-pendientes-table tr[data-id="${solicitudId}"]`);
            if (row) row.remove();

            alert(`Solicitud ${estado} exitosamente`);
        } catch (error) {
            console.error('Error:', error);
            alert('Error al actualizar el estado: ' + error.message);
        }
    }

    // Función para enviar solicitud desde la página principal
    async function enviarSolicitud(e) {
        e.preventDefault();
        
        const formData = new FormData(e.target);
        
        try {
            const response = await fetch('/api/solicitar-credito/', {
                method: 'POST',
                body: formData
            });

            if (!response.ok) {
                const error = await response.json();
                throw new Error(error.detail || 'Error al enviar la solicitud');
            }

            const result = await response.json();
            alert(`Solicitud enviada exitosamente. Su número de solicitud es: ${result.id}`);
            e.target.reset();
        } catch (error) {
            console.error('Error:', error);
            alert('Error al enviar la solicitud: ' + error.message);
        }
    }

    document.getElementById('credito-form').addEventListener('submit', async function(e) {
        e.preventDefault();
        
        const data = {
            cliente_id: parseInt(document.getElementById('cliente-id').value),
            celular_id: parseInt(document.getElementById('celular_id').value),
            plazo_meses: parseInt(document.getElementById('plazo_meses').value),
            ingreso_mensual: parseFloat(document.getElementById('ingreso_mensual').value),
            estado: 'pendiente'
        };

        console.log('Intentando enviar datos:', data);  // Debug
        
        try {
            const response = await fetch('/api/solicitudes/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(data)
            });

            console.log('Respuesta recibida:', response.status);  // Debug

            const responseData = await response.json();
            console.log('Datos de respuesta:', responseData);  // Debug

            if (!response.ok) {
                throw new Error(responseData.detail || 'Error al crear el crédito');
            }

            alert('Crédito creado correctamente');
            document.getElementById('credito-form').reset();
            window.location.href = '/admin';
        } catch (error) {
            console.error('Error completo:', error);
            alert('Error al crear el crédito: ' + error.message);
        }
    });
});