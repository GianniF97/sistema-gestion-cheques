import pandas as pd
import streamlit as st
from main import registrar_cheque, listar_cheques, cambiar_estado_cheque

st.title("Formulario de Cheques")


with st.form("formulario_cheques"):
    numero = st.text_input("Número de cheque")
    tipo = st.selectbox("Tipo de cheque", ["Físico", "Echeq"])
    emisor = st.text_input("Emisor del cheque (Quién firmó)")
    banco = st.selectbox("Banco emisor", ["BBVA", "Banco Macro", "Banco Galicia", "Banco Santander", "Banco Patagonia", "Banco Ciudad", "HSBC", "Banco Comafi", "Banco Itaú", "Banco Credicoop", "otro"])
    monto = st.number_input("Monto")
    fecha_emision = st.date_input("Fecha de emisión")
    fecha_pago = st.date_input("Fecha de pago")
    
    boton_registrar = st.form_submit_button("Registrar cheque")
    
    if boton_registrar:
        f_emision_txt = fecha_emision.strftime("%Y-%m-%d")
        f_pago_txt = fecha_pago.strftime("%Y-%m-%d")
        
        exito, mensaje = registrar_cheque(numero, tipo, emisor, banco, monto, f_emision_txt, f_pago_txt)
        
        if exito:
            st.success(mensaje)
            st.rerun() 
        else:
            st.error(mensaje)
    



st.subheader("📋 Cheques Registrados en el Sistema")

mis_cheques = listar_cheques()

if mis_cheques:
   
    columnas = [
        "ID", "N° Cheque", "Tipo", "Emisor", "Banco Emisor", 
        "Monto ($)", "F. Emisión", "F. Pago", "Estado", "Entregado a", "F. Entrega"
    ]
    
   
    df = pd.DataFrame(mis_cheques, columns=columnas)
    
   
    df_visualizacion = df.drop(columns=["ID"])
    
   
    st.dataframe(df_visualizacion, use_container_width=True)
else:
    st.info("Aún no hay cheques registrados en el sistema.")



st.subheader("🤝 Entregar Cheque a Terceros")

with st.form("formulario_entrega"):
    num_cheque_entrega = st.text_input("Número del cheque a entregar")
    persona_destino = st.text_input("¿A quién se lo entregamos?")
    
    boton_entregar = st.form_submit_button("Confirmar Entrega")
    
    if boton_entregar:
        if num_cheque_entrega and persona_destino:
            cambiar_estado_cheque(num_cheque_entrega, persona_destino)
            st.success(f"¡Cheque N° {num_cheque_entrega} marcado como entregado a {persona_destino}!")
            st.rerun()
        else:
            st.error("Por favor, completa ambos campos para realizar la entrega.")


st.subheader("🔄 Cambiar Estado del Cheque (Depositar / Entregar)")

with st.form("formulario_destino"):
    num_cheque_entrega = st.text_input("Número del cheque a procesar")
    
    accion = st.radio("¿Qué acción desea realizar?", ["Depositar en Banco", "Entregar a Tercero"])
    
  
    persona_destino = st.text_input("¿A quién se lo entregamos? (Opcional si va al banco)")
    
    boton_procesar = st.form_submit_button("Confirmar Operación")
    
    if boton_procesar:
        if num_cheque_entrega:
           
            if accion == "Entregar a Tercero" and not persona_destino:
                st.error("Por favor, ingresa el nombre del tercero al que le entregas el cheque.")
            else:
              
                from main import cambiar_estado_cheque 
                cambiar_estado_cheque(num_cheque_entrega, accion, persona_destino)
                
                st.success(f"¡Cheque N° {num_cheque_entrega} procesado con éxito como: {accion}!")
                st.rerun()
        else:
            st.error("Por favor, ingresa el número de cheque.")