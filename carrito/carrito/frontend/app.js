let carrito = [];
let productos = [];

async function cargarProductos(){

    const respuesta =
    await fetch(
        "http://127.0.0.1:8000/productos"
    );

    productos =
    await respuesta.json();

    let contenedor =
    document.getElementById("productos");

    contenedor.innerHTML = "";

    productos.forEach(producto => {

        contenedor.innerHTML += `

        <div class="col-md-6 producto-card">

            <div class="card shadow">

                <div class="card-body">

                    <h5>${producto.nombre}</h5>

                    <p>Precio: $${producto.precio}</p>

                    <p>Stock: ${producto.stock}</p>

                    <button
                    class="btn btn-primary"
                    onclick="agregarCarrito(${producto.id_producto})">

                        Agregar al carrito

                    </button>

                </div>

            </div>

        </div>

        `;
    });
}

cargarProductos();
function agregarCarrito(id){

    const producto =
    productos.find(
    p => p.id_producto === id
    );

    carrito.push(producto);

    mostrarCarrito();

    Swal.fire({
        icon:'success',
        title:'Producto agregado',
        text: producto.nombre,
        timer:1500,
        showConfirmButton:false
    });

}

function mostrarCarrito(){

    let contenedor =
    document.getElementById("carrito");

    contenedor.innerHTML = "";

    let total = 0;

    carrito.forEach((producto,index) => {

        total += producto.precio;

        contenedor.innerHTML += `

        <div class="card mb-2">

            <div class="card-body d-flex justify-content-between">

                <span>

                    ${producto.nombre}
                    - $${producto.precio}

                </span>

                <button
                class="btn btn-sm btn-danger"
                onclick="eliminarProducto(${index})">

                    X

                </button>

            </div>

        </div>

        `;

    });

    document.getElementById("total")
    .innerText = `Total: $${total}`;

}
function eliminarProducto(index){

    carrito.splice(index,1);

    mostrarCarrito();

}

function vaciarCarrito(){

    carrito = [];

    mostrarCarrito();

    Swal.fire({
        icon:'warning',
        title:'Carrito vaciado'
    });

}

function finalizarCompra(){

    if(carrito.length === 0){

        Swal.fire({
            icon:'error',
            title:'El carrito está vacío'
        });

        return;
    }

    Swal.fire({
        icon:'success',
        title:'Compra realizada'
    });

    carrito = [];

    mostrarCarrito();

}