import bcrypt

def verificar_senha_mestra(senha: str, senha_cript_mestra: str) -> bool:
    senha_cript_mestra = senha_cript_mestra.encode('utf-8')
        
    # 2. Converte a senha digitada no login para bytes
    senha_bytes = senha.encode('utf-8')
    
    # 3. Compara a senha em texto puro com o hash salvo
    return bcrypt.checkpw(senha_bytes, senha_cript_mestra)