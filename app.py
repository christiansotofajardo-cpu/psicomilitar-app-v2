import streamlit as st

# ------------------------------------------------------------------
# CONFIGURACIÓN GENERAL
# ------------------------------------------------------------------
st.set_page_config(
    page_title="PsychoMilitar 2.1",
    page_icon="🪖",
    layout="wide"
)

# ------------------------------------------------------------------
# ESTADO GLOBAL
# ------------------------------------------------------------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "username" not in st.session_state:
    st.session_state.username = ""

if "evaluaciones" not in st.session_state:
    # lista de diccionarios con cada evaluación
    st.session_state.evaluaciones = []


# ------------------------------------------------------------------
# FUNCIONES AUXILIARES
# ------------------------------------------------------------------
def login_screen():
    st.title("🪖 Sistema PsychoMilitar 2.1")
    st.subheader("Acceso restringido a personal autorizado")

    st.markdown(
        "Ingrese sus credenciales para acceder al sistema de evaluación "
        "psicológica y cognitiva automatizada."
    )

    col1, col2 = st.columns(2)

    with col1:
        usuario = st.text_input("Usuario", value="")
    with col2:
        clave = st.text_input("Contraseña", type="password", value="")

    st.caption("Credenciales DEMO: usuario **admin** | clave **psico2025**")

    if st.button("Ingresar"):
        if usuario == "admin" and clave == "psico2025":
            st.session_state.logged_in = True
            st.session_state.username = usuario
            st.success("Acceso concedido. Bienvenido, comandante.")
        else:
            st.error("Credenciales incorrectas. Intente nuevamente.")


def vista_dashboard():
    st.title("📊 Dashboard operativo PsychoMilitar 2.1")

    total_eval = len(st.session_state.evaluaciones)
    hoy_eval = sum(1 for e in st.session_state.evaluaciones if e.get("es_hoy", False))

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Evaluaciones registradas (demo)", total_eval)
    with col2:
        st.metric("Evaluaciones del día (demo)", hoy_eval)
    with col3:
        st.metric("Estado del sistema", "OPERATIVO")

    st.markdown("---")
    st.markdown(
        "Este dashboard muestra un resumen **demo** del comportamiento del sistema. "
        "En la versión productiva, estos indicadores se conectarán a la base de datos real."
    )


def vista_aplicar_test():
    st.title("📝 Aplicar Test PsicoMilitar")

    st.markdown(
        "Complete los datos del evaluado y responda el módulo de **screening breve**. "
        "Los resultados serán almacenados temporalmente en esta sesión (DEMO)."
    )
    st.markdown("---")

    # Datos básicos del evaluado
    col1, col2, col3 = st.columns(3)
    with col1:
        rut = st.text_input("RUT / ID del evaluado")
    with col2:
        nombre = st.text_input("Nombre completo")
    with col3:
        edad = st.number_input("Edad", min_value=17, max_value=65, value=21)

    col4, col5 = st.columns(2)
    with col4:
        unidad = st.text_input("Unidad / Región")
    with col5:
        genero = st.selectbox(
            "Género",
            ["No responde", "Femenino", "Masculino", "Otro"]
        )

    st.markdown("### Bloque 1: Estado de ánimo (última semana)")
    q1 = st.slider("Ánimo bajo / tristeza", 0, 10, 3)
    q2 = st.slider("Irritabilidad / enojo", 0, 10, 4)
    q3 = st.slider("Ansiedad / preocupación", 0, 10, 5)

    st.markdown("### Bloque 2: Control e impulsividad")
    q4 = st.slider("Control de impulsos en situaciones de estrés", 0, 10, 6)
    q5 = st.slider("Actúa sin pensar en consecuencias", 0, 10, 4)

    if st.button("Calcular y registrar evaluación"):
        if not rut or not nombre:
            st.error("Debe ingresar al menos RUT/ID y Nombre del evaluado.")
            return

        mood_score = (q1 + q2 + q3) / 3.0
        impulse_score = (q4 + (10 - q5)) / 2.0
        global_score = (10 - mood_score) * 0.5 + impulse_score * 0.5

        if global_score >= 7.5:
            nivel = "Bajo"
            etiqueta = "✅ Riesgo bajo"
            comentario = (
                "Perfil compatible con buen ajuste emocional e impulsivo. "
                "No se observan indicadores críticos en este screening breve."
            )
        elif global_score >= 5.0:
            nivel = "Medio"
            etiqueta = "🟡 Riesgo medio"
            comentario = (
                "Existen algunos indicadores que ameritan monitoreo. "
                "Se sugiere entrevista clínica focalizada antes de decisiones críticas."
            )
        else:
            nivel = "Alto"
            etiqueta = "🛑 Riesgo alto"
            comentario = (
                "El screening sugiere un perfil de riesgo elevado. "
                "Se recomienda evaluación psicológica en mayor profundidad."
            )

        registro = {
            "rut": rut,
            "nombre": nombre,
            "edad": edad,
            "unidad": unidad,
            "genero": genero,
            "mood_score": round(mood_score, 1),
            "impulse_score": round(impulse_score, 1),
            "global_score": round(global_score, 1),
            "nivel_riesgo": nivel,
            "es_hoy": True,  # demo
        }

        st.session_state.evaluaciones.append(registro)

        st.success(f"Evaluación registrada para {nombre} ({rut}).")

        st.markdown("#### Resultado inmediato")
        colr1, colr2, colr3 = st.columns(3)
        with colr1:
            st.metric("Estado de ánimo (riesgo)", f"{registro['mood_score']} / 10")
        with colr2:
            st.metric("Control de impulsos", f"{registro['impulse_score']} / 10")
        with colr3:
            st.metric("Índice global", f"{registro['global_score']} / 10")

        st.markdown(f"**Nivel de riesgo estimado:** {etiqueta}")
        st.info(comentario)


def vista_resultados():
    st.title("📋 Resultados de Evaluaciones (DEMO)")

    if not st.session_state.evaluaciones:
        st.warning("Aún no hay evaluaciones registradas en esta sesión.")
        return

    st.markdown(
        "A continuación se muestran las evaluaciones registradas durante esta sesión "
        "(almacenamiento en memoria, modo DEMO)."
    )

    for i, ev in enumerate(reversed(st.session_state.evaluaciones), start=1):
        st.markdown("---")
        st.markdown(f"### Evaluación #{i} — {ev['nombre']} ({ev['rut']})")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.write(f"**Edad:** {ev['edad']}")
            st.write(f"**Género:** {ev['genero']}")
        with col2:
            st.write(f"**Unidad:** {ev['unidad']}")
            st.write(f"**Riesgo:** {ev['nivel_riesgo']}")
        with col3:
            st.write(f"**Ánimo (riesgo):** {ev['mood_score']} / 10")
            st.write(f"**Impulsos:** {ev['impulse_score']} / 10")
            st.write(f"**Global:** {ev['global_score']} / 10")


def vista_acerca_de():
    st.title("ℹ️ Acerca de PsychoMilitar 2.1")
    st.markdown(
        """
        **PsychoMilitar 2.1** es un prototipo funcional de sistema de evaluación
        psicológica y cognitiva para contextos militares.

        Esta versión:

        - Opera en servidores en la nube (Render).
        - Utiliza una arquitectura ligera basada en Streamlit.
        - Permite aplicar un módulo de *screening* breve y visualizar resultados demo.
        - Está diseñada como base para integrar, en versiones futuras, bases de datos,
          módulos avanzados de scoring y análisis automatizado.

        Esta es una **versión de demostración interna**.
        """
    )


# ------------------------------------------------------------------
# LAYOUT PRINCIPAL
# ------------------------------------------------------------------
if not st.session_state.logged_in:
    login_screen()
else:
    with st.sidebar:
        st.markdown("### 🪖 PsychoMilitar 2.1")
        st.markdown(f"**Usuario:** {st.session_state.username}")
        opcion = st.radio(
            "Navegación",
            ["Dashboard", "Aplicar test", "Resultados", "Acerca de", "Cerrar sesión"],
        )

    if opcion == "Dashboard":
        vista_dashboard()
    elif opcion == "Aplicar test":
        vista_aplicar_test()
    elif opcion == "Resultados":
        vista_resultados()
    elif opcion == "Acerca de":
        vista_acerca_de()
    elif opcion == "Cerrar sesión":
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.experimental_rerun()
