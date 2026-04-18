import streamlit as st
import akinator

# Configuración inicial de la página
st.set_page_config(page_title="Akinator Web", page_icon="🧞‍♂️", layout="centered")

# Estilos CSS
st.markdown("""
<style>
    .title {
        text-align: center;
        color: #38bdf8;
        font-weight: bold;
    }
    .question-box {
        background-color: #1e293b;
        color: #f8fafc;
        padding: 30px;
        border-radius: 15px;
        text-align: center;
        font-size: 24px;
        margin: 20px 0;
        font-weight: 500;
        box-shadow: 0px 4px 10px rgba(0,0,0,0.3);
    }
    div.stButton > button {
        font-weight: bold;
        border-radius: 10px;
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<h1 class="title">Akinator El Genio 🧞‍♂️</h1>', unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #94a3b8; font-size: 18px;'>Piensa en un personaje real o ficticio. Yo lo adivinaré.</p>", unsafe_allow_html=True)

# Variables de estado (para mantener el juego activo al recargar)
if 'aki' not in st.session_state:
    st.session_state.aki = akinator.Akinator()
if 'started' not in st.session_state:
    st.session_state.started = False
if 'guessed' not in st.session_state:
    st.session_state.guessed = False
if 'game_over' not in st.session_state:
    st.session_state.game_over = False

def start_game():
    st.session_state.aki.start_game(language="es")
    st.session_state.started = True
    st.session_state.guessed = False
    st.session_state.game_over = False

def send_answer(ans):
    # Enviar respuesta
    st.session_state.aki.answer(ans)
    # Detectar si adivinó
    if getattr(st.session_state.aki, 'win', False):
        st.session_state.guessed = True

def confirm_guess():
    st.session_state.aki.choose()
    st.session_state.game_over = True
    st.session_state.guessed = False
    st.session_state.win_status = 'win'

def reject_guess():
    st.session_state.aki.exclude()
    if st.session_state.aki.finished:
        st.session_state.game_over = True
        st.session_state.guessed = False
        st.session_state.win_status = 'defeat'
    elif not getattr(st.session_state.aki, 'win', False):
        st.session_state.guessed = False

# Lógica condicional de la pantalla
if not st.session_state.started:
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.button("🔮 Iniciar Juego", on_click=start_game, use_container_width=True, type="primary")

elif st.session_state.game_over:
    if st.session_state.win_status == 'win':
        st.success("¡Genial! He vuelto a ganar. Soy un genio imparable.")
    else:
        st.error(f"¡Me rindo! \n\n{st.session_state.aki.question}")
    
    st.button("¡Volver a Jugar!", on_click=start_game, use_container_width=True)

elif st.session_state.guessed:
    st.progress(100)
    st.markdown("<div class='question-box'>¡He adivinado! ¿Pensabas en...? 🤔</div>", unsafe_allow_html=True)
    
    name = getattr(st.session_state.aki, 'name_proposition', 'Desconocido')
    desc = getattr(st.session_state.aki, 'description_proposition', '')
    pic = getattr(st.session_state.aki, 'photo', None)
    
    st.markdown(f"<h2 style='text-align: center; color: #fbbf24;'>{name}</h2>", unsafe_allow_html=True)
    st.markdown(f"<p style='text-align: center; font-style: italic; font-size: 20px;'>{desc}</p>", unsafe_allow_html=True)
    
    if pic:
        st.image(pic, use_column_width=True)
        
    col1, col2 = st.columns(2)
    with col1:
        st.button("✅ ¡Sí, es mi personaje!", on_click=confirm_guess, use_container_width=True, type="primary")
    with col2:
        st.button("❌ No, no lo es.", on_click=reject_guess, use_container_width=True)

else:
    # Pantalla de preguntas normal
    prog = st.session_state.aki.progression
    st.progress(int(prog))
    st.markdown(f"<div class='question-box'>{st.session_state.aki.question}</div>", unsafe_allow_html=True)
    
    st.button("Sí", on_click=send_answer, args=("yes",), use_container_width=True)
    st.button("No", on_click=send_answer, args=("no",), use_container_width=True)
    st.button("No lo sé", on_click=send_answer, args=("i don't know",), use_container_width=True)
    st.button("Probablemente", on_click=send_answer, args=("probably",), use_container_width=True)
    st.button("Probablemente no", on_click=send_answer, args=("probably not",), use_container_width=True)
