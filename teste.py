def pagina_recuperar_senha_redefinicao():

    if request.method == "GET":

        return render_template(
            "password/auth_password_reset.html"
        )


    # ============================================
    # PEGA AS SENHAS
    # ============================================

    nova_senha = request.form.get(
        "new-password"
    )

    nova_senha_confirm = request.form.get(
        "confirm-password"
    )


    # ============================================
    # VERIFICA SE AS SENHAS SÃO IGUAIS
    # ============================================

    if nova_senha != nova_senha_confirm:

        return render_template(
            "password/auth_password_reset.html",
            erro_senha=True
        )


    # ============================================
    # PEGA O E-MAIL DA SESSION
    # ============================================

    email = session.get(
        "email_recuperacao"
    )


    # Se não existir e-mail na session
    if not email:

        return redirect(
            url_for(
                "pagina_recuperar_senha"
            )
        )


    # ============================================
    # ATUALIZA A SENHA
    # ============================================

    sucesso = atualizar_senha(
        email,
        nova_senha
    )


    # ============================================
    # SE DEU CERTO
    # ============================================

    if sucesso:

        # Remove os dados da recuperação
        session.pop(
            "email_recuperacao",
            None
        )

        session.pop(
            "codigo_recuperacao",
            None
        )

        session.pop(
            "expiracao_codigo",
            None
        )


        return render_template(
            "password/auth_password_reset.html",
            senha_atualizada=True
        )


    # ============================================
    # SE DEU ERRO
    # ============================================

    return render_template(
        "password/auth_password_reset.html",
        erro_atualizar_senha=True
    )
