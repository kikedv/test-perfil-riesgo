# -*- coding: utf-8 -*-
"""
Editor de Spyder

Este es un archivo temporal.
"""


import streamlit as st
import numpy_financial as npf
import matplotlib.pyplot as plt
import pandas as pd

# Fórmulas adicionales
def calculate_final_value(current_value, inflation, years):
    return current_value * (1 + inflation / 100) ** years

def calculate_net_value(final_value, tax_rate):
    return final_value / (1 - tax_rate / 100)

def calculate_annual_savings(rate, years, initial_capital, net_goal):
    return abs(npf.pmt(rate / 100, years, -initial_capital, net_goal, 0))

def calculate_annual_savings_with_increase(rate, increase_rate, years, initial_capital, net_goal):
    rate = rate / 100
    increase_rate = increase_rate / 100

    if rate == increase_rate:
        return (net_goal - (initial_capital * (1 + rate) ** years)) / (years * (1 + rate) ** years)

    numerator = net_goal - (initial_capital * (1 + rate) ** years)
    denominator = (
        ((1 - ((1 + increase_rate) / (1 + rate)) ** years) / (rate - increase_rate))
        * (1 + rate) ** years
    )
    return numerator / denominator if denominator != 0 else 0

# Título
st.title("¿Cuánto necesito ahorrar todos los meses para conseguir mis objetivos?")

# Párrafo inicial
parrafo_inicial = (
    "Esta herramienta te ayudará para saber grosso modo cuánto tienes que ahorrar e invertir cada mes "
    "(y cada año) para alcanzar un determinado objetivo económico. Es una orientación, una ayuda. "
    "Completa los siguientes campos y observa qué te sugieren las matemáticas."
)
st.markdown(parrafo_inicial)

# Entradas del usuario
st.header("Datos del Cálculo")

current_value = st.number_input("Importe actual del objetivo:", min_value=0.0, step=1000.0)
initial_capital = st.number_input("Capital inicial:", min_value=0.0, step=1000.0)
years = st.number_input("Número de años:", min_value=1, step=1)
inflation = st.number_input("Inflación promedio estimada (%):", min_value=0.0, step=0.1)
tax_rate = st.number_input("Impuestos estimados sobre las ganancias (%):", min_value=0.0, step=0.1)

# Datos de la Inversión
st.header("Datos de la Inversión")
st.markdown(
    "Ahora introduce la rentabilidad promedio anual que esperas alcanzar con tu estrategia de inversión. "
    "En la sección de carteras modelo, tienes varias propuestas que te indican la rentabilidad estimada en "
    "base a cómo se han comportado en el pasado. Introduce también un porcentaje de incremento anual del "
    "ahorro que destinarás a la inversión. Sería importante que lo introdujeras porque eso querrá decir "
    "que todos los años tratarás de incrementar tus aportaciones en ese porcentaje para alimentar más a tu máquina de hacer dinero."
)
expected_rate = st.number_input("Rentabilidad esperada de la inversión (%):", min_value=0.0, step=0.1)
annual_increase = st.number_input("Incremento ahorro anual (%):", min_value=0.0, step=0.1)

# Botón CALCULAR
if st.button("CALCULAR"):
    if current_value > 0 and inflation >= 0 and years > 0 and tax_rate >= 0 and expected_rate > 0:
        # Cálculo del gran capital y gran capital neto
        final_value = calculate_final_value(current_value, inflation, years)
        net_value = calculate_net_value(final_value, tax_rate)

        texto_resultado = (
            f"En base a estos datos, el importe que debes alcanzar es {final_value:,.2f}. "
            f"Sin embargo, como Hacienda te quitará una parte de los beneficios, deberás alcanzar un capital algo mayor. "
            f"Ese GRAN CAPITAL es de {net_value:,.2f}."
        )
        st.markdown(texto_resultado)

        # Cálculo del ahorro sin incremento anual (corregido con abs())
        annual_savings = abs(calculate_annual_savings(expected_rate, years, initial_capital, net_value))
        monthly_savings = annual_savings / 12

        # Cálculo del ahorro con incremento anual
        annual_savings_increase = calculate_annual_savings_with_increase(
            expected_rate, annual_increase, years, initial_capital, net_value
        )
        monthly_savings_increase = annual_savings_increase / 12

        # Resumen
        resumen = (
            f"¿Qué quiere decir todo lo que hemos calculado? Muy fácil, para alcanzar tu objetivo, tienes que alcanzar un GRAN CAPITAL de {net_value:,.2f} "
            f"dentro de {years} años. Para lograr ese objetivo, y suponiendo que ejecutes una estrategia de inversión que te proporcione un {expected_rate:.2f}% "
            f"de rentabilidad anual promedio, tendrás que ahorrar e invertir cada mes un monto de {monthly_savings:,.2f} o, en términos anuales, {annual_savings:,.2f}. "
            f"Ahora bien, si haces el esfuerzo de incrementar todos los años tus aportaciones en un {annual_increase:.2f}%, la cantidad mensual y anual varía en el "
            f"primer año. Ahora tendrás que ahorrar e invertir ese primer año un total de {annual_savings_increase:,.2f}, es decir, {monthly_savings_increase:,.2f} al mes."
        )
        st.markdown(resumen)

        # Gráfico de evolución del capital
        st.header("Evolución del Capital Acumulado")

        # Variables para la evolución del capital
        capital_evolucion = []
        aportaciones = []
        revalorizacion = []
        capital_actual = initial_capital
        ahorro_anual = annual_savings_increase
        total_aportaciones = initial_capital

        for i in range(1, years + 1):
            # Aplicar rentabilidad
            capital_actual *= (1 + expected_rate / 100)
            # Agregar el ahorro anual
            capital_actual += ahorro_anual
            # Registrar aportaciones
            total_aportaciones += ahorro_anual
            aportaciones.append(total_aportaciones)
            # Registrar revalorización
            revalorizacion.append(capital_actual - total_aportaciones)
            # Guardar capital acumulado total
            capital_evolucion.append(capital_actual)
            # Incrementar el ahorro anual por inflación
            ahorro_anual *= (1 + inflation / 100)

        # Crear DataFrame para el gráfico
        df_evolucion = pd.DataFrame({
            "Año": list(range(1, years + 1)),
            "Capital Aportado": aportaciones,
            "Revalorización": revalorizacion,
            "Capital Total": capital_evolucion
        })

        # Generar gráfico de área
        plt.figure(figsize=(10, 6))
        plt.fill_between(df_evolucion["Año"], df_evolucion["Capital Aportado"], label="Capital Aportado", alpha=0.6)
        plt.fill_between(df_evolucion["Año"], df_evolucion["Capital Total"], df_evolucion["Capital Aportado"],
                         label="Revalorización", alpha=0.6)
        plt.title("Evolución del Capital Acumulado", fontsize=16)
        plt.xlabel("Año", fontsize=12)
        plt.ylabel("Capital Acumulado ($)", fontsize=12)
        plt.legend(loc="upper left")
        plt.grid(True)
        plt.tight_layout()

        # Mostrar el gráfico en Streamlit
        st.pyplot(plt)
    else:
        st.markdown("Por favor, completa todos los campos para obtener los resultados. 🙏")

st.markdown("---")
st.markdown("Desarrollado por **Socaire, GdP**")

hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """

st.markdown(hide_streamlit_style, unsafe_allow_html=True) 


