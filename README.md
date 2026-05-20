# 📋 Sistema de Gestión de Cheques cartera

Una aplicación web interactiva desarrollada para automatizar el control, registro y seguimiento de cheques físicos y electrónicos (Echeqs). Permite llevar un historial detallado de la cartera de cheques y gestionar las entregas a terceros.

## ✨ Características del Sistema

- **Registro completo:** Captura de datos financieros críticos (Número de cheque, Tipo, Emisor, Banco Emisor, Monto y Fechas).
- **Persistencia de Datos:** Conexión local robusta utilizando **SQLite** para el almacenamiento seguro.
- **Interfaz Intuitiva:** Desarrollado con **Streamlit** para ofrecer una experiencia Full-Stack ágil y moderna desde el navegador.
- **Flujo de Entregas:** Módulo dedicado para transferir o endosar cheques existentes a terceros actualizando el estado en tiempo real.

## 🛠️ Tecnologías Utilizadas

- **Python 3.13** (Lenguaje principal)
- **Streamlit** (Interfaz de usuario)
- **SQLite3** (Motor de base de datos relacional)

## 🚀 Cómo ejecutar el proyecto localmente

1. Clonar este repositorio o descargar los archivos de código.
2. Asegurarse de tener instalado Python y Streamlit en la PC.
3. Ejecutar el servidor web desde la terminal con el comando:
   ```bash
   python -m streamlit run app.py