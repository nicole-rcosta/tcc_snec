from flask import Flask, render_template, request, redirect, session, jsonify, url_for, flash
from model.extra_activity_register import cadastrar_atividade as ca, recuperar_atividade as ra, excluir_atividade as ea
from model.usuarios import cadastrar, logar, verificar_email, atualizar_senha, cadastrar
from static.utils.verification_password import verificar_senha_mestra as vsm
from model.class_register import recuperar_salas, adicionar_sala, deletar_sala
from model.students_register import recuperar_alunos, adicionar_aluno, deletar_aluno
from model.nutri_dashboard import recuperar_dados_dashboard, buscar_alunos_almoco_hoje, atualizar_status_almoco_aluno
from model.students_extra_register import recuperar_alunos_atividade, adicionar_aluno_atividade, excluir_aluno_atividade
from model.teacher_attendance_record import buscar_alunos, alunos_presentes, salvar_his_lanche, salvar_his_almoco, buscar_turmas, buscar_qntd_alunos, buscar_his_lanche
from model.adm_access import buscar_adm, buscar_usuario_pendente, rejeitar_usuario, aprovar_usuario
import secrets
import time
import pandas
from static.utils.send_email import enviar_email
from model.inserts_csv import inserir_excel_bcd

app = Flask(__name__)
app.secret_key = "snec_tcc_chave"

@app.route("/")

#Rota que exibe a página de login
@app.route("/login")
def pagina_login():
    return render_template("login/auth_login.html")

# Rota que envia os dados do formulário para fazer o login
@app.route("/login/post", methods=["POST"])
def logar_usuario():

    # Pega os dados do formulário e guarda em variáveis
    cpf = request.form.get("cpf-real")
    senha = request.form.get("password")

    # Define a senha mestra já criptografada
    senha_cript_mestra = "$2b$12$WpdfRGaObonrj/OnjmTHM.BcB73YWHLsf2KXQuN0h.hxgK6EJjd8W"

    # Verifica se o usuário é o administrador master e redireciona pra página de primeiro acesso
    if (cpf == '00000000000') and vsm(senha, senha_cript_mestra):
        return render_template("adm/admin_register.html")

    # Guarda o retorno da função logar dentro de uma variável
    resultado = logar(cpf, senha)

    # Verifica se o login foi bem sucedido e guarda o usuário na session
    if resultado.get('sucesso'):
        session['usuario'] = resultado.get('usuario')
        cargo = resultado['usuario']['cargo']
        # Redireciona o usuário à tela inicial do seu respectivo cargo
        if cargo == 'prof':
            return redirect('/teacher')
        elif cargo == 'nutri':
            return redirect('/nutri_dashboard')
        elif cargo == 'adm':
            return render_template("/adm/admin_item_register.html")
        
    # Caso a função de logar não tenha sido bem sucedida
    else:
        # Exibe mensagem de erro caso o CPF ou SENHA sejam inválidos
        if resultado.get('mensagem') == 'Aguarde a aprovação do administrador para efetivar o seu cadastro.' or resultado.get('mensagem') == 'CPF ou senha incorretos.':
            return render_template("login/auth_login.html", erro = resultado.get('mensagem'))
        # Exibe mensagem de erro caso o usuário não exista
        elif resultado.get('mensagem') == "Usuário não encontrado. Cadastre-se!":
            return redirect("/cadastro")
        else:
            pass

#Rota que exibe a página de cadastro
@app.route("/cadastro")
def pagina_cadastro():
    return render_template("/register/auth_register.html")

# Rota que envia os dados do formulário para fazer o cadastro
@app.route("/cadastro/post", methods=["POST"])
def cadastrar_usuario():

    # Pega os dados do formulário e guarda em variáveis
    nome = request.form.get("name")
    cpf = request.form.get("cpf-real")
    email = request.form.get("email")
    cargo = request.form.get("register")
    senha = request.form.get("password")
    status = "pendente"

    # Guarda o retorno da função cadastro dentro de uma variável
    cadastro_resp = cadastrar(nome, email, cargo, senha, cpf, status)

    # Verifica se o cadastro foi bem sucedido e redireciona o usuário pra página de login
    if cadastro_resp.get('sucesso'):
        return render_template("/login/auth_login.html")
    else:
    # Caso tenha erros no cadastro, exibe uma mensagem de erro  
        if cadastro_resp.get('mensagem') == "CPF inválido." or cadastro_resp.get('mensagem') == "CPF já cadastrado." or cadastro_resp.get('mensagem') == "Este email já pertence a um usuario.":
            return render_template("/register/auth_register.html", erro = cadastro_resp.get('mensagem'))
        else:
            return redirect("/cadastro")
    
# ---------------------------
# Paginas de Administrador
# ---------------------------

# Rota que exibe a página inicial de adm
@app.route("/adm")
def pagina_adm():
    usuario = session.get('usuario')
    if not usuario or usuario.get('cargo') != 'adm':
        return redirect("/login")

    nome = usuario.get('nome')
    return render_template("/adm/admin_item_register.html", nome_usuario=nome)

@app.route("/adm_register")
def pagina_adm_register():
    return render_template("/adm/admin_register.html")

# Rota que envia os dados do formulário para fazer o cadastro de primeiro acesso 
@app.route("/adm_register/post", methods=["POST"])
def cadastrar_adm():
    # Pega os dados do formulário e guarda em variáveis
    nome = request.form.get("name")
    cpf = request.form.get("cpf-real")
    email = request.form.get("email")
    senha = request.form.get("password")
    confirmar_senha = request.form.get("confirm-password")
    cargo = "adm"
    status = "aprovado"

    # Verifica se as senhas digitadas correspondem
    if senha == confirmar_senha:
        if cadastrar(nome, email, cargo, senha, cpf, status):
            return render_template("/login/auth_login.html")
        else:
            return redirect("/adm_register")
    else:
        flash("Digite a mesma senha para confirmar.")
        return redirect("/adm_register")
    
# Rota que exibe a página de cadastro de atividades
@app.route("/adm/reg_activity")
def pagina_cad_atividade():
    # Recupera as atividades e guarda em uma varíavel
    atividades = ra()
    return render_template("adm/admin_extra_activity_register.html", atividades=atividades)

# Rota que envia os dados da atividade para fazer o cadastro
@app.route("/adm/reg_activity/post", methods=["POST"])
def pagina_cad_atividades():

    # Pega os dados do formulário e guarda em variáveis
    ativid = request.form.get("activity_name")
    periodo = request.form.get("activity_period")

    # verifica se os campos estão preenchidos
    if ativid and periodo:

        # cadastra atividade
        ca(ativid, periodo)

    return redirect(url_for("pagina_cad_atividade"))
        
# Rota que deleta uma atividade de acordo com ID enviado
@app.route("/adm/exc_activity/<id_atividade>", methods=["POST"])
def excluir_atividades(id_atividade):

    # deleta atividade
    delete = ea(id_atividade)
    if delete.get('sucesso'):
        return redirect("/adm/reg_activity")
    else:

        # em caso de erros, exibe a mensagem de erro no terminal
        erro = delete.get('mensagem')
        flash(erro)
        return redirect("/adm/reg_activity")

#Rota que exibe a página de cadastrar sala
@app.route("/adm/reg_class")
def pagina_cad_sala():

    # Recupera salas cadastradas e guarda em uma variável
    salas = recuperar_salas()
    return render_template("adm/admin_room_register.html", salas = salas)

# Rota que envia os dados da sala para fazer o cadastro
@app.route("/adm/reg_class/post", methods=["POST"])
def pagina_cad_sala_post():

    # Pega os dados do formulário e guarda em variáveis
    turma= request.form.get("room_class")
    periodo= request.form.get("room_period")
    qnt_aluno= request.form.get("class_quantity")

    # Cadastra salas
    add_sala = adicionar_sala(turma=turma,periodo=periodo,qnt_alunos=qnt_aluno)

    if add_sala.get("sucesso"):
        return render_template("adm/admin_room_register.html", erro = add_sala.get("mensagem"))
    else:
        return redirect("/adm/reg_class")

# Rota que deleta uma sala de acordo com ID enviado
@app.route("/adm/reg_class/delete/<int:id>")
def pagina_cad_sala_del(id):

    # deleta sala
    delete = deletar_sala(id)
    if delete.get('sucesso'):
        return redirect("/adm/reg_class")

    # em caso de erros, exibe a mensagem de erro no terminal
    else:
        erro = delete.get('mensagem')
        flash(erro)
        return redirect("/adm/reg_class")

#Rota que exibe a página de cadastrar aluno
@app.route("/adm/reg_student")
def pagina_cad_aluno():

    # Recupera alunos cadastrados e guarda em uma variável
    alunos = recuperar_alunos()

    # Recupera salas cadastradas e guarda em uma variável
    salas = recuperar_salas()
    return render_template("adm/admin_student_register.html", alunos=alunos,salas=salas)

# Rota que envia os dados do aluno para fazer o cadastro
@app.route("/adm/reg_student/post", methods=["POST"])
def pagina_cad_aluno_post():

    # Pega os dados do formulário e guarda em variáveis
    rm = request.form.get("student_rm")
    nome_aluno = request.form.get("student_name")
    id_turma = request.form.get("student_class")

    # Cadastra o aluno
    adicionar_aluno(rm,nome_aluno,id_turma)

    return redirect("/adm/reg_student")

# Rota que deleta um estudante de acordo com ID enviado
@app.route("/adm/reg_student/delete/<int:id>")
def pagina_cad_aluno_delete(id):

    # deleta sala
    delete = deletar_aluno(id)
    if delete.get('sucesso'):
        return redirect("/adm/reg_student")

    # em caso de erros, exibe a mensagem de erro no terminal
    else:
        erro = delete.get('mensagem')
        flash(erro)
        return redirect("/adm/reg_student")

# Rota que cadastra alunos pela planilha do EXCEL
@app.route("/adm/reg_student/excel", methods=["POST"])
def pegar_excel_pag_student():

    # Pega o arquivo enviado pelo usuário e guarda dentro de uma variável
    arquivo = request.files.get('input_excel')

    # Chama a função de cadastrar e verifica se deu certo
    if inserir_excel_bcd(arquivo):
        return redirect("/adm/reg_student")

    # Exibe mensagem de erro caso não deu certo
    else:
        flash("Dados Inválidos! Verifique se elas existem ou se foram digitadas corretamente.")
        return redirect("/adm/reg_student")

# Rota que cadastra alunos pela planilha CSV
@app.route("/adm/reg_student/csv", methods=["POST"])
def pegar_csv_pag_student():

    # Pega o arquivo enviado pelo usuário e guarda dentro de uma variável
    arquivo = request.files.get('input_csv')

    # Chama a função de cadastrar e verifica se deu certo
    if inserir_excel_bcd(arquivo):
        return redirect("/adm/reg_student")

    # Exibe mensagem de erro caso não deu certo
    else:
        flash("Dados Inválidos! Verifique se elas existem ou se foram digitadas corretamente.")
        return redirect("/adm/reg_student")

# Rota que exibe a tela de cadastro dos alunos nas atividades
@app.route("/adm/reg_student_extra")
def pagina_cad_aluno_ativ():

    # Recupera os dados já cadastrados e guardam em uma variável
    alunos = recuperar_alunos()
    atividades= ra()
    alunos_atv = recuperar_alunos_atividade()
    return render_template("adm/admin_student_extra_register.html", alunos=alunos, atividades=atividades, alunos_atv=alunos_atv)

# Rota que cadastra os alunos nas atividades 
@app.route("/adm/reg_student_extra/post", methods=["POST"])
def pagina_cad_aluno_ativ_post():

    # Pega os dados dos formulários e guarda em variáveis
    rm = request.form.get("student_rm")
    id_atividade = request.form.get("student_activity")
    dia_semana = request.form.get("student_week-day")

    # cadastra aluno na atividade
    adicionar_aluno_atividade(rm,id_atividade,dia_semana)

    return redirect("/adm/reg_student_extra")

# Rota que deleta um estudante de acordo com ID enviado
@app.route("/adm/reg_student_extra/delete/<int:id>/<int:atividade>/<string:dia>")
def pagina_cad_aluno_ativ_delete(id,atividade,dia):

    # deleta sala
    excluir_aluno_atividade(id,atividade,dia)

    return redirect("/adm/reg_student_extra")

# Rota que verifica se o usuário é um admin para poder aprovar outros cargos
@app.route("/adm/conf_panel/post", methods=["POST"])
def verificar_adm():

    # Pega os dados do formulário e guarda em variáveis
    id_usuario = session.get("usuario")["id"]
    senha = request.form.get("password")
    busca_adm_resp = buscar_adm(id_usuario, senha)
    if busca_adm_resp.get("sucesso"):
        return redirect("/adm/adm_panel")

    # Em caso de erro exibe mensafgem na interface
    elif busca_adm_resp.get("mensagem") == "Senha incorreta!":
        return render_template("adm/admin_item_register.html", erro = busca_adm_resp.get("mensagem"))
    else:
        return redirect("/adm")

# Rota que exibe a tela de aprovação de usuário
@app.route("/adm/adm_panel")
def pagina_painel_adm():
    # Recupera usuários que ainda estão pendentes
    usuarios_pendentes = buscar_usuario_pendente().get("mensagem")
    return render_template("adm/admin_access.html", usuarios_pendentes = usuarios_pendentes)

# Rota que aprova usuário pelo id
@app.route("/adm/adm_panel/approve/<int:id>")
def pagina_painel_adm_aprovar(id):
    aprovar_usuario(id)
    return redirect("/adm/adm_panel")

# Rota que rejeita usuário pelo id
@app.route("/adm/adm_panel/reject/<int:id>")
def pagina_painel_adm_rejeitar(id):
    rejeitar_usuario(id)
    return redirect("/adm/adm_panel")


# ---------------------------
# Paginas de Nutricionista
# ---------------------------

# Rota que exibe o dashboard da nutricionista
@app.route("/nutri_dashboard")
def pagina_dashboard():
    # Chama a função que busca e processa os dados do MySQL
    dados = recuperar_dados_dashboard()


    nome_usuario = session.get("usuario", "Nutricionista")
       
    if dados.get("sucesso"):
        # Renderiza o HTML passando todas as variáveis necessárias
        return render_template(
            "nutri/nutritionist_dashboard.html",
            usuario=nome_usuario,
            turmas=dados.get("turmas", []),          
            total_lanches=dados.get("total_lanches", 0),
            total_almocos=dados.get("total_almocos", 0),
            todas_concluidas=dados.get("todas_concluidas", False))
    else:
        return render_template(
            "nutri/nutritionist_dashboard.html",
            erro=dados.get("mensagem"))
    
# Rota que exibe o dashboard de pessoas que vão ficar para o almoço
@app.route("/nutri_dashboard/report")
def pagina_dashboard_report():
    return render_template("nutri/nutritionist_report.html")

# ---------------------------
# ENDPOINTS REST API (Usados pelo arquivo nutritionist_report.js)
# ---------------------------

# json para renderizar os alunos para o almoço
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
    id_usuario = session.get("usuario")["id"]

    resultado = atualizar_status_almoco_aluno(rm_aluno, atendido, id_usuario)
    return jsonify(resultado)

# ---------------------------
# Paginas de Professor
# ---------------------------

# Rota que exibe página inicial de professor
@app.route("/teacher")
def pagina_prof_selecionar_sala():

    usuario = session.get('usuario')
   
    if not usuario or usuario.get('cargo') != 'prof':
        return redirect("/login")
    
    turmas = buscar_turmas()
    # Recupera turmas cadastradas e guarda em uma variável

    # verifica se a "Recuperação foi bem sucedida"
    if turmas.get("sucesso"):
        return render_template("teacher/teacher_class_select.html", turmas = turmas.get("turmas"))
    else:
        return render_template("teacher/teacher_class_select.html", erro = turmas.get("mensagem"))

# Rota que exibe informação da turma de acordo com o ID
@app.route("/teacher/class_info/<id_turma>")
def pagina_prof_registro(id_turma):

    usuario = session.get('usuario')
       
    if not usuario or usuario.get('cargo') != 'prof':
        return redirect("/login")

    # Recupera quantidade de alunos da turma
    qnt_alunos = buscar_qntd_alunos(id_turma).get("quantidade_alunos")

    # Recupera dados já cadastrados
    alunos = buscar_alunos(id_turma)
    his_lanche = buscar_his_lanche(id_turma)
    turmas = buscar_turmas()

    # Verifica se o processo foi bem sucedido para avançar para a próxima página
    if his_lanche.get("sucesso"):
        return render_template("teacher/teacher_class_select.html", turmas = turmas.get("turmas"), erro=his_lanche.get("mensagem"))
    else:
        if alunos.get("sucesso"):
            return render_template("teacher/teacher_attendance_record.html", id_turma=id_turma, qnt_alunos=qnt_alunos, alunos=alunos.get("alunos"))
        else:
            return render_template("teacher/teacher_attendance_record.html", id_turma=id_turma, qnt_alunos=qnt_alunos, erro=alunos.get("mensagem"))

# Rota que confirma as atividades da turma de acordo com o ID
@app.route("/teacher/class_info/confirm/<int:id_turma>", methods=['POST'])
def pagina_confirmacao_prof(id_turma):

    # Recupera informações já cadastradas
    qtd_alunos = request.form.get('quantidade_alunos')
    rms_contraturnos = request.form.getlist('rms_contraturnos')

    return render_template("teacher/teacher_attendance_confirm.html",
                           id_turma=id_turma,
                           qtd_alunos=qtd_alunos,
                           rms_contraturnos=rms_contraturnos)

# Rota que envia os dados inserido pelo professor para o banco de dados
@app.route("/teacher/class_info/save/<int:id_turma>", methods=['POST'])
def salvar_registro_prof(id_turma):
    # recupera os dados
    dados = request.get_json()
    qtd_alunos = dados.get('quantidade_alunos')
    rms_contraturnos = dados.get('rms_contraturno', [])  # Apenas os RMs marcados pelo professor
    id_usuario = session.get("usuario")["id"]

    # Executa a gravação no banco de dados
    sucesso = salvar_his_lanche(id_turma, qtd_alunos, id_usuario), salvar_his_almoco(id_usuario, rms_contraturnos)

    if sucesso:
        return jsonify({
            'sucesso': True, 
            'redirect_url': url_for('pagina_prof_selecionar_sala')
        }), 200
    else:
        return jsonify({
            'sucesso': False, 
            'erro': 'Não foi possível salvar o registro.'
        }), 500


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
    
    if enviar_email(email, codigo):
        return render_template("password/auth_password_insert.html")

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

@app.route("/logout")
def sair():
    session.clear()
    return redirect("/login")


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)