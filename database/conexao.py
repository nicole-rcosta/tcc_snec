import mysql.connector as sql

def conectar():
    conexao = sql.connect(
        host="localhost",
        port=3306,
        user="root",
        password="root",
        database="db_snec"
    )

    #Criando o cursor
    cursor = conexao.cursor(dictionary=True)
    return conexao, cursor