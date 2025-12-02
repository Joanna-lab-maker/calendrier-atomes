
import io, csv
from datetime import date, datetime
import streamlit as st

st.set_page_config(page_title="Calendrier de l’Avent — QCM Atomes (Seconde – J.A.)",
                   page_icon="⚛️", layout="wide")

DAYS = [
    {
        "theme": "Devinette — Quel atome ?",
        "recap": "Atome neutre : nbre d’électrons = Z. e = 1,60 × 10⁻¹⁹ C.",
        "question": "Mon cortège électronique a une charge égale à −6,4 × 10⁻¹⁹ C et ma charge totale est nulle. Mon noyau contient un neutron de plus que de protons. Qui suis‑je ?",
        "qcm": {"a": "Hydrogène‑1 (protium)", "b": "Hydrogène‑2 (deutérium)", "c": "Béryllium‑9"},
        "answer": "c",
        "solution": "−6,4×10⁻¹⁹ C = −4e ⇒ 4e− ⇒ Z=4 (Be). « un neutron de plus » ⇒ N=5 ⇒ ⁹Be."
    },
    {
        "theme": "Conversion d’unités — Rayon atomique",
        "recap": "1 pm = 10⁻¹² m.",
        "question": "Un atome de titane (Ti) a un rayon de 140 pm. Ce rayon est équivalent à :",
        "qcm": {"a": "1,40 × 10⁻¹⁰ m", "b": "14,0 × 10⁻¹⁰ m", "c": "140 × 10⁻¹⁰ m"},
        "answer": "a",
        "solution": "140 pm = 140 × 10⁻¹² m = 1,40 × 10⁻¹⁰ m."
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
        "solution": "A ≈ (5,0×10⁻²⁶) / (1,67×10⁻²⁷) ≈ 30."
    },
    {
        "theme": "Numéro atomique (Z) d’un ion",
        "recap": "Z = nbre de protons (indépendant de la charge).",
        "question": "L’ion chlorure Cl⁻ est présent dans l’eau minérale. Quel est le numéro atomique du chlore ?",
        "qcm": {"a": "11", "b": "17", "c": "35"},
        "answer": "b",
        "solution": "Le chlore a Z = 17."
    },
    {
        "theme": "Isotopes du cuivre (malachite)",
        "recap": "Isotopes stables : ⁶³Cu et ⁶⁵Cu.",
        "question": "Lequel contient le plus de neutrons ?",
        "qcm": {"a": "⁶³Cu", "b": "⁶⁵Cu", "c": "Ils ont le même N"},
        "answer": "b",
        "solution": "Même Z=29, A plus grand ⇒ plus de neutrons."
    },
    {
        "theme": "Isotopes du carbone — Électrons",
        "recap": "Atome neutre : nbre d’électrons = Z. Pour C, Z=6.",
        "question": "Combien d’électrons possède l’atome neutre de carbone‑14 ?",
        "qcm": {"a": "6", "b": "8", "c": "14"},
        "answer": "a",
        "solution": "Z = 6 ⇒ 6 e−."
    },
    {
        "theme": "Rappel — Z du carbone",
        "recap": "Le carbone a Z = 6.",
        "question": "Quel est le numéro atomique (Z) du carbone ?",
        "qcm": {"a": "12", "b": "14", "c": "6"},
        "answer": "c",
        "solution": "Z=6."
    },
    {
        "theme": "Électrons de valence",
        "recap": "Les électrons de la couche externe déterminent la réactivité.",
        "question": "Config : 1s² 2s² 2p⁶ 3s² 3p³. Combien d’électrons sur la couche externe ?",
        "qcm": {"a": "3", "b": "5", "c": "7"},
        "answer": "b",
        "solution": "Couche n=3 : 2 + 3 = 5."
    },
    {
        "theme": "Famille chimique — azote vs phosphore",
        "recap": "Même colonne ⇒ même motif externe ns² np³ ; P est une période en dessous de N.",
        "question": "L’azote a 1s² 2s² 2p³. Pour le phosphore (période suivante), quelle config ?",
        "qcm": {"a": "1s² 2s² 2p⁵", "b": "1s² 2s² 2p⁶ 3s² 3p³", "c": "1s² 2s² 2p⁶ 3s² 3p⁵"},
        "answer": "b",
        "solution": "1s² 2s² 2p⁶ 3s² 3p³."
    },
]

if "scores" not in st.session_state:
    st.session_state.scores = {i+1: None for i in range(len(DAYS))}
if "log" not in st.session_state:
    st.session_state.log = []
def french_date_for(day:int): return f"{day} déc."

st.sidebar.title("⚛️ Calendrier QCM — Atomes (Seconde – J.A.)")
student_id = st.sidebar.text_input("Identifiant élève", value="", placeholder="Prénom_Nom ou code")
lock = st.sidebar.toggle("Verrouiller par date (1–24 déc.)", value=False)
today = date.today()
st.sidebar.markdown(f"**Aujourd’hui :** {today.day} {today.strftime('%b')}")

vals = [v for v in st.session_state.scores.values() if v is not None]
total = sum(vals) if vals else 0
st.sidebar.metric("Score", f"{total}/{len(DAYS)}")
st.sidebar.progress(total/len(DAYS) if len(DAYS) else 0.0)

if st.sidebar.button("🔄 Réinitialiser", use_container_width=True):
    st.session_state.scores = {i+1: None for i in range(len(DAYS))}
    st.session_state.log = []
    st.rerun()

if st.session_state.log:
    out = io.StringIO()
    w = csv.DictWriter(out, fieldnames=["timestamp","student_id","day","choice_key","correct"])
    w.writeheader()
    for r in st.session_state.log: w.writerow(r)
    st.sidebar.download_button("⬇️ Export CSV", out.getvalue().encode("utf-8"),
                               file_name="avent_qcm_resultats.csv", mime="text/csv",
                               use_container_width=True)

st.title("Calendrier de l’Avent — Les Atomes (Seconde – J.A.)")
st.caption("Version QCM (jours 1 à 10).")
cols = st.columns(4, gap="small")
for i in range(len(DAYS)):
    d = i + 1
    with cols[i % 4]:
        locked = lock and not (today.month == 12 and d <= min(24, today.day))
        badge = "🔒" if locked else ("✅" if st.session_state.scores[d] == 1 else ("❌" if st.session_state.scores[d] == 0 else "🗓️"))
        with st.expander(f"{badge} Jour {d} — {DAYS[i]['theme']}", expanded=False):
            st.markdown(f"**À ouvrir le :** {french_date_for(d)}")
            st.markdown(f"> *Rappel* : {DAYS[i]['recap']}")
            st.markdown(f"**Question :** {DAYS[i]['question']}")
            if locked:
                st.info("Case verrouillée (mode calendrier).")
            else:
                opts = list(DAYS[i]["qcm"].items())
                labels = [f\"{k}. {v}\" for k, v in opts]
                choice = st.radio("Choisis la bonne réponse :", labels, key=f"qcm_{d}")
                if st.button("Vérifier", key=f"btn_{d}", use_container_width=True):
                    good_key = DAYS[i]["answer"]
                    good_label = f\"{good_key}. {DAYS[i]['qcm'][good_key]}\"
                    correct = 1 if (choice == good_label) else 0
                    if st.session_state.scores[d] is None:
                        st.session_state.scores[d] = correct
                    ts = datetime.now().isoformat(timespec="seconds")
                    st.session_state.log.append({
                        "timestamp": ts,
                        "student_id": student_id or "anonyme",
                        "day": d,
                        "choice_key": choice.split(".")[0],
                        "correct": correct
                    })
                    if correct:
                        st.success("✅ Bonne réponse !")
                    else:
                        st.error(f"❌ Mauvaise réponse. La bonne était : {good_label}")
                    with st.expander("Voir la solution", expanded=False):
                        st.write(DAYS[i]["solution"])
