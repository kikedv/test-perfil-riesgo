import streamlit as st
import smtplib
from email.mime.text import MIMEText

# --- CONFIGURACIÓN EMAIL ---
ADMIN_EMAIL = "noresponder@school.socairepatrimonios.com"
SMTP_SERVER = "smtp.mailgun.org"
SMTP_PORT = 465
SMTP_USER = "noresponder@school.socairepatrimonios.com"
SMTP_PASS = ""

# --- FUNCIONES DE LÓGICA ---
def get_score(responses):
    # ... (idéntica a la anterior, omitida para simplificar)
    # Aquí va la misma función que ya tenías para calcular el perfil
    pass

def get_result(score):
    # ... (idéntica a la anterior)
    pass

def send_email(user_email, score, result):
    subject = "Nuevo resultado del Test de Cartera Ideal"
    body = f"""
    El siguiente usuario ha realizado el test de perfil de riesgo.

    Email: {user_email}
    Resultado: {round(score, 2)} / 5
    Recomendación: {result}
    """
    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = SMTP_USER
    msg["To"] = ADMIN_EMAIL

    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_USER, SMTP_PASS)
            server.send_message(msg)
        return True
    except Exception as e:
        print("Error al enviar correo:", e)
        return False

# --- INTERFAZ ---
def main():
    st.title("Test para conocer tu cartera ideal")
    st.markdown("<h2>¿Quieres saber qué estrategia de inversión se adapta mejor a ti? Responde a estas 10 preguntas y ¡descúbrelo!</h2>", unsafe_allow_html=True)
    st.markdown("---")

    responses = {}
    responses["Edad"] = st.number_input("¿Qué edad tienes?", min_value=0, max_value=120, value=35)
    responses["Personas a cargo"] = st.radio("¿Tienes personas a tu cargo?", ["Sí", "No"]) == "Sí"
    responses["Ocupación"] = st.selectbox("¿Cuál es tu ocupación actual?", [
        "Empresario con empleados", "Autónomo por cuenta propia", 
        "Empleado contrato indefinido", "Empleado contrato temporal", 
        "Jubilado", "En paro"
    ])
    responses["Horizonte temporal"] = st.selectbox("¿Cuánto tiempo puedes invertir sin tocar el dinero?", [
        "10-20 años", "Hasta 10 años", "Hasta 5 años", "Hasta 3 años", "Menos de 1 año"
    ])
    responses["Conocimiento financiero"] = st.selectbox("¿Cuánto sabes de finanzas?", [
        "Es mi profesión", "Bastante experto", "Conozco conceptos básicos", "Casi nada"
    ])
    responses["Reacción a caída"] = st.radio("Si la bolsa cae un 10%, ¿qué harías?", [
        "Invertiría más dinero", "No haría nada", "Retiraría parte", "Retiraría todo"
    ])
    responses["Rentabilidad o liquidez"] = st.radio("A la hora de rentabilizar tu patrimonio, prefieres:", [
        "Máxima rentabilidad a largo plazo", "Disposición del dinero en todo momento"
    ])
    responses["Productos financieros"] = st.multiselect("¿Qué productos financieros has tenido?", [
        "Productos derivados", "Fondos y ETFs", "Acciones", "Depósitos", "Cuentas corrientes"
    ])
    responses["Volatilidad"] = st.selectbox("¿Qué opinas de la volatilidad?", [
        "Lo conozco y lo asumo", "Lo conozco pero prefiero evitarla", "No lo conozco"
    ])
    responses["Rentabilidad histórica"] = st.selectbox("¿Cuál de estas afirmaciones refleja mejor la rentabilidad histórica de la bolsa americana?", [
        "Rentabilidad 10% y volatilidad 16%", "Rentabilidad 20% y volatilidad 5%", "No lo sé"
    ])

    st.markdown("---")
    user_email = st.text_input("Introduce tu correo electrónico para recibir tu perfil y recomendación:")

    if st.button("Enviar mi perfil"):
        score = get_score(responses)
        result = get_result(score)

        if user_email:
            success = send_email(user_email, score, result)
            if success:
                st.success("Tu perfil ha sido enviado correctamente. ¡Gracias!")
                st.markdown(f"### Resultado: {round(score, 2)} / 5")
                st.markdown(result)
            else:
                st.error("Hubo un error al enviar tu perfil. Por favor, intenta más tarde.")
        else:
            st.warning("Por favor, introduce tu correo electrónico.")

if __name__ == "__main__":
    main()
