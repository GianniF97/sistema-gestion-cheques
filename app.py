import pandas as pd
import streamlit as st
from main import registrar_cheque, listar_cheques, cambiar_estado_cheque

st.set_page_config(page_title="Gestión de Cheques", page_icon="💰", layout="wide")

# --- CONTROL DE ACCESO MANUAL (INMUNE A MAYÚSCULAS) ---
if "autenticado" not in st.session_state:
    st.session_state.autenticado = False

if not st.session_state.autenticado:
    st.title("🔐 Acceso al Sistema de Cheques")
    st.subheader("Por favor, introduce tus credenciales para continuar")
    
    with st.form("form_login_privado"):
        usuario = st.text_input("Usuario (Correo)")
        clave = st.text_input("Contraseña", type="password")
        btn_ingresar = st.form_submit_button("Iniciar Sesión")
        
        if btn_ingresar:
            # .lower() convierte lo que escribas a minúsculas, evitando errores si te olvidás las mayúsculas
            if usuario.lower() == "gianniferrari9789@gmail.com" and clave == "Cheques2026*":
                st.session_state.autenticado = True
                st.success("¡Acceso concedido!")
                st.rerun()
            else:
                st.error("Usuario o contraseña incorrectos. Sistema privado.")
    st.stop() 

# --- SIDEBAR ---
with st.sidebar:
    st.write("👤")
    st.write(f"**Bienvenido, Gianni!**")
    st.write(f"✉️ gianniferrari9789@gmail.com")
    st.markdown("---")
    if st.button("🚪 Cerrar Sesión"):
        st.session_state.autenticado = False
        st.rerun()

# --- CUERPO PRINCIPAL DE LA APP ---
st.title("🏦 Sistema de Gestión de Cheques")
st.markdown("---")

mis_cheques = listar_cheques()
columnas = ["ID", "N° Cheque", "Tipo", "Emisor", "Banco Emisor", "Monto ($)", "F. Emisión", "F. Pago", "Estado", "Entregado a", "F. Entrega"]

if mis_cheques and len(mis_cheques) > 0:
    df = pd.DataFrame(mis_cheques, columns=columnas)
else:
    df = pd.DataFrame(columns=columnas)

df["Monto ($)"] = pd.to_numeric(df["Monto ($)"], errors='coerce')

tab_cartera, tab_registro, tab_operaciones = st.tabs(["📋 Ver Cartera", "➕ Registrar Cheque", "🔄 Cambiar Estado"])

with tab_cartera:
    if not df.empty:
        df["Monto ($)"] = pd.to_numeric(df["Monto ($)"], errors='coerce').fillna(0)
        
        total_monto = float(df["Monto ($)"].sum())
        pendientes = df[df["Estado"] == "pendiente"]
        total_pendiente = float(pendientes["Monto ($)"].sum()) if not pendientes.empty else 0.0
        cant_pendientes = len(pendientes)
        
        total_monto_en_ars = f"$ {total_monto:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
        total_pendiente_en_ars = f"$ {total_pendiente:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
        
        m1, m2, m3 = st.columns(3)
        m1.metric("Total en Cartera", total_monto_en_ars)
        m2.metric("Pendiente de Cobro", total_pendiente_en_ars)
        m3.metric("Cheques Pendientes", cant_pendientes)

        st.markdown("### Detalle de Cheques")
        
        df_visual = df.drop(columns=["ID"]).copy()
        df_visual["Monto ($)"] = df_visual["Monto ($)"].apply(
            lambda x: f"$ {x:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
        )
        
        st.dataframe(df_visual, width="stretch")
        
    else:
        st.info("Aún no hay cheques registrados. ¡Empezá por la pestaña de registro!")

with tab_registro:
    st.subheader("Cargar nuevo cheque a la cartera")
    
    if "mensaje_exito" in st.session_state:
        st.success(st.session_state.mensaje_exito)
        del st.session_state.mensaje_exito 
        
    with st.form("form_nuevo_cheque"):
        c1, c2 = st.columns(2)
        with c1:
            numero = st.text_input("Número de cheque")
            emisor = st.text_input("Emisor (Quién firmó)")
            banco = st.selectbox("Banco emisor", ["BBVA", "Banco Macro", "Banco Galicia", "Banco Santander", "Banco Patagonia", "Banco Ciudad", "HSBC", "Banco Comafi", "Banco Itaú", "Banco Credicoop", "otro"])
        with c2:
            tipo = st.selectbox("Tipo de cheque", ["Físico", "Echeq"])
            monto = st.number_input("Monto ($)", min_value=0.0, step=1000.0, format="%.2f")
            f_emision = st.date_input("Fecha de emisión")
            f_pago = st.date_input("Fecha de pago")
        
        btn_reg = st.form_submit_button("Registrar en el Sistema")
        
        if btn_reg:
            exito, mensaje = registrar_cheque(numero, tipo, emisor, banco, monto, f_emision.strftime("%Y-%m-%d"), f_pago.strftime("%Y-%m-%d"))
            if exito:
                st.session_state.mensaje_exito = mensaje
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