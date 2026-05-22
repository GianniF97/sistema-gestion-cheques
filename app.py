import pandas as pd
import streamlit as st
from main import registrar_cheque, listar_cheques, cambiar_estado_cheque


st.set_page_config(page_title="Gestión de Cheques", page_icon="💰", layout="wide")


if not st.user.get("email"):
    st.title("🔐 Acceso al Sistema de Cheques")
    st.subheader("Por favor, inicia sesión para continuar")
    st.info("Este sistema es privado y requiere autenticación previa.")
    
    st.login()  
with st.sidebar:
    if st.user.get("avatar"):
        st.image(st.user.get("avatar"), width=70)
    else:
        st.write("👤")
    st.write(f"**Bienvenido, {st.user.get('name', 'Usuario')}!**")
    st.write(f"✉️ {st.user.get('email')}")
    st.markdown("---")
    if st.button("🚪 Cerrar Sesión"):
        st.logout()
        st.rerun()


st.title("🏦 Sistema de Gestión de Cheques")
st.markdown("---")



mis_cheques = listar_cheques()
columnas = ["ID", "N° Cheque", "Tipo", "Emisor", "Banco Emisor", "Monto ($)", "F. Emisión", "F. Pago", "Estado", "Entregado a", "F. Entrega"]
df = pd.DataFrame(mis_cheques, columns=columnas)


df["Monto ($)"] = pd.to_numeric(df["Monto ($)"], errors='coerce')


tab_cartera, tab_registro, tab_operaciones = st.tabs(["📋 Ver Cartera", "➕ Registrar Cheque", "🔄 Cambiar Estado"])


with tab_cartera:
    if not df.empty:
        
        # 1. Asegurar que Pandas lo trate como número puro
        df["Monto ($)"] = pd.to_numeric(df["Monto ($)"], errors='coerce').fillna(0)
        
        # 2. Calcular los totales matemáticos exactos
        total_monto = float(df["Monto ($)"].sum())
        pendientes = df[df["Estado"] == "pendiente"]
        total_pendiente = float(pendientes["Monto ($)"].sum())
        cant_pendientes = len(pendientes)
        
        # 3. Formatear las tarjetas métricas (Estilo Argentina: . para miles, , para decimales)
        total_monto_en_ars = f"$ {total_monto:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
        total_pendiente_en_ars = f"$ {total_pendiente:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
        
        m1, m2, m3 = st.columns(3)
        m1.metric("Total en Cartera", total_monto_en_ars)
        m2.metric("Pendiente de Cobro", total_pendiente_en_ars)
        m3.metric("Cheques Pendientes", cant_pendientes)

        st.markdown("### Detalle de Cheques")
        
        # 4. CREAR UNA COPIA VISUAL Y FORMATEAR LA COLUMNA COMO STRING CONTROLADO
        df_visual = df.drop(columns=["ID"]).copy()
        
        # Forzamos el formato manualmente para evitar que el navegador lo altere
        df_visual["Monto ($)"] = df_visual["Monto ($)"].apply(
            lambda x: f"$ {x:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
        )
        
        # 5. Mostrar la tabla simple (ya que viene pre-formateada como texto limpio)
        st.dataframe(df_visual, use_container_width=True)
        
    else:
        st.info("Aún no hay cheques registrados. ¡Empezá por la pestaña de registro!")


with tab_registro:
    st.subheader("Cargar nuevo cheque a la cartera")
    
    # MOSTRAR EL MENSAJE GUARDADO (si existe) DESPUÉS DEL REINICIO
    if "mensaje_exito" in st.session_state:
        st.success(st.session_state.mensaje_exito)
        del st.session_state.mensaje_exito # Lo borramos para que no aparezca siempre
        
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
                # Guardamos el mensaje en la memoria de la sesión antes de reiniciar
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