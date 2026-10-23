import mysql.connector as sql
import os
from dotenv import load_dotenv

load_dotenv()

def conectar():
    BD_AMBIENTE = os.getenv("BD_AMBIENTE", "local")
    if BD_AMBIENTE == "local":
        conexao = sql.connect(
            host="localhost",
            port=3306,
            user="root",
            password="root",
            database="db_snec"
        )
    elif BD_AMBIENTE == "online":
        conexao = sql.connect(
                    host=os.getenv("BD_HOST"),
                    port=os.getenv("BD_PORT"),
                    user=os.getenv("BD_USER"),
                    password=os.getenv("BD_PASSWORD"),
                    database=os.getenv("BD_DATABASE")
                )
    #Criando o cursor
    cursor = conexao.cursor(dictionary=True)
    return conexao, cursor

