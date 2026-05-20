import sqlite3
import datetime


conexion = sqlite3.connect("cheques.db")
cursor = conexion.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS cheques (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        numero TEXT NOT NULL UNIQUE,
        tipo TEXT NOT NULL,
        emisor TEXT NOT NULL,
        banco TEXT NOT NULL,
        monto REAL NOT NULL,
        fecha_emision TEXT,
        fecha_pago TEXT NOT NULL,
        estado TEXT NOT NULL,
        entregado_a TEXT,
        fecha_entrega TEXT
    )
""")

conexion.commit()
conexion.close()

print("¡Base de datos creada con éxito!")



def registrar_cheque(numero, tipo, emisor, banco, monto, fecha_emision, fecha_pago):
    conexion = sqlite3.connect("cheques.db")
    cursor = conexion.cursor()
    
    try:
        cursor.execute("""
            INSERT INTO cheques (numero, tipo, emisor, banco, monto, fecha_emision, fecha_pago, estado)
            VALUES (?, ?, ?, ?, ?, ?, ?, 'pendiente')
        """, (numero, tipo, emisor, banco, monto, fecha_emision, fecha_pago))
        
        conexion.commit()
        conexion.close()
        return True, "Cheque registrado con éxito."
        
    except sqlite3.IntegrityError:
        conexion.close()
        return False, f"El cheque N° {numero} ya se encuentra registrado en el sistema."



def cambiar_estado_cheque(numero, accion, entregado_a=None):
    conexion = sqlite3.connect("cheques.db")
    cursor = conexion.cursor()
    fecha_hoy = datetime.date.today().strftime("%Y-%m-%d")
    
    # Si la acción es depositar, el destino es el banco y el estado es 'depositado'
    if accion == "Depositar en Banco":
        nuevo_estado = "depositado"
        destino = "Banco (Depósito)"
    else:
        # Si no, es una entrega normal a un tercero
        nuevo_estado = "entregado"
        destino = entregado_a

    cursor.execute("""
        UPDATE cheques
        SET estado = ?, entregado_a = ?, fecha_entrega = ?
        WHERE numero = ?
    """, (nuevo_estado, destino, fecha_hoy, numero))
    
    conexion.commit()
    conexion.close()
    print(f"Cheque N° {numero} actualizado a {nuevo_estado}.")



def listar_cheques():
    conexion = sqlite3.connect("cheques.db")
    cursor = conexion.cursor()
    
    cursor.execute("SELECT * FROM cheques")
    cheques = cursor.fetchall()
    
    conexion.close()
    return cheques