import streamlit as st
import random

# --- CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(page_title="Irregular Verbs Master", page_icon="🇬🇧", layout="centered")

# --- BASE DE DATOS COMPLETA (79 VERBOS SEGÚN PDF) ---
VERBOS_POR_PAGINA = {
    1: [("Buy", "Bought", "Bought"), ("Catch", "Caught", "Caught"), ("Fight", "Fought", "Fought"), ("Find", "Found", "Found"), ("Make", "Made", "Made"), ("Read", "Read", "Read"), ("Say", "Said", "Said"), ("Sleep", "Slept", "Slept")],
    2: [("Win", "Won", "Won"), ("Be", "Was/Were", "Been"), ("Break", "Broke", "Broken"), ("Drink", "Drank", "Drunk"), ("Eat", "Ate", "Eaten"), ("Go", "Went", "Gone"), ("Ride", "Rode", "Ridden"), ("See", "Saw", "Seen")],
    3: [("Swim", "Swam", "Swum"), ("Write", "Wrote", "Written"), ("Cut", "Cut", "Cut"), ("Feel", "Felt", "Felt"), ("Get", "Got", "Got"), ("Send", "Sent", "Sent"), ("Come", "Came", "Come"), ("Drive", "Drove", "Driven")],
    4: [("Forget", "Forgot", "Forgotten"), ("Know", "Knew", "Known"), ("Learn", "Learnt", "Learnt"), ("Sing", "Sang", "Sung"), ("Speak", "Spoke", "Spoken"), ("Build", "Built", "Built"), ("Cost", "Cost", "Cost"), ("Fight", "Fought", "Fought")],
    5: [("Hear", "Heard", "Heard"), ("Keep", "Kept", "Kept"), ("Leave", "Left", "Left"), ("Meet", "Met", "Met"), ("Pay", "Paid", "Paid"), ("Sell", "Sold", "Sold"), ("Sit", "Sat", "Sat"), ("Sleep", "Slept", "Slept")],
    6: [("Spend", "Spent", "Spent"), ("Stand", "Stood", "Stood"), ("Tell", "Told", "Told"), ("Think", "Thought", "Thought"), ("Become", "Became", "Become"), ("Begin", "Began", "Begun"), ("Bite", "Bit", "Bitten"), ("Blow", "Blew", "Blown")],
    7: [("Choose", "Chose", "Chosen"), ("Do", "Did", "Done"), ("Draw", "Drew", "Drawn"), ("Fall", "Fell", "Fallen"), ("Fly", "Flew", "Flown"), ("Give", "Gave", "Given"), ("Freeze", "Froze", "Frozen"), ("Forget", "Forgot", "Forgotten")],
    8: [("Grow", "Grew", "Grown"), ("Hide", "Hid", "Hidden"), ("Ring", "Rang", "Rung"), ("Show", "Showed", "Shown"), ("Steal", "Stole", "Stolen"), ("Take", "Took", "Taken"), ("Throw", "Threw", "Thrown"), ("Wear", "Wore", "Worn")],
    9: [("Dig", "Dug", "Dug"), ("Feed", "Fed", "Fed"), ("Hit", "Hit", "Hit"), ("Hold", "Held", "Held"), ("Shoot", "Shot", "Shot"), ("Smell", "Smelt", "Smelt"), ("Sew", "Sewed", "Sewn"), ("Shake", "Shook", "Shaken"), ("Shut", "Shut", "Shut")],
    10: [("Bring", "Brought", "Brought"), ("Lend", "Lent", "Lent"), ("Bend", "Bent", "Bent"), ("Bet", "Bet", "Bet"), ("Bleed", "Bled", "Bled"), ("Burn", "Burnt", "Burnt"), ("Light", "Lit", "Lit"), ("Mean", "Meant", "Meant"), ("Lose", "Lost", "Lost")]
}

# --- GESTIÓN DEL ESTADO (Para que no se borren los datos al recargar) ---
if 'lista' not in st.session_state:
    st.session_state.lista = []
    st.session_state.idx = 0
    st.session_state.jugando = False
    st.session_state.respondido = False
    st.session_state.es_correcto = False

def iniciar():
    data = []
    for i in range(1, st.session_state.max_pags + 1):
        data.extend(VERBOS_POR_PAGINA[i])
    if st.session_state.randomize:
        random.shuffle(data)
    st.session_state.lista = data
    st.session_state.idx = 0
    st.session_state.jugando = True

# --- INTERFAZ ---
st.title("🇬🇧 Irregular Verbs Trainer")

if not st.session_state.jugando:
    with st.container(border=True):
        st.write("### Configura tu sesión")
        st.session_state.max_pags = st.slider("Páginas del PDF a incluir:", 1, 10, 10)
        st.session_state.randomize = st.checkbox("Mezclar verbos (Recomendado)", value=True)
        st.button("Comenzar Práctica", on_click=iniciar, use_container_width=True)
else:
    if st.session_state.idx < len(st.session_state.lista):
        verbo = st.session_state.lista[st.session_state.idx]
        
        st.progress((st.session_state.idx) / len(st.session_state.lista))
        st.write(f"Verbo {st.session_state.idx + 1} de {len(st.session_state.lista)}")
        
        st.markdown(f"<h1 style='text-align: center; color: #4CAF50;'>{verbo[0]}</h1>", unsafe_allow_html=True)

        # Formulario de respuesta
        with st.form(key="my_form"):
            c1, c2 = st.columns(2)
            p_simple = c1.text_input("Past Simple").strip().lower()
            p_participle = c2.text_input("Past Participle").strip().lower()
            submit = st.form_submit_button("Comprobar", use_container_width=True)

        if submit:
            st.session_state.respondido = True
            # Lógica de validación
            is_be = (verbo[0] == "Be" and p_simple in ["was", "were", "was/were"])
            c_past = (p_simple == verbo[1].lower()) or is_be
            c_part = (p_participle == verbo[2].lower())
            st.session_state.es_correcto = c_past and c_part

        if st.session_state.respondido:
            if st.session_state.es_correcto:
                st.success("✨ ¡Correcto!")
            else:
                st.error(f"❌ Incorrecto. La respuesta es: **{verbo[1]}** | **{verbo[2]}**")
            
            if st.button("Siguiente Verbo →", use_container_width=True):
                st.session_state.idx += 1
                st.session_state.respondido = False
                st.rerun()
    else:
        st.balloons()
        st.success("### ¡Has completado todos los verbos! 🎉")
        if st.button("Volver al inicio"):
            st.session_state.jugando = False
            st.rerun()