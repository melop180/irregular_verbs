import streamlit as st
import random

# --- CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(page_title="Irregular Verbs Master", page_icon="🇬🇧", layout="centered")

# --- BASE DE DATOS ORGANIZADA POR PÁGINAS (Tus saltos de línea) ---
PAGINAS_VERBOS = {
    1: [("Buy", "Bought", "Bought"), ("Catch", "Caught", "Caught"), ("Fight", "Fought", "Fought"), ("Find", "Found", "Found"), ("Make", "Made", "Made"), ("Read", "Read", "Read"), ("Say", "Said", "Said"), ("Sleep", "Slept", "Slept")],
    2: [("Win", "Won", "Won"), ("Be", "Was/Were", "Been"), ("Break", "Broke", "Broken"), ("Drink", "Drank", "Drunk"), ("Eat", "Ate", "Eaten"), ("Go", "Went", "Gone"), ("Ride", "Rode", "Ridden"), ("See", "Saw", "Seen")],
    3: [("Swim", "Swam", "Swum"), ("Write", "Wrote", "Written"), ("Cut", "Cut", "Cut"), ("Feel", "Felt", "Felt"), ("Get", "Got", "Got"), ("Send", "Sent", "Sent"), ("Come", "Came", "Come"), ("Drive", "Drove", "Driven")],
    4: [("Forget", "Forgot", "Forgotten"), ("Know", "Knew", "Known"), ("Learn", "Learned/Learnt", "Learnt"), ("Sing", "Sang", "Sung"), ("Speak", "Spoke", "Spoken"), ("Build", "Built", "Built"), ("Cost", "Cost", "Cost"), ("Fight", "Fought", "Fought")],
    5: [("Find", "Found", "Found"), ("Hear", "Heard", "Heard"), ("Keep", "Kept", "Kept"), ("Leave", "Left", "Left"), ("Meet", "Met", "Met"), ("Pay", "Paid", "Paid"), ("Sell", "Sold", "Sold"), ("Sit", "Sat", "Sat")],
    6: [("Spend", "Spent", "Spent"), ("Stand", "Stood", "Stood"), ("Tell", "Told", "Told"), ("Think", "Thought", "Thought"), ("Become", "Became", "Become"), ("Begin", "Began", "Begun"), ("Bite", "Bit", "Bitten"), ("Blow", "Blew", "Blown")],
    7: [("Choose", "Chose", "Chosen"), ("Do", "Did", "Done"), ("Draw", "Drew", "Drawn"), ("Fall", "Fell", "Fallen"), ("Fly", "Flew", "Flown"), ("Give", "Gave", "Given"), ("Ring", "Rang", "Rung"), ("Take", "Took", "Taken")],
    8: [("Wear", "Wore", "Worn")],
    9: [("Dig", "Dug", "Dug"), ("Feed", "Fed", "Fed"), ("Hit", "Hit", "Hit"), ("Hold", "Held", "Held"), ("Shoot", "Shot", "Shot"), ("Smell", "Smelt", "Smelt"), ("Sew", "Sewed", "Sewn"), ("Shake", "Shook", "Shaken")],
    10: [("Hide", "Hid", "Hidden"), ("Steal", "Stole", "Stolen"), ("Bring", "Brought", "Brought"), ("Lend", "Lent", "Lent"), ("Bend", "Bent", "Bent"), ("Bet", "Bet", "Bet"), ("Bleed", "Bled", "Bled"), ("Burn", "Burnt", "Burnt")],
    11: [("Can", "Could", "Could"), ("Forbid", "Forbade", "Forbidden"), ("Forgive", "Forgave", "Forgiven"), ("Freeze", "Froze", "Frozen"), ("Shine", "Shone", "Shone"), ("Teach", "Taught", "Taught")]
}

# --- GESTIÓN DEL ESTADO ---
if 'lista' not in st.session_state:
    st.session_state.lista = []
    st.session_state.idx = 0
    st.session_state.puntos = 0
    st.session_state.jugando = False
    st.session_state.respondido = False

def iniciar(paginas_seleccionadas):
    data = []
    for pag in paginas_seleccionadas:
        data.extend(PAGINAS_VERBOS[pag])
    
    # Eliminar duplicados exactos (ej. Fight aparece en pág 1 y 4)
    data = list(dict.fromkeys(data))
    
    if st.session_state.randomize:
        random.shuffle(data)
    
    st.session_state.lista = data
    st.session_state.idx = 0
    st.session_state.puntos = 0
    st.session_state.jugando = True

# --- INTERFAZ ---
st.title("🇬🇧 Verbs Master")

if not st.session_state.jugando:
    with st.container(border=True):
        st.write("### 📝 Selecciona las páginas para estudiar")
        
        # Crear columnas para los checkboxes de forma que se vean ordenados
        col_a, col_b = st.columns(2)
        seleccion = []
        
        for i in range(1, 12):
            target_col = col_a if i <= 6 else col_b
            if target_col.checkbox(f"Página {i}", value=True, key=f"pg_{i}"):
                seleccion.append(i)
        
        st.divider()
        st.session_state.randomize = st.checkbox("Mezclar verbos", value=True)
        
        if st.button("Comenzar Práctica", use_container_width=True, disabled=len(seleccion) == 0):
            iniciar(seleccion)
            st.rerun()
else:
    # Lógica del juego
    if st.session_state.idx < len(st.session_state.lista):
        verbo = st.session_state.lista[st.session_state.idx]
        
        st.progress(st.session_state.idx / len(st.session_state.lista))
        st.write(f"Verbo {st.session_state.idx + 1} de {len(st.session_state.lista)} | ⭐ Aciertos: {st.session_state.puntos}")
        
        st.markdown(f"<h1 style='text-align: center; color: #4CAF50;'>{verbo[0]}</h1>", unsafe_allow_html=True)

        with st.form(key=f"f_{st.session_state.idx}"):
            c1, c2 = st.columns(2)
            p_simple = c1.text_input("Past Simple").strip().lower()
            p_participle = c2.text_input("Past Participle").strip().lower()
            submit = st.form_submit_button("Comprobar", use_container_width=True)

        if submit:
            st.session_state.respondido = True
            # Normalización de respuestas
            sol_past = [s.strip().lower() for s in verbo[1].replace('/', ',').split(',')]
            sol_part = [s.strip().lower() for s in verbo[2].replace('/', ',').split(',')]
            
            if p_simple in sol_past and p_participle in sol_part:
                st.session_state.es_correcto = True
                st.session_state.puntos += 1
            else:
                st.session_state.es_correcto = False

        if st.session_state.respondido:
            if st.session_state.es_correcto:
                st.success("✨ ¡Correcto!")
            else:
                st.error(f"❌ Respuesta: **{verbo[1]}** | **{verbo[2]}**")
            
            if st.button("Siguiente Verbo →", use_container_width=True):
                st.session_state.idx += 1
                st.session_state.respondido = False
                st.rerun()
    else:
        st.balloons()
        st.success(f"### ¡Sesión terminada! 🎉\nTu puntuación: **{st.session_state.puntos}/{len(st.session_state.lista)}**")
        if st.button("Volver al inicio"):
            st.session_state.jugando = False
            st.rerun()
