from flask import Flask, render_template, request, redirect, session, jsonify, flash, url_for
from model.extra_activity_register import cadastrar_atividade as ca, recuperar_atividade as ra, excluir_atividade as ea
from model.usuarios import cadastrar, logar
from model.usuarios import verificar_email
from model.usuarios import atualizar_senha
from model.salas import recuperar_salas
from model.salas import adicionar_sala
from model.salas import deletar_sala

import mysql
import mysql.connector
import secrets
import time
import smtplib
from email.message import EmailMessage

app = Flask(__name__)
app.secret_key = "snec_tcc_chave"

@app.route("/")

@app.route("/login")
def pagina_login():
    return render_template("login/auth_login.html")
@app.route("/login/post", methods=["POST"])
def logar_usuario():
    cpf = request.form.get("cpf")
    senha = request.form.get("password")

    resultado = logar(cpf, senha)

    if resultado['sucesso']:
        session['usuario'] = resultado['usuario']
        cargo = resultado['usuario']['cargo']
        if cargo == 'prof':
            return redirect('/teacher')
        elif cargo == 'nutri':
            return redirect('/nutri_dashboard')
        elif cargo == 'adm':
            return redirect('/adm')
        return render_template()
    else:
        return redirect("/cadastro")

@app.route("/cadastro")
def pagina_cadastro():
    return render_template("register/auth_register.html")
@app.route("/cadastro/post", methods=["POST"])
def cadastrar_usuario():
    nome = request.form.get("name")
    cpf = request.form.get("cpf")
    email = request.form.get("email")
    cargo = request.form.get("register")
    senha = request.form.get("password")

    if cadastrar(nome, email, cargo, senha, cpf):
        return render_template("login/auth_login.html")
    else:
        return redirect("/cadastro")
    
# ---------------------------
# Paginas de Administrador
# ---------------------------

@app.route("/adm")
def pagina_adm():
    return render_template("adm/admin_item_register.html")

@app.route("/adm_register")
def pagina_adm_register():
    return render_template("adm/admin_register.html")

@app.route("/adm/reg_activity")
def pagina_cad_atividade():
    atividades = ra()
    return render_template("adm/admin_extra_activity_register.html", atividades=atividades)

@app.route("/adm/reg_activity/post", methods=["POST"])
def pagina_cad_atividades():
    ativid = request.form.get("activity_name")
    periodo = request.form.get("activity_period")

    if ativid and periodo:
        ca(ativid, periodo)

    return redirect(url_for("pagina_cad_atividade"))
        

@app.route("/adm/exc_activity/<id_atividade>", methods=["POST"])
def excluir_atividades(id_atividade):
    
    ea(id_atividade)
    return redirect(url_for("pagina_cad_atividade"))


@app.route("/adm/reg_student")
def pagina_cad_aluno():
    return render_template("adm/admin_extra_student_register.html")




@app.route("/adm/reg_class")
def pagina_cad_sala():
    salas = recuperar_salas()
    return render_template("adm/admin_room_register.html", salas = salas)

@app.route("/adm/reg_class/post", methods=["POST"])
def pagina_cad_sala_post():
    turma= request.form.get("room_class")
    periodo= request.form.get("room_period")
    qnt_aluno= request.form.get("class_quantity")
    adicionar_sala(turma=turma,periodo=periodo,qnt_alunos=qnt_aluno)
    return redirect("/adm/reg_class")

@app.route("/adm/reg_class/delete/<int:id>")
def pagina_cad_sala_del(id):
    deletar_sala(id)
    return redirect("/adm/reg_class")




@app.route("/adm/conf_panel")
def pagina_confirmar_painel():
    return render_template("adm/admin_confirm.html")

@app.route("/adm/adm_panel")
def pagina_painel_adm():
    return render_template("adm/admin_access.html")


# ---------------------------
# Paginas de Nutricionista
# ---------------------------

@app.route("/nutri_dashboard")
def pagina_dashboard():
    return render_template("nutri/nutritionist_dashboard.html")

@app.route("/nutri_dashboard/report")
def pagina_dashboard_report():
    return render_template("nutri/nutritionist_report.html")

# ---------------------------
# Paginas de Professor
# ---------------------------

@app.route("/teacher")
def pagina_prof_selecionar_sala():
    return render_template("teacher/teacher_class_select.html")

@app.route("/teacher/class_info")
def pagina_prof_registro():
    return render_template("teacher/teacher_attendance_record.html")

@app.route("/teacher/class_info/confirm")
def pagina_confirmacao_prof():
    return render_template("teacher/teacher_attendance_confirm.html")

# =========================================================
# RECUPERAÇÃO DE SENHA
# =========================================================

# GET
# Mostra a página onde o usuário informa o e-mail
@app.route("/password_recover", methods=["GET"])
def pagina_recuperar_senha():
    return render_template(
        "password/auth_password_recover.html"
    )


# POST
# Recebe o e-mail, verifica, gera o código e envia
@app.route("/password_recover", methods=["POST"])
def receber_email():
    
    email_destinatario = request.form.get("email")

    # Verifica se o e-mail existe
    if not verificar_email(email_destinatario):
        return render_template(
            "password/auth_password_recover.html",
            erro_email=True
        )

    # Gera o código de 5 dígitos
    codigo = f"{secrets.randbelow(100000):05d}"

    # Salva as informações na sessão
    session["codigo_recuperacao"] = codigo
    session["expiracao_codigo"] = time.time() + 100
    session["email_recuperacao"] = email_destinatario

    # Dados do remetente
    EMAIL_REMETENTE = "pablolorenzomoralez@gmail.com"

    # NÃO coloque a senha diretamente no código em produção
    SENHA_APP = "mtls ntmg kxxn aquu" 

    # Cria o e-mail
    mensagem = EmailMessage()

    mensagem["Subject"] = "Código de Recuperação de senha"
    mensagem["From"] = EMAIL_REMETENTE
    mensagem["To"] = email_destinatario

    mensagem.set_content(f"""
Confirme seu e-mail

Use este código no SNEC para confirmar que este e-mail é seu:

{codigo}
""")

    # Envia o e-mail
    try:

        with smtplib.SMTP(
            "smtp.gmail.com",
            587,
            timeout=3
        ) as servidor:

            servidor.starttls()

            servidor.login(
                EMAIL_REMETENTE,
                SENHA_APP
            )

            print("Enviando e-mail...", flush=True)

            servidor.send_message(mensagem)

            print(
                "E-mail enviado com sucesso!",
                flush=True
            )

    except (
        smtplib.SMTPException,
        TimeoutError,
        OSError
    ) as erro:

        print(
            f"Erro ao enviar e-mail: {erro}",
            flush=True
        )

        return render_template(
            "password/auth_password_recover.html",
            erro_envio=True
        )

    # POST → GET
    return redirect(
        url_for("pagina_recuperar_senha_codigo")
    )


# GET
# Mostra a página onde o usuário informa o código
@app.route("/password_recover/code", methods=["GET"])
def pagina_recuperar_senha_codigo():
    return render_template(
        "password/auth_password_insert.html"
    )


# POST
# Recebe e valida o código
@app.route("/password_recover/code", methods=["POST"])
def verificar_codigo():

    codigo = session.get(
        "codigo_recuperacao"
    )

    expiracao = session.get(
        "expiracao_codigo",
        0
    )

    # Verifica se existe um código
    if not codigo:
        return redirect(
            url_for("pagina_recuperar_senha")
        )

    # Verifica se o código expirou
    if time.time() >= expiracao:

        session.pop(
            "codigo_recuperacao",
            None
        )

        session.pop(
            "expiracao_codigo",
            None
        )

        return render_template(
            "password/auth_password_insert.html",
            codigo_expirado=True
        )

    # Recebe o código enviado pelo JavaScript
    codigo_digitado = request.form.get(
        "codigo",
        ""
    )

    # Verifica se o código está correto
    if codigo_digitado != codigo:

        return render_template(
            "password/auth_password_insert.html",
            erro_codigo=True
        )

    # Código correto
    session.pop(
        "codigo_recuperacao",
        None
    )

    session.pop(
        "expiracao_codigo",
        None
    )

    # Indica que o usuário foi autorizado
    session["recuperacao_autorizada"] = True

    # POST → GET
    return redirect(
        url_for(
            "pagina_recuperar_senha_redefinicao"
        )
    )


# GET
# Mostra a página para criar a nova senha
@app.route(
    "/password_recover/code/password_reset",
    methods=["GET"]
)
def pagina_recuperar_senha_redefinicao():

    # Impede acesso direto à página sem validar o código
    if not session.get("recuperacao_autorizada"):
        return redirect(
            url_for("pagina_recuperar_senha")
        )

    return render_template(
        "password/auth_password_reset.html"
    )


# POST
# Recebe a nova senha e atualiza no banco
@app.route(
    "/password_recover/code/password_reset",
    methods=["POST"]
)
def redefinir_senha():

    # Verifica se o usuário passou pela validação
    if not session.get("recuperacao_autorizada"):
        return redirect(
            url_for("pagina_recuperar_senha")
        )

    nova_senha = request.form.get(
        "new-password"
    )

    nova_senha_confirm = request.form.get(
        "confirm-password"
    )

    # Verifica se as senhas são iguais
    if nova_senha != nova_senha_confirm:

        return render_template(
            "password/auth_password_reset.html",
            erro_senha=True
        )

    # Recupera o e-mail salvo anteriormente
    email = session.get(
        "email_recuperacao"
    )

    # Atualiza a senha no banco
    sucesso = atualizar_senha(
        email,
        nova_senha
    )

    if sucesso:

        # Limpa os dados da recuperação
        session.pop(
            "email_recuperacao",
            None
        )

        session.pop(
            "recuperacao_autorizada",
            None
        )

        # POST → GET
        return redirect(
            url_for("pagina_recuperacao_sucesso")
        )

    return render_template(
        "password/auth_password_reset.html",
        erro_atualizacao=True
    )


# GET
# Página intermediária de sucesso
@app.route(
    "/password_recover/success",
    methods=["GET"]
)
def pagina_recuperacao_sucesso():

    return render_template(
        "password/auth_password_reset.html",
        senha_atualizada=True
    )


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)