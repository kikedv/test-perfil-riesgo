import streamlit as st
import smtplib
from email.mime.text import MIMEText

# --- CONFIGURACIÓN DEL EMAIL ---
ADMIN_EMAIL = "tucorreo@tudominio.com"      # Cambia esto por tu email
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SMTP_USER = "turemitente@gmail.com"         # Tu email de envío
SMTP_PASS = "tu_contraseña_o_app_password"  # Usa contraseña de aplicación si es Gmail

# --- ESTILOS CSS ---
st.markdown("""
    <style>
        html, body, [class*="css"]  {
            font-family: 'Helvetica Neue', sans-serif;
            color: #333333;
            background-color: #ffffff;
        }
        .block-container {
            padding: 2rem 2rem 2rem 2rem;
        }
        h1 {
            color: #222222;
            font-size: 2.8rem;
            margin-bottom: 0.5rem;
        }
        h2 {
            font-size: 1.4rem;
            color: #444444;
            margin-top: 0.5rem;
            margin-bottom: 2rem;
        }
        label {
            font-size: 1.2rem !important;
            font-weight: 500 !important;
        }
        .stButton>button {
            background-color: #d7a77a;
            color: white;
            border: none;
            padding: 0.6rem 1.5rem;
            font-size: 1.1rem;
            border-radius: 8px;
        }
        .stButton>button:hover {
            background-color: #c68f62;
        }
    </style>
""", unsafe_allow_html=True)

# --- FUNCIÓN PARA ENVIAR EMAIL ---
def send_email(user_email, score, result):
    subject = "Nuevo resultado del Test de Cartera Ideal"
    body = f"""\
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

# --- CÁLCULO DEL PERFIL DE RIESGO ---
def get_score(responses):
    total_score = 0
    num_questions = 10

    age = responses["Edad"]
    if age <= 20:
        total_score += 5
    elif age <= 30:
        total_score += 4
    elif age <= 50:
        total_score += 3
    elif age <= 65:
        total_score += 2
    else:
        total_score += 1

    total_score += 2 if responses["Personas a cargo"] else 5

    ocupacion_scores = {
        "Empresario con empleados": 5,
        "Autónomo por cuenta propia": 4,
        "Empleado contrato indefinido": 4,
        "Empleado contrato temporal": 2,
        "Jubilado": 1,
        "En paro": 2
    }
    total_score += ocupacion_scores[responses["Ocupación"]]

    horizonte_scores = {
        "10-20 años": 5,
        "Hasta 10 años": 4,
        "Hasta 5 años": 3,
        "Hasta 3 años": 2,
        "Menos de 1 año": 1
    }
    total_score += horizonte_scores[responses["Horizonte temporal"]]

    conocimiento_scores = {
        "Es mi profesión": 5,
        "Bastante experto": 4,
        "Conozco conceptos básicos": 3,
        "Casi nada": 2
    }
    total_score += conocimiento_scores[responses["Conocimiento financiero"]]

    reaccion_scores = {
        "Invertiría más dinero": 5,
        "No haría nada": 4,
        "Retiraría parte": 2,
        "Retiraría todo": 1
    }
    total_score += reaccion_scores[responses["Reacción a caída"]]

    total_score += 5 if responses["Rentabilidad o liquidez"] == "Máxima rentabilidad a largo plazo" else 1

    productos = responses["Productos financieros"]
    if "Productos derivados" in productos:
        total_score += 5
    elif "Acciones" in productos:
        total_score += 4
    elif "Fondos y ETFs" in productos:
        total_score += 3
    elif "Depósitos" in productos:
        total_score += 2
    else:
        total_score += 1

    volatilidad_scores = {
        "Lo conozco y lo asumo": 5,
        "Lo conozco pero prefiero evitarla": 3,
        "No lo conozco": 1
    }
    total_score += volatilidad_scores[responses["Volatilidad"]]

    bolsa_scores = {
        "Rentabilidad 10% y volatilidad 16%": 5,
        "Rentabilidad 20% y volatilidad 5%": 1,
        "No lo sé": 2
    }
    total_score += bolsa_scores[responses["Rentabilidad histórica"]]

    return total_score / num_questions

def get_result(score):
    if score >= 4.5:
        return "Tu perfil es **muy agresivo**. Te recomendamos las estrategias: **Agresiva y Dinámica**."
    elif score >= 3.5:
        return "Tu perfil es **dinámico**. Te recomendamos las estrategias: **Dinámica y Equilibrada**."
    elif score >= 2.5:
        return "Tu perfil es **equilibrado**. Te recomendamos las estrategias: **Equilibrada y Moderada**."
    elif score >= 1.5:
        return "Tu perfil es **moderado**. Te recomendamos las estrategias: **Moderada y Conservadora**."
    else:
        return "Tu perfil es **conservador**. Te recomendamos las estrategias: **Conservadora y Moderada**."

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

