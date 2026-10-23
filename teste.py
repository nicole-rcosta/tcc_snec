
from email.message import EmailMessage
import secrets
import smtplib

# linha que gera o código
codigo = f"{secrets.randbelow(100000):05d}"

# coloca um limite de 5 minutos segundos pra expirar
email = 'pablo.moralez@aluno.senai.br'

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

    # -----------------------------------------------------------------------

