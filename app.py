import streamlit as st
from main import registrar_cheque, listar_cheques, entregar_cheque

st.title("Formulario de Cheques")


with st.form("formulario_cheques"):
    numero = st.text_input("Número de cheque")
    tipo = st.selectbox("Tipo de cheque", ["Físico", "Echeq"])
    emisor = st.text_input("Emisor del cheque (Quién firmó)")
    banco = st.selectbox("Banco emisor", ["BBVA", "Banco Macro", "Banco Galicia", "Banco Santander", "Banco Patagonia", "Banco Ciudad", "HSBC", "Banco Comafi", "Banco Itaú", "Banco Credicoop","otro"])
    monto = st.number_input("Monto")
    fecha_emision = st.date_input("Fecha de emisión")
    fecha_pago = st.date_input("Fecha de pago")
    
    boton_registrar = st.form_submit_button("Registrar cheque")
    
    if boton_registrar:
        f_emision_txt = fecha_emision.strftime("%Y-%m-%d")
        f_pago_txt = fecha_pago.strftime("%Y-%m-%d")
        
        
        registrar_cheque(numero, tipo, emisor, banco, monto, f_emision_txt, f_pago_txt)
        st.success("Cheque registrado con éxito.")


st.subheader(" Cheques Registrados en el Sistema")

mis_cheques = listar_cheques()

if mis_cheques:
    st.dataframe(mis_cheques)
else:
    st.info("Aún no hay cheques registrados en el sistema.")


st.subheader("Entregar Cheque a Terceros")

with st.form("formulario_entrega"):
    num_cheque_entrega = st.text_input("Número del cheque a entregar")
    persona_destino = st.text_input("¿A quién se lo entregamos?")
    
    boton_entregar = st.form_submit_button("Confirmar Entrega")
    
    if boton_entregar:
        if num_cheque_entrega and persona_destino:
            entregar_cheque(num_cheque_entrega, persona_destino)
            st.success(f"¡Cheque N° {num_cheque_entrega} marcado como entregado a {persona_destino}!")
            st.rerun()
        else:
            st.error("Por favor, completa ambos campos para realizar la entrega.")