import pandas as pd
import streamlit as st
from main import registrar_cheque, listar_cheques, cambiar_estado_cheque


st.set_page_config(page_title="Gestión de Cheques", page_icon="", layout="wide")

st.title(" Sistema de Gestión de Cheques")
st.markdown("---")


mis_cheques = listar_cheques()
columnas = ["ID", "N° Cheque", "Tipo", "Emisor", "Banco Emisor", "Monto ($)", "F. Emisión", "F. Pago", "Estado", "Entregado a", "F. Entrega"]
df = pd.DataFrame(mis_cheques, columns=columnas)


tab_cartera, tab_registro, tab_operaciones = st.tabs(["📋 Ver Cartera", "➕ Registrar Cheque", "🔄 Cambiar Estado"])


with tab_cartera:
    if not df.empty:
        total_monto = df["Monto ($)"].sum()
        pendientes = df[df["Estado"] == "pendiente"]
        total_pendiente = pendientes["Monto ($)"].sum()
        cant_pendientes = len(pendientes)

        m1, m2, m3 = st.columns(3)
        m1.metric(" Total en Cartera", f"$ {total_monto:,.2f}")
        m2.metric(" Pendiente de Cobro", f"$ {total_pendiente:,.2f}")
        m3.metric(" Cheques Pendientes", cant_pendientes)

        st.markdown("### Detalle de Cheques")
       
        df_visual = df.drop(columns=["ID"])
        st.dataframe(
            df_visual, 
            use_container_width=True,
            column_config={
                "Monto ($)": st.column_config.NumberColumn("Monto ($)", format="$ %,.2f"),
                "Estado": st.column_config.TextColumn("Estado", help="Estado actual del cheque")
            }
        )
    else:
        st.info("Aún no hay cheques registrados. ¡Empezá por la pestaña de registro!")


with tab_registro:
    st.subheader("Cargar nuevo cheque a la cartera")
    with st.form("form_nuevo_cheque"):
        c1, c2 = st.columns(2)
        with c1:
            numero = st.text_input("Número de cheque")
            emisor = st.text_input("Emisor (Quién firmó)")
            banco = st.selectbox("Banco emisor", ["BBVA", "Banco Macro", "Banco Galicia", "Banco Santander", "Banco Patagonia", "Banco Ciudad", "HSBC", "Banco Comafi", "Banco Itaú", "Banco Credicoop", "otro"])
        with c2:
            tipo = st.selectbox("Tipo de cheque", ["Físico", "Echeq"])
            monto = st.number_input("Monto ($)", min_value=0.0)
            f_emision = st.date_input("Fecha de emisión")
            f_pago = st.date_input("Fecha de pago")
        
        btn_reg = st.form_submit_button("Registrar en el Sistema")
        
        if btn_reg:
            exito, mensaje = registrar_cheque(numero, tipo, emisor, banco, monto, f_emision.strftime("%Y-%m-%d"), f_pago.strftime("%Y-%m-%d"))
            if exito:
                st.success(mensaje)
                st.rerun()
            else:
                st.error(mensaje)


with tab_operaciones:
    st.subheader("Gestionar destino del cheque")
    with st.form("form_operaciones"):
        c3, c4 = st.columns(2)
        with c3:
            num_proc = st.text_input("Número del cheque a procesar")
            accion = st.radio("¿Qué desea hacer?", ["Depositar en Banco", "Entregar a Tercero"])
        with c4:
            st.write(" ") 
            st.write(" ")
            persona = st.text_input("A quién se entrega (Si aplica)")
        
        btn_proc = st.form_submit_button("Confirmar Operación")
        
        if btn_proc:
            if num_proc:
                if accion == "Entregar a Tercero" and not persona:
                    st.error("Ingresá el nombre del destinatario.")
                else:
                    cambiar_estado_cheque(num_proc, accion, persona)
                    st.success("Operación realizada con éxito.")
                    st.rerun()
            else:
                st.error("Ingresá el número de cheque.")