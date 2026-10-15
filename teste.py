@app.route("/password_receive", methods=["POST"])
def receber_email():


    # verifica se o email existe

    if not verificar_email(email_digitado):

        flash(
            "E-mail não encontrado. Verifique o e-mail digitado.",
            "error"
        )

        return redirect(url_for("sua_pagina_de_cadastro"))


    # se existir:
