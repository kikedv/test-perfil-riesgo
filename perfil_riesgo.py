import streamlit as st

# Estilos CSS personalizados
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
            margin-bottom: 1rem;
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
        hr {
            margin-top: 2rem;
            margin-bottom: 2rem;
        }
    </style>
""", unsafe_allow_html=True)

# Funciones de cálculo y lógica
def get_score(responses):
    total_score = 0
    num_questions = 10

    # P1 Edad
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

    # P2 Personas a cargo
    total_score += 2 if responses["Personas a cargo"] else 5

    # P3 Ocupación
    ocupacion_scores = {
        "Empresario con empleados": 5,
        "Autónomo por cuenta propia": 4,
        "Empleado contrato indefinido": 4,
        "Empleado contrato temporal": 2,
        "Jubilado": 1,
        "En paro": 2
    }
    total_score += ocupacion_scores[responses["Ocupación"]]

    # P4 Horizonte temporal
    horizonte_scores = {
        "10-20 años": 5,
        "Hasta 10 años": 4,
        "Hasta 5 años": 3,
        "Hasta 3 años": 2,
        "Menos de 1 año": 1
    }
    total_score += horizonte_scores[responses["Horizonte temporal"]]

    # P5 Conocimiento financiero
    conocimiento_scores = {
        "Es mi profesión": 5,
        "Bastante experto": 4,
        "Conozco conceptos básicos": 3,
        "Casi nada": 2
    }
    total_score += conocimiento_scores[responses["Conocimiento financiero"]]

    # P6 Reacción a caída del mercado
    reaccion_scores = {
        "Invertiría más dinero": 5,
        "No haría nada": 4,
        "Retiraría parte": 2,
        "Retiraría todo": 1
    }
    total_score += reaccion_scores[responses["Reacción a caída"]]

    # P7 Rentabilidad o liquidez
    total_score += 5 if responses["Rentabilidad o liquidez"] == "Máxima rentabilidad a largo plazo" else 1

    # P8 Productos financieros
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

    # P9 Volatilidad
    volatilidad_scores = {
        "Lo conozco y lo asumo": 5,
        "Lo conozco pero prefiero evitarla": 3,
        "No lo conozco": 1
    }
    total_score += volatilidad_scores[responses["Volatilidad"]]

    # P10 Rentabilidad histórica
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

# Interfaz del test
def main():
    st.title("Test de Perfil de Riesgo del Inversor")
    st.markdown("""
    ¿Quieres saber qué estrategia de inversión se adapta mejor a tu perfil?  
    Responde estas 10 preguntas y descubre cuál es tu tolerancia al riesgo.
    """)
    
    st.markdown("---")

    responses = {}
    responses["Edad"] = st.number_input("1. ¿Qué edad tienes?", min_value=0, max_value=120, value=35)
    responses["Personas a cargo"] = st.radio("2. ¿Tienes personas a tu cargo?", ["Sí", "No"]) == "Sí"
    responses["Ocupación"] = st.selectbox("3. ¿Cuál es tu ocupación actual?", [
        "Empresario con empleados", "Autónomo por cuenta propia", 
        "Empleado contrato indefinido", "Empleado contrato temporal", 
        "Jubilado", "En paro"
    ])
    responses["Horizonte temporal"] = st.selectbox("4. ¿Cuánto tiempo puedes invertir sin tocar el dinero?", [
        "10-20 años", "Hasta 10 años", "Hasta 5 años", "Hasta 3 años", "Menos de 1 año"
    ])
    responses["Conocimiento financiero"] = st.selectbox("5. ¿Cuánto sabes de finanzas?", [
        "Es mi profesión", "Bastante experto", "Conozco conceptos básicos", "Casi nada"
    ])
    responses["Reacción a caída"] = st.radio("6. Si la bolsa cae un 10%, ¿qué harías?", [
        "Invertiría más dinero", "No haría nada", "Retiraría parte", "Retiraría todo"
    ])
    responses["Rentabilidad o liquidez"] = st.radio("7. A la hora de rentabilizar tu patrimonio, prefieres:", [
        "Máxima rentabilidad a largo plazo", "Disposición del dinero en todo momento"
    ])
    responses["Productos financieros"] = st.multiselect("8. ¿Qué productos financieros has tenido?", [
        "Productos derivados", "Fondos y ETFs", "Acciones", "Depósitos", "Cuentas corrientes"
    ])
    responses["Volatilidad"] = st.selectbox("9. ¿Qué opinas de la volatilidad?", [
        "Lo conozco y lo asumo", "Lo conozco pero prefiero evitarla", "No lo conozco"
    ])
    responses["Rentabilidad histórica"] = st.selectbox("10. ¿Cuál de estas afirmaciones refleja mejor la rentabilidad histórica de la bolsa americana?", [
        "Rentabilidad 10% y volatilidad 16%", "Rentabilidad 20% y volatilidad 5%", "No lo sé"
    ])

    st.markdown("---")

    if st.button("Ver mi perfil de riesgo"):
        score = get_score(responses)
        result = get_result(score)
        st.markdown(f"### Resultado: {round(score, 2)} / 5")
        st.markdown(result)

if __name__ == "__main__":
    main()
