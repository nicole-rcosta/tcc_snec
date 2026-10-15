from flask import Flask, render_template, request, redirect, session, jsonify, flash, url_for
from model.extra_activity_register import cadastrar_atividade as ca, recuperar_atividade as ra, excluir_atividade as ea
from model.usuarios import cadastrar, logar
from model.salas import recuperar_salas
from model.salas import adicionar_sala
from model.salas import deletar_sala
import mysql
import mysql.connector

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
        return redirect("/")
    
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

# ---------------------------
# Paginas de Recuperar Senha
# ---------------------------

@app.route("/password_recover")
def pagina_recuperar_senha():
    return render_template("password/auth_password_recover.html")

@app.route("/password_recover/code")
def pagina_recuperar_senha_codigo():
    return render_template("password/auth_password_insert.html")

@app.route("/password_recover/code/password_reset")
def pagina_recuperar_senha_redefinicao():
    return render_template("password/auth_password_reset.html")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)