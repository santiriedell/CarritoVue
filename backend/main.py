from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import conectar

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==========================
# GET PRODUCTOS
# ==========================
@app.get("/productos")
def obtener_productos():
    conexion = conectar()
    cursor = conexion.cursor(dictionary=True)

    cursor.execute("SELECT * FROM productos")
    productos = cursor.fetchall()

    conexion.close()
    return productos


# ==========================
# GET CARRITO
# ==========================
@app.get("/carrito")
def obtener_carrito():

    conexion = conectar()
    cursor = conexion.cursor(dictionary=True)

    sql = """
    SELECT carrito.id_carrito,
           productos.nombre,
           productos.precio,
           carrito.cantidad,
           (productos.precio * carrito.cantidad) AS subtotal
    FROM carrito
    INNER JOIN productos
    ON carrito.id_producto = productos.id_producto
    """

    cursor.execute(sql)
    datos = cursor.fetchall()

    conexion.close()
    return datos


# ==========================
# AGREGAR AL CARRITO
# ==========================
@app.post("/carrito/agregar")
def agregar_carrito(datos: dict):

    id_producto = datos["id_producto"]
    cantidad = datos["cantidad"]

    conexion = conectar()
    cursor = conexion.cursor(dictionary=True)

    # Verificar stock
    cursor.execute(
        "SELECT stock FROM productos WHERE id_producto = %s",
        (id_producto,)
    )

    producto = cursor.fetchone()

    if producto["stock"] < cantidad:
        return {"mensaje": "Stock insuficiente"}

    # Verificar si ya existe
    cursor.execute(
        "SELECT * FROM carrito WHERE id_producto = %s",
        (id_producto,)
    )

    existe = cursor.fetchone()

    if existe:
        nueva_cantidad = existe["cantidad"] + cantidad

        cursor.execute(
            "UPDATE carrito SET cantidad = %s WHERE id_producto = %s",
            (nueva_cantidad, id_producto)
        )
    else:
        cursor.execute(
            "INSERT INTO carrito(id_producto, cantidad) VALUES(%s,%s)",
            (id_producto, cantidad)
        )

    conexion.commit()
    conexion.close()

    return {"mensaje": "Producto agregado"}
    

# ==========================
# ELIMINAR PRODUCTO
# ==========================
@app.delete("/carrito/eliminar/{id}")
def eliminar_producto(id: int):

    conexion = conectar()
    cursor = conexion.cursor()

    cursor.execute(
        "DELETE FROM carrito WHERE id_carrito = %s",
        (id,)
    )

    conexion.commit()
    conexion.close()

    return {"mensaje": "Producto eliminado"}


# ==========================
# FINALIZAR COMPRA
# ==========================
@app.post("/carrito/finalizar")
def finalizar_compra():

    conexion = conectar()
    cursor = conexion.cursor(dictionary=True)

    try:

        # Obtener carrito
        sql = """
        SELECT carrito.id_producto,
               carrito.cantidad,
               productos.stock
        FROM carrito
        INNER JOIN productos
        ON carrito.id_producto = productos.id_producto
        """

        cursor.execute(sql)
        productos = cursor.fetchall()

        # Restar stock
        for producto in productos:

            nuevo_stock = (
                producto["stock"] -
                producto["cantidad"]
            )

            cursor.execute(
                """
                UPDATE productos
                SET stock = %s
                WHERE id_producto = %s
                """,
                (nuevo_stock, producto["id_producto"])
            )

        # Vaciar carrito
        cursor.execute("DELETE FROM carrito")

        conexion.commit()

        return {"mensaje": "Compra finalizada"}

    except:
        conexion.rollback()
        return {"mensaje": "Error en la compra"}

    finally:
        conexion.close()