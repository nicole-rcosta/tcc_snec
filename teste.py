from email.message import EmailMessage
import secrets
import smtplib

# linha que gera o código
codigo = f"{secrets.randbelow(100000):05d}"

# coloca um limite de 5 minutos segundos pra expirar
email_destino = 'pablo.moralez@aluno.senai.br'

# Dados da conta
EMAIL_REMETENTE = "pablolorenzomoralez@gmail.com"
SENHA_APP = "mtls ntmg kxxn aquu" 
DESTINATARIO = email_destino

# ATENÇÃO: Sem o 'f' antes das aspas triplas!
corpo_html = """
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Código de Verificação SNEC</title>
    <style>
        body, table, td, a { -webkit-text-size-adjust: 100%; -ms-text-size-adjust: 100%; }
        table, td { mso-table-lspace: 0pt; mso-table-rspace: 0pt; }
        img { -ms-interpolation-mode: bicubic; border: 0; height: auto; line-height: 100%; outline: none; text-decoration: none; }
        table { border-collapse: collapse !important; }
        body { height: 100% !important; margin: 0 !important; padding: 0 !important; width: 100% !important; background-color: #EBEBF5; }
        
        @media screen and (max-width: 600px) {
            .container { width: 100% !important; }
            .code-box { width: 90% !important; }
            .mobile-hide { display: none !important; }
            .mobile-padding { padding-left: 20px !important; padding-right: 20px !important; }
        }
    </style>
</head>
<body style="background-color: #EBEBF5; margin: 0; padding: 0; font-family: Arial, Helvetica, sans-serif;">

    <table border="0" cellpadding="0" cellspacing="0" width="100%" style="background-color: #EBEBF5;">
        <tr>
            <td align="center" style="padding: 40px 0;">
                
                <table border="0" cellpadding="0" cellspacing="0" width="600" class="container" style="background-color: #EBEBF5; border-collapse: collapse; position: relative;">
                    
                    <tr>
                        <td style="position: relative; padding-bottom: 30px;">
                            
                            <img src="https://www.image2url.com/r2/default/images/1792763792509-2e596ac9-1fc4-4abf-8dc2-7b08b4c0bfe5.png" 
                            alt="" width="80" style="display: block; position: absolute; top: -10px; left: -10px; z-index: 1;">
                            
                            <img src="https://www.image2url.com/r2/default/images/1792763859654-ec6d99ca-3456-4e23-abf2-8e6e710d038c.png" 
                            alt="" width="100" style="display: block; position: absolute; top: -20px; right: -10px; z-index: 1;">

                            <div style="text-align: center; position: relative; z-index: 2; padding-top: 10px;">
                                <img src="https://www.image2url.com/r2/default/images/1792764273211-a3633454-5845-4673-a054-5cb9a9444cfb.png" alt="SNEC" width="180" style="display: inline-block;">
                            </div>
                        </td>
                    </tr>

                    <tr>
                        <td align="center" class="mobile-padding" style="padding: 0 40px 20px 40px;">
                            <h1 style="color: #4A4A8A; font-size: 22px; font-weight: bold; margin: 0; line-height: 1.4; text-align: center;">
                                O seu código de verificação<br>é:
                            </h1>
                        </td>
                    </tr>

                    <tr>
                        <td align="center" style="padding: 0 20px 40px 20px;">
                            <table border="0" cellpadding="0" cellspacing="0" width="80%" class="code-box" style="background-color: #FFFFFF; border-radius: 16px; box-shadow: 0 4px 10px rgba(0,0,0,0.05);">
                                <tr>
                                    <td align="center" style="padding: 30px 20px;">
                                        <span style="color: #FF7043; font-size: 48px; font-weight: bold; letter-spacing: 4px; font-family: Arial, Helvetica, sans-serif;">
                                            CODIGO_AQUI
                                        </span>
                                    </td>
                                </tr>
                            </table>
                        </td>
                    </tr>

                    <tr>
                        <td style="position: relative; height: 80px;">
                            <img src="https://www.image2url.com/r2/default/images/1792763753025-fa070329-097e-47eb-af19-47cd79358578.png" alt="" width="90" style="display: block; position: absolute; bottom: -20px; left: -10px;">
                            
                            <img src="https://www.image2url.com/r2/default/images/1792763607322-42332d77-0f37-4958-ad0b-3757da6783e0.png" alt="" width="120" style="display: block; position: absolute; bottom: -10px; right: -10px;">
                        </td>
                    </tr>

                </table>

            </td>
        </tr>
    </table>

</body>
</html>
"""

# Substitui o texto CODIGO_AQUI pelo código gerado
corpo_html = corpo_html.replace("CODIGO_AQUI", codigo)

email = EmailMessage()
email["Subject"] = "Código de Recuperação de senha"
email["From"] = EMAIL_REMETENTE
email["To"] = DESTINATARIO

email.set_content(f"Use este código no SNEC para confirmar que este e-mail é seu: {codigo}")
email.add_alternative(corpo_html, subtype='html')

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