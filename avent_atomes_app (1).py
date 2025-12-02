import io, csv
from datetime import date, datetime
import streamlit as st

# --- CONFIGURATION DE L’APPLICATION ---
st.set_page_config(page_title="Calendrier de l’Avent — QCM Atomes (Seconde – J.A.)",
                   page_icon="⚛️", layout="wide")

# --- MASQUER LE MENU ET LES BOUTONS ---
st.markdown("""
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
[data-testid="stToolbar"]{display:none!important;}
header [data-testid="stDecoration"]{display:none!important;}
header a[href*="github.com"]{display:none!important;}
header button[kind="header"]{display:none!important;}
</style>
""", unsafe_allow_html=True)

# --- DÉFINITION DES JOURS 1 À 12 ---
DAYS = [
    {
        "theme": "Devinette — Quel atome ?",
        "recap": "Atome neutre : nbre d’électrons = Z. e = 1,60 × 10⁻¹⁹ C.",
        "question": "Mon cortège électronique a une charge égale à −6,4 × 10⁻¹⁹ C et ma charge totale est nulle. "
                    "Mon noyau contient un neutron de plus que de protons. Qui suis-je ?",
        "qcm": {"a": "Hydrogène-1 (protium)", "b": "Hydrogène-2 (deutérium)", "c": "Béryllium-9"},
        "answer": "c",
        "solution": "−6,4×10⁻¹⁹ C = −4e ⇒ 4 électrons ⇒ Z=4 (béryllium). « Un neutron de plus » ⇒ N=5 ⇒ ⁹Be."
    },
    {
        "theme": "Conversion d’unités — Rayon atomique",
        "recap": "1 pm = 10⁻¹² m. Rayons atomiques ~ 100 pm.",
        "question": "Un atome de titane (Ti) a un rayon de 140 pm. Ce rayon est équivalent à :",
        "qcm": {"a": "1,40 × 10⁻¹⁰ m", "b": "14,0 × 10⁻¹⁰ m", "c": "140 × 10⁻¹⁰ m"},
        "answer": "a",
        "solution": "140 pm = 1,40 × 10⁻¹⁰ m."
    },
    {
        "theme": "Ordres de grandeur — Masse d’un atome",
        "recap": "1 u ≈ 1,66 × 10⁻²⁷ kg.",
        "question": "Un atome de tantale ¹⁸¹Ta a une masse environ égale à :",
        "qcm": {"a": "3 × 10⁻²² g", "b": "3 × 10⁻²² mg", "c": "3 × 10⁻²² kg"},
        "answer": "a",
        "solution": "m ≈ 181 × 1,66×10⁻²⁷ kg ≈ 3,0×10⁻²⁵ kg = 3×10⁻²² g."
    },
    {
        "theme": "Nombres de nucléons",
        "recap": "A ≈ masse atome / masse d’un nucléon.",
        "question": "Un atome a une masse 5,0 × 10⁻²⁶ kg. Son noyau contient environ :",
        "qcm": {"a": "3 nucléons", "b": "300 nucléons", "c": "30 nucléons"},
        "answer": "c",
        "solution": "A ≈ (5,0×10⁻²⁶)/(1,67×10⁻²⁷) ≈ 30."
    },
    {
        "theme": "Numéro atomique (Z) d’un ion",
        "recap": "Z = nombre de protons (identifie l’élément).",
        "question": "Dans une eau minérale, on trouve l’ion chlorure Cl⁻. Quel est le numéro atomique du chlore ?",
        "qcm": {"a": "11", "b": "17", "c": "35"},
        "answer": "b",
        "solution": "Le chlore a Z = 17."
    },
    {
        "theme": "Isotopes du cuivre (malachite)",
        "recap": "Isotopes stables : ⁶³Cu et ⁶⁵Cu (Z = 29).",
        "question": "Quel isotope contient le plus de neutrons ?",
        "qcm": {"a": "⁶³Cu", "b": "⁶⁵Cu", "c": "Ils ont le même N"},
        "answer": "b",
        "solution": "Même Z, A plus grand ⇒ plus de neutrons."
    },
    {
        "theme": "Isotopes du carbone — Électrons",
        "recap": "Atome neutre : nbre d’électrons = Z (ici Z = 6).",
        "question": "Combien d’électrons possède l’atome neutre de carbone-14 ?",
        "qcm": {"a": "6", "b": "8", "c": "14"},
        "answer": "a",
        "solution": "Z = 6 ⇒ 6 électrons."
    },
    {
        "theme": "Rappel — Z du carbone",
        "recap": "Le carbone a Z = 6.",
        "question": "Quel est le numéro atomique (Z) du carbone ?",
        "qcm": {"a": "12", "b": "14", "c": "6"},
        "answer": "c",
        "solution": "Z = 6."
    },
    {
        "theme": "Électrons de valence",
        "recap": "Les électrons de la couche externe déterminent la réactivité.",
        "question": "Config : 1s² 2s² 2p⁶ 3s² 3p³. Combien d’électrons sur la couche externe ?",
        "qcm": {"a": "3", "b": "5", "c": "7"},
        "answer": "b",
        "solution": "Couche n = 3 : 3s²3p³ ⇒ 2 + 3 = 5."
    },
    {
        "theme": "Famille chimique — Azote vs Phosphore",
        "recap": "Même colonne ⇒ même motif externe ns² np³ ; P est une période en dessous de N.",
        "question": "L’azote a 1s² 2s² 2p³. Pour le phosphore (période suivante), quelle configuration ?",
        "qcm": {"a": "1s² 2s² 2p⁵", "b": "1s² 2s² 2p⁶ 3s² 3p³", "c": "1s² 2s² 2p⁶ 3s² 3p⁵"},
        "answer": "b",
        "solution": "Même motif externe mais niveau n = 3 : 1s² 2s² 2p⁶ 3s² 3p³."
    },
    {
        "theme": "Famille chimique — Configuration électronique",
        "recap": "Deux éléments appartiennent à la même famille chimique s’ils ont le même nombre d’électrons de valence.",
        "question": "Deux atomes ont pour configuration : 1s² 2s² 2p² et 1s² 2s² 2p⁴. Appartiennent-ils à la même famille ?",
        "qcm": {
            "a": "Oui, même nombre d’électrons de valence.",
            "b": "Non, nombre d’électrons de valence différent.",
            "c": "Oui, même période."
        },
        "answer": "b",
        "solution": "Le premier atome a 4 électrons de valence, le second 6 ⇒ familles différentes."
    },
    {
        "theme": "Ions de NaCl — L’ion chlorure Cl⁻",
        "recap": "Un ion négatif (anion) résulte du gain d’électron(s). Z(Cl) = 17 → 17 protons → 18 électrons dans Cl⁻.",
        "question": "À propos de Cl⁻, quelle proposition est correcte ?",
        "qcm": {
            "a": "Il a perdu 1 électron ; cation ; 17 p⁺ et 16 e⁻.",
            "b": "Il a gagné 1 électron ; anion ; 17 p⁺ et 18 e⁻.",
            "c": "Il a gagné 1 électron ; cation ; 18 p⁺ et 17 e⁻."
        },
        "answer": "b",
        "solution": "Cl a Z = 17 ⇒ 17 protons. En devenant Cl⁻, il gagne 1 électron ⇒ 18 e⁻ (anion)."
    },
  {
    "theme": "Configuration électronique — Calcium",
    "recap": "Le calcium (Ca) est dans la 2ᵉ colonne → famille des alcalino-terreux, et dans la 4ᵉ période du tableau périodique.",
    "question": "L’atome de calcium appartient à la 2ᵉ colonne et à la 4ᵉ période de la classification. Quelle est sa configuration électronique ?",
    "qcm": {
        "a": "1s² 2s² 2p⁶ 3s² 3p⁶ 3d²",
        "b": "1s² 2s² 2p⁶ 3s² 3p⁶ 4s²",
        "c": "1s² 2s² 2p⁶ 3s² 3p⁴"
    },
    "answer": "b",
    "solution": "Le calcium (Z=20) remplit la sous-couche 4s après la 3p : sa configuration est 1s² 2s² 2p⁶ 3s² 3p⁶ 4s².",
    "image": "https://raw.githubusercontent.com/Joanna-lab-maker/calendrier-atomes/main/images/jour13.png"
},
  {
    "theme": "Périodes du tableau périodique — Configurations électroniques",
    "recap": "Les éléments d’une même période ont le même nombre de couches électroniques (même nombre quantique principal n).",
    "question": "Les atomes X, Y et Z ont respectivement les configurations suivantes :\n\nX : 1s² 2s² 2p¹\nY : 1s² 2s² 2p⁵\nZ : 1s² 2s² 2p⁶ 3s² 3p²\n\nLesquels appartiennent à la même période ?",
    "qcm": {
        "a": "X et Y",
        "b": "Y et Z",
        "c": "X et Z"
    },
    "answer": "a",
    "solution": "X (1s² 2s² 2p¹) et Y (1s² 2s² 2p⁵) ont leurs électrons dans les couches n=1 et n=2, donc appartiennent à la 2ᵉ période. Z (3p²) a trois couches, donc 3ᵉ période.",
    "image": "https://raw.githubusercontent.com/Joanna-lab-maker/calendrier-atomes/main/images/jour14.png"
},
  {
    "theme": "Molécule d’ammoniac — Liaisons covalentes",
    "recap": "Dans la molécule d’ammoniac (NH₃), l’atome d’azote forme des liaisons covalentes simples avec les atomes d’hydrogène.",
    "question": "Combien de liaisons covalentes contient la molécule d’ammoniac (NH₃) ?",
    "qcm": {
        "a": "2",
        "b": "3",
        "c": "4"
    },
    "answer": "b",
    "solution": "L’ammoniac (NH₃) comporte trois liaisons covalentes simples entre l’atome d’azote et les trois atomes d’hydrogène.",
    "image": "https://raw.githubusercontent.com/Joanna-lab-maker/calendrier-atomes/main/images/jour15.png"
},
]

# --- INITIALISATION DES SCORES ---
def _reset_state_to_days():
    st.session_state.scores  = {i+1: None for i in range(len(DAYS))}
    if "log" not in st.session_state:
        st.session_state.log = []

if ("scores" not in st.session_state) or (set(st.session_state.scores.keys()) != set(range(1, len(DAYS)+1))):
    _reset_state_to_days()

# --- BARRE LATÉRALE ---
st.sidebar.title("⚛️ Calendrier QCM — Atomes (Seconde – J.A.)")
student_id = st.sidebar.text_input("Identifiant élève", value="", placeholder="Prénom_Nom ou code")
lock = st.sidebar.toggle("Verrouiller par date (1–24 décembre)", value=False)
today = date.today()
st.sidebar.markdown(f"Aujourd’hui : {today.day} {today.strftime('%b')}")

vals = [v for v in st.session_state.scores.values() if v is not None]
total = sum(vals) if vals else 0
done = sum(1 for v in vals if v is not None)
st.sidebar.metric("Jours validés", f"{done}/{len(DAYS)}")
st.sidebar.metric("Score", f"{total}/{len(DAYS)}")
st.sidebar.progress(total/len(DAYS) if len(DAYS) else 0.0, text="Progression")

if st.sidebar.button("🔄 Réinitialiser", use_container_width=True):
    _reset_state_to_days()
    st.session_state.log = []
    st.rerun()

# --- PAGE PRINCIPALE ---
st.title("Calendrier de l’Avent — Les Atomes (Seconde – J.A.)")
st.caption("Version QCM (jours 1 à 12).")

cols = st.columns(4, gap="small")
for i, day in enumerate(DAYS):
    d = i + 1
    with cols[i % 4]:
        locked = lock and not (today.month == 12 and d <= min(24, today.day))
        state = st.session_state.scores[d]
        badge = "🔒" if locked else ("✅" if state == 1 else ("❌" if state == 0 else "🗓️"))
        with st.expander(f"{badge} Jour {d} — {day['theme']}", expanded=False):
            st.markdown(f"**À ouvrir le :** {d} déc.")
            st.markdown(f"> *Rappel express* : {day['recap']}")
            st.markdown(f"**Question :** {day['question']}")
            opts = list(day["qcm"].items())
            labels = [f"{k}. {v}" for k, v in opts]
            choice = st.radio("Choisis la bonne réponse :", labels, key=f"qcm_{d}")
            if st.button("Vérifier", key=f"btn_{d}", use_container_width=True):
                good_key = day["answer"]
                good_label = f"{good_key}. {day['qcm'][good_key]}"
                correct = 1 if (choice == good_label) else 0
                if st.session_state.scores[d] is None:
                    st.session_state.scores[d] = correct
                ts = datetime.now().isoformat(timespec="seconds")
                st.session_state.log.append({
                    "timestamp": ts,
                    "student_id": student_id or "anonyme",
                    "day": d,
                    "choice_key": choice.split(".", 1)[0],
                    "correct": correct
                })
                if correct:
                    st.success("✅ Bonne réponse !")
                else:
                    st.error(f"❌ Mauvaise réponse. La bonne était : {good_label}")
                with st.expander("Voir la solution", expanded=False):
                    st.write(day["solution"])
