from flask import Flask, render_template, request, redirect, session, jsonify, flash, url_for
from model.extra_activity_register import cadastrar_atividade as ca, recuperar_atividade as ra, excluir_atividade as ea
from model.usuarios import cadastrar, logar
from model.usuarios import verificar_email
from model.usuarios import atualizar_senha
from static.utils.verification_password import verificar_senha_mestra as vsm
import bcrypt
from model.usuarios import cadastrar
from model.class_register import recuperar_salas
from model.class_register import adicionar_sala
from model.class_register import deletar_sala
from model.students_register import recuperar_alunos
from model.students_register import adicionar_aluno
from model.students_register import deletar_aluno
from model.nutri_dashboard import recuperar_dados_dashboard
from model.students_extra_register import recuperar_alunos_atividade
from model.students_extra_register import adicionar_aluno_atividade
from model.students_extra_register import excluir_aluno_atividade
from model.nutritionist_report import buscar_alunos_almoco_hoje, atualizar_status_almoco_aluno
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

    senha_cript_mestra = "$2b$12$WpdfRGaObonrj/OnjmTHM.BcB73YWHLsf2KXQuN0h.hxgK6EJjd8W"

    if (cpf == '00000000000') and vsm(senha, senha_cript_mestra):
        return render_template("adm/admin_register.html")

    resultado = logar(cpf, senha)

    if resultado['sucesso']:
        session['usuario'] = resultado['usuario']
        cargo = resultado['usuario']['cargo']

        if cargo == 'prof':
            return redirect('/teacher')

        elif cargo == 'nutri':
            return redirect('/nutri_dashboard')

        elif cargo == 'adm':
            return render_template("/adm/admin_item_register.html")

        return render_template()

    elif resultado.get('erro_login'):
        return render_template(
            "login/auth_login.html",
            erro_login=True
        )

    elif resultado.get('erro_aprovacao'):
        return render_template(
            "login/auth_login.html",
            erro_aprovacao=True
        )

    elif resultado.get('erro_servidor'):
        return render_template(
            "login/auth_login.html",
            erro_servidor=True
        )

@app.route("/cadastro")
def pagina_cadastro():
    return render_template("/register/auth_register.html")
@app.route("/cadastro/post", methods=["POST"])
def cadastrar_usuario():
    nome = request.form.get("name")
    cpf = request.form.get("cpf")
    email = request.form.get("email")
    cargo = request.form.get("register")
    senha = request.form.get("password")
    status = "pendente"

    resultado = cadastrar(nome, email, cargo, senha, cpf, status)

    if resultado["sucesso"]:
        return render_template("/login/auth_login.html")

    elif resultado.get("erro_cadastro_vazio"):
        return render_template(
            "/register/auth_register.html",
            erro_cadastro_vazio=True
        )

    elif resultado.get("erro_cpf"):
        return render_template(
            "/register/auth_register.html",
            erro_cpf=True
        )

    elif resultado.get("erro_cadastro_existente"):
        return render_template(
            "/register/auth_register.html",
            erro_cadastro_existente=True
        )

    elif resultado.get("erro_servidor"):
        return render_template(
            "/register/auth_register.html",
            erro_servidor=True
        )
    
# ---------------------------
# Paginas de Administrador
# ---------------------------

@app.route("/adm")
def pagina_adm():
    return render_template("/adm/admin_item_register.html")


@app.route("/adm_register")
def pagina_adm_register():
    return render_template("/adm/admin_register.html")


@app.route("/adm_register/post", methods=["POST"])
def cadastrar_adm():
    nome = request.form.get("name")
    cpf = request.form.get("cpf")
    email = request.form.get("email")
    senha = request.form.get("password")
    confirmar_senha = request.form.get("confirm-password")
    cargo = "adm"
    status = "aprovado"

    if senha == confirmar_senha:
        if cadastrar(nome, email, cargo, senha, cpf, status):
            return render_template("/login/auth_login.html")
        else:
            return redirect("/adm_register")
    else:
        return redirect("/adm_register")

@app.route("/adm/reg_activity")
def pagina_cad_atividade():
    atividades = ra()
    return render_template("adm/admin_extra_activity_register.html", atividades=atividades)


@app.route("/adm/reg_activity/post", methods=["POST"])
def pagina_cad_atividades():
    ativid = request.form.get("activity_name")
    periodo = request.form.get("activity_period")

    resultado = ca(ativid, periodo)

    if resultado["sucesso"]:
        return redirect(url_for("pagina_cad_atividade"))

    elif resultado.get("erro_atividade_vazia"):
        return render_template(
            "adm/admin_extra_activity_register.html",
            erro_atividade_vazia=True
        )

    elif resultado.get("erro_atividade_existente"):
        return render_template(
            "adm/admin_extra_activity_register.html",
            erro_atividade_existente=True
        )

    elif resultado.get("erro_servidor"):
        return render_template(
            "adm/admin_extra_activity_register.html",
            erro_servidor=True
        )

        

@app.route("/adm/exc_activity/<id_atividade>", methods=["POST"])
def excluir_atividades(id_atividade):
    
    ea(id_atividade)
    return redirect(url_for("pagina_cad_atividade"))



@app.route("/adm/reg_class")
def pagina_cad_sala():
    salas = recuperar_salas()
    print(salas)
    return render_template("adm/admin_room_register.html", salas = salas)

@app.route("/adm/reg_class/post", methods=["POST"])
def pagina_cad_sala_post():
    turma = request.form.get("room_class")
    periodo = request.form.get("room_period")
    qnt_aluno = request.form.get("class_quantity")

    resultado = adicionar_sala(
        turma=turma,
        periodo=periodo,
        qnt_alunos=qnt_aluno
    )

    if resultado["sucesso"]:
        return redirect("/adm/reg_class")

    elif resultado.get("erro_sala_vazia"):
        return render_template(
            "/adm/admin_room_register.html",
            erro_sala_vazia=True
        )

    elif resultado.get("erro_turma_existente"):
        return render_template(
            "/adm/admin_room_register.html",
            erro_turma_existente=True
        )

    elif resultado.get("erro_servidor"):
        return render_template(
            "/adm/admin_room_register.html",
            erro_servidor=True
        )



@app.route("/adm/reg_class/delete/<int:id>")
def pagina_cad_sala_del(id):
    deletar_sala(id)
    return redirect("/adm/reg_class")

    



@app.route("/adm/reg_student")
def pagina_cad_aluno():
    alunos = recuperar_alunos()
    salas = recuperar_salas()
    return render_template("adm/admin_student_register.html", alunos=alunos,salas=salas)

@app.route("/adm/reg_student/post", methods=["POST"])
def pagina_cad_aluno_post():

    rm = request.form.get("student_rm")
    nome_aluno = request.form.get("student_name")
    id_turma = request.form.get("student_class")

    resultado = adicionar_aluno(
        rm,
        nome_aluno,
        id_turma
    )

    if resultado["sucesso"]:
        return redirect("/adm/reg_student")

    elif resultado.get("erro_aluno_vazio"):
        return render_template(
            "adm/admin_student_register.html",
            erro_aluno_vazio=True
        )

    elif resultado.get("erro_aluno_existente"):
        return render_template(
            "adm/admin_student_register.html",
            erro_aluno_existente=True
        )

    elif resultado.get("erro_servidor"):
        return render_template(
            "adm/admin_student_register.html",
            erro_servidor=True
        )



@app.route("/adm/reg_student/delete/<int:id>")
def pagina_cad_aluno_delete(id):

    deletar_aluno(id)

    return redirect("/adm/reg_student")




@app.route("/adm/reg_student_extra")
def pagina_cad_aluno_ativ():
    alunos = recuperar_alunos()
    atividades= ra()
    alunos_atv = recuperar_alunos_atividade()
    return render_template("adm/admin_student_extra_register.html", alunos=alunos, atividades=atividades, alunos_atv=alunos_atv)


@app.route("/adm/reg_student_extra/post", methods=["POST"])
def pagina_cad_aluno_ativ_post():

    rm = request.form.get("student_rm")
    id_atividade = request.form.get("student_activity")
    dia_semana = request.form.get("student_week-day")

    resultado = adicionar_aluno_atividade(
        rm,
        id_atividade,
        dia_semana
    )

    if resultado["sucesso"]:
        return redirect("/adm/reg_student_extra")

    elif resultado.get("erro_aluno_atividade_vazio"):
        return render_template(
            "adm/admin_student_extra_register.html",
            erro_aluno_atividade_vazio=True
        )

    elif resultado.get("erro_aluno_atividade_existente"):
        return render_template(
            "adm/admin_student_extra_register.html",
            erro_aluno_atividade_existente=True
        )

    elif resultado.get("erro_servidor"):
        return render_template(
            "adm/admin_student_extra_register.html",
            erro_servidor=True
        )


@app.route("/adm/reg_student_extra/delete/<int:id>/<int:atividade>/<string:dia>")
def pagina_cad_aluno_ativ_delete(id,atividade,dia):

    excluir_aluno_atividade(id,atividade,dia)

    return redirect("/adm/reg_student_extra")


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
    # Chama a função que busca e processa os dados do MySQL
    dados = recuperar_dados_dashboard()
    
    # Pega o nome do usuário da sessão ou define um padrão
    nome_usuario = session.get("usuario_nome", "Nutricionista")

    # Renderiza o HTML passando todas as variáveis necessárias
    return render_template(
        "nutri/nutritionist_dashboard.html",
        usuario=nome_usuario,
        turmas=dados["turmas"],
        total_lanches=dados["total_lanches"],
        total_almocos=dados["total_almocos"],
        todas_concluidas=dados["todas_concluidas"]
    )

    

@app.route("/nutri_dashboard/report")
def pagina_dashboard_report():
    return render_template("nutri/nutritionist_report.html")

# ---------------------------
# ENDPOINTS REST API (Usados pelo arquivo nutritionist_report.js)
# ---------------------------

@app.route("/api/nutri/alunos-almoco", methods=["GET"])
def api_alunos_almoco():
    """Retorna a lista de alunos do dia em formato JSON para o JS renderizar a tabela."""
    dados = buscar_alunos_almoco_hoje()
    return jsonify(dados)

@app.route("/api/nutri/atualizar-almoco", methods=["POST"])
def api_atualizar_almoco():
    """Recebe o clique no checkbox da tabela e atualiza a presenca no MySQL."""
    dados = request.get_json()

    if not dados or "rm" not in dados or "atendido" not in dados:
        return jsonify({"sucesso": False, "mensagem": "Dados incompletos"}), 400

    rm_aluno = dados.get("rm")
    atendido = dados.get("atendido")

    # Obtém o ID do usuário conectado na sessão (se houver login)
    usuario_sessao = session.get("usuario", {})
    id_usuario = usuario_sessao.get("id_usuario", None)

    resultado = atualizar_status_almoco_aluno(rm_aluno, atendido, id_usuario)
    return jsonify(resultado)

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
    
    # linha que gera o código
    codigo = f"{secrets.randbelow(100000):05d}"

    session["codigo_recuperacao"] = codigo

    # coloca um limite de 5 minutos segundos pra expirar
    session["expiracao_codigo"] = time.time() + 300

    email = request.form.get("email")
    session["email_recuperacao"] = email

    # verifica se o email existe
    if not verificar_email(email):
        return render_template(
            "password/auth_password_recover.html",
            erro_email=True
        )

    # se existir segue ess logica:
    
    # Dados da conta
    EMAIL_REMETENTE = "pablolorenzomoralez@gmail.com"
    # tomar cuidado com isso
    SENHA_APP = "mtls ntmg kxxn aquu" 
    DESTINATARIO = email

    email = EmailMessage()
    email["Subject"] = "Código de Recuperação de senha"
    email["From"] = EMAIL_REMETENTE
    email["To"] = DESTINATARIO

    email.set_content(f'''
    Confirme seu e-mail

    Use este código no snec pra confirmar que este e-mail é seu:

    {codigo}

    ''')

    # Conectando ao Gmail e enviando

    try:
        with smtplib.SMTP("smtp.gmail.com", 587, timeout=3) as servidor:
            servidor.starttls()
            servidor.login(EMAIL_REMETENTE, SENHA_APP)

            print("Enviando e-mail...", flush=True)
            servidor.send_message(email)

            print("E-mail enviado com sucesso!", flush=True)

    except (smtplib.SMTPException, TimeoutError, OSError) as erro:
        print(f"Envio não confirmado: {erro}", flush=True)

    finally:
        print("Programa encerrado.", flush=True)
        
        return  render_template("password/auth_password_insert.html")

#página onde o usuário informa o código
@app.route("/password_recover/code", methods=["GET"])
def pagina_recuperar_senha_codigo():
    return render_template(
        "password/auth_password_insert.html"
    )



# recebe e valida o código
@app.route("/password_recover/code", methods=["POST"])
def verificar_codigo():

    codigo = session.get("codigo_recuperacao")
    expiracao = session.get("expiracao_codigo", 0)

    if not codigo:
        return "<h2>Nenhum código foi gerado!</h2>"

    # ve se o código expirou
    if time.time() >= expiracao:
        session.pop("codigo_recuperacao", None)
        session.pop("expiracao_codigo", None)

        return render_template(
                    "password/auth_password_insert.html",
                    codigo_expirado=True
                )

    
    codigo_digitado = request.form.get("codigo-completo")
    # ve se o código está correto
    if codigo_digitado == codigo:
        session.pop("codigo_recuperacao", None)
        session.pop("expiracao_codigo", None)
        session["recuperacao_autorizada"] = True
        return redirect(url_for("pagina_recuperar_senha_redefinicao"))

    return render_template(
                        "password/auth_password_insert.html",
                        erro_codigo=True
                    )
    

# mostra a página para criar a nova senha
@app.route(
    "/password_recover/code/password_reset",
    methods=["GET"]
)
def pagina_recuperar_senha_redefinicao():

    # impede acesso a página sem ve o código
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

       
        session.pop("email_recuperacao",None)

        session.pop("recuperacao_autorizada",None)

     
        return redirect(
            url_for("pagina_recuperacao_sucesso")
        )

    return render_template(
        "password/auth_password_reset.html",
        erro_atualizacao=True
    )



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