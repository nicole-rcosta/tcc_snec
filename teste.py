import secrets
import time
from flask import Flask, session, request

app = Flask(__name__)
app.secret_key = "chave_teste"

@app.route("/")
def gerar_codigo():
    codigo = f"{secrets.randbelow(100000):05d}"

    session["codigo_recuperacao"] = codigo
    # coloca um limite de 3 minutos pra expirar
    session["expiracao_codigo"] = time.time() + 180

    return f"""
        <h2>Código gerado: {codigo}</h2>
        <p>Validade: 180 segundos</p>
        <a href="/validar">Testar código</a>
    """

@app.route("/validar")
def validar_codigo():
    codigo = session.get("codigo_recuperacao")
    expiracao = session.get("expiracao_codigo", 0)

    if not codigo:
        return "Nenhum código gerado. <a href='/'>Gerar código</a>"

    if time.time() >= expiracao:
        session.pop("codigo_recuperacao", None)
        session.pop("expiracao_codigo", None)
        return "Código expirado! <a href='/'>Gerar outro</a>"


if __name__ == "__main__":
    app.run(debug=True)