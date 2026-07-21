<template>
  <div class="container mt-4">
    <h1 class="text-center mb-4">🛒 Tienda Online</h1>

    <div class="row">
      <div class="col-md-8">
        <h3>Productos</h3>
        <div class="row">
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
                v-for="(producto, index) in carrito" 
                :key="index" 
                class="card mb-2"
              >
                <div class="card-body d-flex justify-content-between align-items-center">
                  <span>{{ producto.nombre }} - ${{ producto.precio }}</span>
                  <button 
                    class="btn btn-sm btn-danger" 
                    @click="eliminarProducto(index)"
                  >
                    X
                  </button>
                </div>
              </div>
            </div>

            <hr>

            <h4>Total: ${{ total }}</h4>

            <button class="btn btn-success w-100" @click="finalizarCompra">
              Finalizar Compra
            </button>
            <button class="btn btn-danger w-100 mt-2" @click="vaciarCarrito">
              Vaciar Carrito
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import Swal from 'sweetalert2'; // Asegúrate de tener instalado sweetalert2 (npm install sweetalert2)

// Estado reactivo
const productos = ref([]);
const carrito = ref([]);

// Obtener datos del backend
const cargarProductos = async () => {
  try {
    const respuesta = await fetch("http://127.0.0.1:8000/productos");
    productos.value = await respuesta.json();
  } catch (error) {
    console.error("Error al cargar productos:", error);
  }
};

// Hook de ciclo de vida: se ejecuta al montar el componente
onMounted(() => {
  cargarProductos();
});

// Propiedad computada para el total (se actualiza automáticamente)
const total = computed(() => {
  return carrito.value.reduce((suma, producto) => suma + producto.precio, 0);
});

// Métodos del carrito
const agregarCarrito = (id) => {
  const producto = productos.value.find(p => p.id_producto === id);
  if (producto) {
    carrito.value.push(producto);
    Swal.fire({
      icon: 'success',
      title: 'Producto agregado',
      text: producto.nombre,
      timer: 1500,
      showConfirmButton: false
    });
  }
};

const eliminarProducto = (index) => {
  carrito.value.splice(index, 1);
};

const vaciarCarrito = () => {
  carrito.value = [];
  Swal.fire({
    icon: 'warning',
    title: 'Carrito vaciado'
  });
};

const finalizarCompra = () => {
  if (carrito.value.length === 0) {
    Swal.fire({
      icon: 'error',
      title: 'El carrito está vacío'
    });
    return;
  }
  
  Swal.fire({
    icon: 'success',
    title: 'Compra realizada'
  });
  
  carrito.value = [];
};
</script>

<style>
/* Aquí puedes incluir el contenido de tu antiguo style.css si lo deseas */
.producto-card {
  margin-bottom: 1rem;
}
</style>
