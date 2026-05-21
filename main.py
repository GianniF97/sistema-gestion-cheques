import datetime
<<<<<<< HEAD
from supabase import create_client, Client


SUPABASE_URL = "https://ezwblubdgtmcucpyxulj.supabase.co"
SUPABASE_KEY = "sb_publishable_-IdHxHC9-0yMOqQvwCVyTw_2blp9qQz"
=======
import streamlit as st  
from supabase import create_client, Client


SUPABASE_URL = st.secrets["SUPABASE_URL"]
SUPABASE_KEY = st.secrets["SUPABASE_KEY"]
>>>>>>> 054fdea414702561f0a5d8852c3b0e9e55c9c396

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)



def registrar_cheque(numero, tipo, emisor, banco, monto, fecha_emision, fecha_pago):
    try:
<<<<<<< HEAD
        # FORZAR CONVERSIÓN: Asegura que si viene como texto o float impreciso, 
        # se transforme en un flotante puro de Python (ej: 150000.0)
        monto_limpio = float(monto)
        
        data, count = supabase.table("cheques").insert({
            "numero": numero,
            "tipo": tipo,
            "emisor": emisor,
            "banco": banco,
            "monto": monto_limpio,  # Usamos la variable limpia aquí
            "fecha_emision": fecha_emision,
            "fecha_pago": fecha_pago,
            "estado": "pendiente"
        }).execute()
        
        return True, "Cheque registrado con éxito en la nube."
        
    except Exception as e:
        return False, f"Error al registrar: Asegúrese de que el N° {numero} no esté repetido."
        
        return True, "Cheque registrado con éxito en la nube."
        
    except Exception as e:
       
        return False, f"Error al registrar: Asegúrese de que el N° {numero} no esté repetido."

=======
      
        supabase.table("cheques").insert({
            "numero": numero,
            "tipo": tipo,
            "emisor": emisor,
            "banco": banco,
            "monto": monto,
            "fecha_emision": fecha_emision,
            "fecha_pago": fecha_pago,
            "estado": "pendiente"
        }).execute()
        
        return True, "Cheque registrado con éxito en la nube."
        
    except Exception as e:
       
        return False, f"Error al registrar: Asegúrese de que el N° {numero} no esté repetido."
>>>>>>> 054fdea414702561f0a5d8852c3b0e9e55c9c396


def cambiar_estado_cheque(numero, accion, entregado_a=None):
    fecha_hoy = datetime.date.today().strftime("%Y-%m-%d")
    
    if accion == "Depositar en Banco":
        nuevo_estado = "depositado"
        destino = "Banco (Depósito)"
    else:
        nuevo_estado = "entregado"
        destino = entregado_a

    
    supabase.table("cheques").update({
        "estado": nuevo_estado,
        "entregado_a": destino,
        "fecha_entrega": fecha_hoy
    }).eq("numero", numero).execute()



def listar_cheques():
    try:
<<<<<<< HEAD
        
=======
       
>>>>>>> 054fdea414702561f0a5d8852c3b0e9e55c9c396
        respuesta = supabase.table("cheques").select("*").execute()
        cheques_data = respuesta.data
        
        if not cheques_data:
            return []
            
<<<<<<< HEAD
     
=======
      
>>>>>>> 054fdea414702561f0a5d8852c3b0e9e55c9c396
        lista_ordenada = []
        for c in cheques_data:
            lista_ordenada.append((
                c.get("id"),
                c.get("numero"),
                c.get("tipo"),
                c.get("emisor"),
                c.get("banco"),
                c.get("monto"),
                c.get("fecha_emision"),
                c.get("fecha_pago"),
                c.get("estado"),
                c.get("entregado_a"),
                c.get("fecha_entrega")
            ))
        return lista_ordenada
    except Exception:
<<<<<<< HEAD
        return []
=======
        return []
>>>>>>> 054fdea414702561f0a5d8852c3b0e9e55c9c396
