<template>
  <div class="container mt-4">
    <h1 class="text-center mb-4">🛒 Tienda Online</h1>

    <div class="row">
      <div class="col-md-8">
        <h3>Productos</h3>
        <div id="productos" class="row">
          <div 
            v-for="producto in productos" 
            :key="producto.id_producto" 
            class="col-md-6 producto-card mb-3"
          >
            <div class="card shadow">
              <div class="card-body">
                <h5>{{ producto.nombre }}</h5>
                <p>Precio: ${{ producto.precio }}</p>
                <p>Stock: {{ producto.stock }}</p>
                <button 
                  class="btn btn-primary" 
                  @click="agregarCarrito(producto.id_producto)"
                  :disabled="producto.stock === 0"
                >
                  Agregar al carrito
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div class="col-md-4">
        <div class="card shadow">
          <div class="card-body">
            <h3>Carrito</h3>
            
            <div id="carrito">
              <div 
                v-for="item in carrito" 
                :key="item.id_carrito" 
                class="card mb-2"
              >
                <div class="card-body d-flex justify-content-between align-items-center">
                  <div>
                    <strong>{{ item.nombre }}</strong> <br>
                    <small>Cant: {{ item.cantidad }} | Subtotal: ${{ item.subtotal }}</small>
                  </div>
                  <button 
                    class="btn btn-sm btn-danger" 
                    @click="eliminarProducto(item.id_carrito)"
                  >
                    X
                  </button>
                </div>
              </div>
            </div>

            <hr>

            <h4 id="total">Total: ${{ total }}</h4>

            <button class="btn btn-success w-100" @click="finalizarCompra">
              Finalizar Compra
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import Swal from 'sweetalert2'; // Recuerda instalarlo o usar CDN para las alertas visuales [cite: 10]

// Estado reactivo
const productos = ref([]);
const carrito = ref([]);

// ==========================
// API FETCH: PRODUCTOS
// ==========================
// Lee la tabla productos y devuelve la lista en JSON [cite: 15]
const cargarProductos = async () => {
  try {
    const respuesta = await fetch("http://127.0.0.1:8000/productos");
    productos.value = await respuesta.json();
  } catch (error) {
    console.error("Error al cargar productos (¿Está FastAPI encendido?):", error);
  }
};

// ==========================
// API FETCH: CARRITO
// ==========================
// Devuelve los productos actuales en la tabla carrito 
const cargarCarrito = async () => {
  try {
    const respuesta = await fetch("http://127.0.0.1:8000/carrito");
    carrito.value = await respuesta.json();
  } catch (error) {
    console.error("Error al cargar el carrito:", error);
  }
};

// Se ejecuta automáticamente al abrir la página [cite: 24]
onMounted(() => {
  cargarProductos();
  cargarCarrito();
});

// Calcula el total sumando los subtotales [cite: 27]
const total = computed(() => {
  return carrito.value.reduce((suma, item) => suma + parseFloat(item.subtotal), 0);
});

// ==========================
// API POST: AGREGAR AL CARRITO
// ==========================
// Recibe el id_producto y la cantidad, validando el stock [cite: 17, 18]
const agregarCarrito = async (id_producto) => {
  try {
    const respuesta = await fetch("http://127.0.0.1:8000/carrito/agregar", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ id_producto: id_producto, cantidad: 1 }) // Agregamos de a 1 por clic
    });
    
    const data = await respuesta.json();

    if (data.mensaje === "Stock insuficiente") {
      Swal.fire({
        icon: 'error',
        title: 'Oops...',
        text: 'No hay suficiente stock en la base de datos'
      });
      return;
    }

    // Alerta linda y actualización de la vista [cite: 10]
    Swal.fire({
      icon: 'success',
      title: 'Producto agregado',
      timer: 1000,
      showConfirmButton: false
    });
    
    // Recargamos los datos para ver los cambios de la base de datos
    cargarCarrito();
    
  } catch (error) {
    console.error("Error al agregar al carrito:", error);
  }
};

// ==========================
// API DELETE: ELIMINAR PRODUCTO
// ==========================
// Elimina un producto específico del carrito 
const eliminarProducto = async (id_carrito) => {
  try {
    await fetch(`http://127.0.0.1:8000/carrito/eliminar/${id_carrito}`, {
      method: "DELETE"
    });
    
    cargarCarrito(); // Actualizamos la lista
  } catch (error) {
    console.error("Error al eliminar:", error);
  }
};

// ==========================
// API POST: FINALIZAR COMPRA
// ==========================
// Resta el stock y vacía la tabla carrito mediante una transacción 
const finalizarCompra = async () => {
  if (carrito.value.length === 0) {
    Swal.fire({ icon: 'error', title: 'El carrito está vacío' });
    return;
  }
  
  try {
    const respuesta = await fetch("http://127.0.0.1:8000/carrito/finalizar", {
      method: "POST"
    });
    const data = await respuesta.json();

    if (data.mensaje === "Compra finalizada") {
      // Limpia la pantalla con un mensaje de éxito [cite: 28]
      Swal.fire({
        icon: 'success',
        title: '¡Compra exitosa!',
        text: 'El stock ha sido actualizado en la base de datos.'
      });
      
      cargarCarrito(); // Quedará vacío
      cargarProductos(); // Se actualizan los números de stock
    } else {
      Swal.fire({ icon: 'error', title: 'Error en la compra' });
    }
  } catch (error) {
    console.error("Error al finalizar:", error);
  }
};
</script>

<style>
.producto-card { margin-bottom: 1rem; }
</style>