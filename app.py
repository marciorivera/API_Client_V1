import streamlit as st
import pandas as pd
from api_client import obtener_usuarios_api
from database import crear_tabla, guardar_usuarios, consultar_usuarios, eliminar_datos

st.set_page_config(page_title="API-SQLITE", page_icon=":guardsman:", layout="wide")

crear_tabla()

st.title("API-SQLITE-STREAMLIT")
st.write("Esta aplicacion permite obtener datos de una API y almacenarlos en una base de datos SQLite, asi como consultar y eliminar los datos almacenados")

menu=st.sidebar.selectbox(
    "Seleccione una opcion",
    [
        "Inicio",
        "Consumir API",
        "Ver la base de datos",
        "Buscar los usuarios",
        "Eliminar los datos"
    ]
)

if menu=="Inicio":
    st.header("Bienvenido a la aplicacion API-SQLITE-STREAMLIT")
    st.write("Esta aplicacion permite obtener datos de una API y almacenarlos en una base de datos SQLite, asi como consultar y eliminar los datos almacenados")

    st.info("Seleccione una opcion en el menu lateral para comenzar a utilizar la aplicacion")
    
elif menu=="Consumir API":
    st.header ("Consumir API publica")
    st.write("API Utilizada")
    st.code("https://jsonplaceholder.typicode.com/users")
    
    if st.button("Obtener usuarios de la API"):
       usuarios=obtener_usuarios_api()
       if usuarios:
           guardar_usuarios(usuarios)
           st.success("Usuarios obtenidos y guardados en la base de datos")
           st.json(usuarios[0])
       else:
           st.error("No se pudieron obtener los usuarios de la API")
           
elif menu == "Ver la base de datos":
    st.header("Tabla almacenada en nuestro SQLite")
    
    df = consultar_usuarios()
    
    if df.empty:
        st.warning("La base de datos esta vacia. Primero consuma la API")
    else: 
        st.dataframe(df,use_container_width=True)
        
        col1, col2, col3 = st.columns(3)
        col1.metric("Total usuarios", len(df))
        col2.metric("Total ciudades", df["ciudad"].nunique())
        col3.metric("Total correos", df["email"].nunique())
        
elif menu == "Buscar los usuarios":
    st.header("Buscar usuario en SQLite")

    df = consultar_usuarios()

    if df.empty:
        st.warning("No hay datos guardados")
    else:
        nombre = st.text_input("Ingrese nombre o usuario a buscar")

        if nombre:
            resultado = df[
                df["nombre"].str.contains(nombre, case=False, na=False) |
                df["usuario"].str.contains(nombre, case=False, na=False)
            ]

            if resultado.empty:
                st.error("No se encontraron coincidencias")
            else:
                st.success("Resultado encontrado")
                st.dataframe(resultado, use_container_width=True)

elif menu == "Eliminar los datos":
    st.header("Eliminar registros de SQLite")

    st.warning("Esta accion eliminara todos los datos almacenados")

    if st.button("Eliminar todos los datos"):
        eliminar_datos()
        st.success("Datos eliminados correctamente")   