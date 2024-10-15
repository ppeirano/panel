import streamlit as st
import yfinance as yf
import time
import matplotlib.colors as mcolors

# Título de la aplicación
st.title("Monitor de Índices y Acciones")

# Lista predeterminada de activos
default_assets = ["SPY", "QQQ", "DIA", "IWM", "EWZ", "AAPL", "MSFT", "TSLA", "NVDA", "MCD", "KO", "PEP", "XLK", "XLE", "XLF", "XLY", "XLV", "GGAL", "GGAL.BA", "BMA", "ALUA.BA", "YPF", "VIST", ]

# Función para obtener datos
def get_data(ticker):
    stock = yf.Ticker(ticker)
    data = stock.history(period='1d')
    if data.empty:
        return None
    return round((data['Close'].iloc[-1] - data['Open'].iloc[-1]) / data['Open'].iloc[-1] * 100, 2)

# Función para obtener el último valor
def get_last_value(ticker):
    try:
        gv=0
        stock = yf.Ticker(ticker)
        data = stock.history(period='1d')
        if data.empty:
            return 0
        else:
            gv = round(data['Close'].iloc[-1],2)
    except:
        gv = 0
        print(ticker)
    return gv 

# Función para obtener datos de rendimiento
def get_performance(ticker):
    try:
        gp = 0
        stock = yf.Ticker(ticker)
        data = stock.history(period='1d')
        if data.empty:
            gp = 0
        else:
            gp = round((data['Close'].iloc[-1] - data['Open'].iloc[-1]) / data['Open'].iloc[-1] * 100, 2)
    except:
        gp = 0
        print(ticker)
    return gp

# Control deslizante para el intervalo de actualización
refresh_rate = st.slider("Intervalo de actualización (segundos)", 5, 300, 60)


# Check para alternar entre rendimiento y último valor
show_last_value = st.checkbox("Mostrar último valor en lugar del rendimiento")


# Función para mapear el rendimiento a un color
def performance_to_color(performance):
    norm = mcolors.Normalize(vmin=-5, vmax=5)
    cmap = mcolors.LinearSegmentedColormap.from_list("", ["red", "white", "green"])
    rgb_color = cmap(norm(performance))
    hex_color = mcolors.to_hex(rgb_color)
    return hex_color

# Estilo para etiquetas con espaciado
def render_label(asset, value, display_type):
    if display_type == "performance":
        color = performance_to_color(value)
        tcolor = "black"
    else:
        color = "#0B132B"  # Blanco si es el último valor
        tcolor="white"

    st.markdown(f"""
        <div style="background-color:{color}; padding: 10px; margin-bottom: 10px; border-radius: 10px; text-align: center; border: 1px solid black", >
            <span style="color:{tcolor}; font-size:20px;"><strong>{asset}</strong></span>
            <span style="color:{tcolor}; font-size:16px;">{value}</span>
        </div>
        """, unsafe_allow_html=True)


# Mostrar cada activo con su rendimiento
cols = st.columns(4)  # 3 columnas para las tarjetas

for i, asset in enumerate(default_assets):
    with cols[i % 4]:  # Organizar en columnas
        if show_last_value:
            value = get_last_value(asset)
            render_label(asset, value, "last_value")
        else:
            performance = get_performance(asset)
            if performance is not None:
                render_label(asset, performance, "performance")
            else:
                st.warning(f"Sin datos para {asset}")

# Configuración para refrescar automáticamente
while True:
    time.sleep(refresh_rate)
    st.rerun()

