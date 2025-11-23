
import re
import io
import csv
from datetime import date, datetime
import streamlit as st

st.title("Calendrier de l’Avent — Les Atomes (Seconde – J.A.)")
st.image("https://raw.githubusercontent.com/Joanna-lab-maker/calendrier-atomes/main/Capture%20d'%C3%A9cran%202025-11-23%20231049.png", width=180)



# ---------------------- Données pédagogiques (24 jours) ----------------------
DAYS = [
   {"theme": "Qu’est-ce qu’un atome ?",
 "recap": "Un atome est constitué d’un noyau (protons + neutrons) et d’électrons dans un nuage électronique.",
 "question": "Mon cortège électronique a une charge égale à -6.4 × 10^-19 C alors que ma charge totale est nulle. Mon noyau contient un neutron de plus que de protons. Qui suis-je ?",
 "solution": "Il s’agit de l’atome de deutérium (hydrogène-2).",
 "accept": [r"deut", r"hydrog", r"H2"]},


    {"theme":"Origine du mot atome",
     "recap":"Du grec « atomos » = indivisible. Les modèles modernes ont montré qu’il est divisible (noyau/électrons).",
     "question":"Pourquoi l’étymologie « indivisible » est-elle trompeuse aujourd’hui ?",
     "solution":"Parce qu'on connaît la structure interne (noyau + électrons).",
     "accept":[r"noyau", r"électrons?|electrons?"]},

    {"theme":"Modèle de Dalton",
     "recap":"Dalton (début XIXe) propose des « billes » indivisibles et des combinaisons définies.",
     "question":"Cite une limite du modèle de Dalton.",
     "solution":"N’explique ni noyau, ni électrons, ni isotopes, ni l’électricité.",
     "accept":[r"noyau|électrons?|electrons?|isotopes?"]},

    {"theme":"Modèle de Thomson",
     "recap":"« Pudding aux raisins » : électrons plongés dans une masse positive.",
     "question":"Quel résultat expérimental n’est pas expliqué par ce modèle ?",
     "solution":"La forte déviation de quelques particules α (feuille d’or) observée par Rutherford.",
     "accept":[r"feuille d.?or|rutherford|déviation|alpha"]},

    {"theme":"Rutherford et le noyau",
     "recap":"Diffusion des particules α : découverte d’un noyau dense et chargé positivement.",
     "question":"Que révèle la déviation rare mais importante des α ?",
     "solution":"Charge positive et masse concentrées dans un très petit volume : le noyau.",
     "accept":[r"noyau|charge positive|petit volume|concentr"]},

    {"theme":"Bohr et niveaux d’énergie",
     "recap":"Électrons sur des orbites quantifiées ; sauts d’un niveau à l’autre avec émission/absorption.",
     "question":"Donne un exemple d’application des niveaux quantifiés (spectres).",
     "solution":"Raies spectrales de l’hydrogène (émission/absorption).",
     "accept":[r"raies? spectrales?|spectre|hydrog[èe]ne"]},

    {"theme":"Particules : p, n, e−",
     "recap":"Proton (+1), neutron (0), électron (−1). Masse de l’électron ~2000× plus petite que celle du proton.",
     "question":"Classe p, n, e− par masse décroissante.",
     "solution":"neutron ≈ proton ≫ électron.",
     "accept":[r"neutron.*proton.*électrons?|proton.*neutron.*électrons?"]},

    {"theme":"Numéro atomique Z",
     "recap":"Z = nombre de protons du noyau (et d’électrons pour l’atome neutre).",
     "question":"Quel est Z pour l’oxygène ? et pour le sodium ?",
     "solution":"O : 8 ; Na : 11.",
     "accept":[r"(8.*11|11.*8)"]},

    {"theme":"Nombre de masse A",
     "recap":"A = Z + N (protons + neutrons).",
     "question":"Pour O-16 (A=16, Z=8), calcule N.",
     "solution":"N = 8 neutrons.",
     "accept":[r"\\b8\\b"]},

    {"theme":"Isotopes",
     "recap":"Même Z, A différent (donc N différent). Propriétés chimiques semblables, masses différentes.",
     "question":"Donne deux isotopes du carbone.",
     "solution":"12C et 13C (14C radioactif).",
     "accept":[r"(12\\s*C|C\\s*12)", r"(13\\s*C|C\\s*13)"]},

    {"theme":"Nuage électronique",
     "recap":"Modèle quantique : probabilité de présence, pas d’orbites classiques.",
     "question":"Pourquoi parle-t-on de « nuage » plutôt que d’orbites ?",
     "solution":"On décrit des zones de probabilité / incertitude sur la position.",
     "accept":[r"probabilit|incertitud|zones? de pr[ée]sence|nuage"]},

    {"theme":"Couches K, L, M",
     "recap":"Capacités max usuelles : K:2, L:8, M:18 (règle 2n², version seconde).",
     "question":"Combien d’électrons max sur la couche L ?",
     "solution":"8 électrons.",
     "accept":[r"\\b8\\b"]},

    {"theme":"Règle de remplissage (1s → 3p)",
     "recap":"Remplissage par énergie croissante : 1s, 2s, 2p, 3s, 3p (simplifié).",
     "question":"Après 2p, quelle sous-couche se remplit ?",
     "solution":"3s.",
     "accept":[r"\\b3s\\b"]},

    {"theme":"Configuration du sodium (Z=11)",
     "recap":"Na : 1s² 2s² 2p⁶ 3s¹ (K2 L8 M1).",
     "question":"Combien d’électrons de valence pour Na ?",
     "solution":"1 électron de valence.",
     "accept":[r"\\b1\\b|\\bun\\b"]},

    {"theme":"Gaz nobles & stabilité",
     "recap":"Couches externes saturées (Ne, Ar) → grande stabilité chimique.",
     "question":"Pourquoi le néon est-il peu réactif ?",
     "solution":"Couche de valence complète (configuration stable).",
     "accept":[r"valence compl[èe]te|couche.*compl[èe]te|stable"]},

    {"theme":"Électrons de valence",
     "recap":"Électrons de la couche externe → réactivité.",
     "question":"Combien pour le chlore (Z=17) ?",
     "solution":"7 électrons de valence.",
     "accept":[r"\\b7\\b|\\bsept\\b"]},

    {"theme":"Ions : cations & anions",
     "recap":"Perte d’e− → cation ; gain d’e− → anion.",
     "question":"Na devient Na⁺ : que s’est-il passé ?",
     "solution":"Na a perdu un électron.",
     "accept":[r"perdu.*[ée]lectron|perdu un electron"]},

    {"theme":"Liaison ionique vs covalente",
     "recap":"Ionique : transfert (NaCl). Covalente : partage (H₂O, O₂).",
     "question":"Classe H₂O, NaCl, O₂ par type de liaison.",
     "solution":"NaCl ionique ; H₂O et O₂ covalentes.",
     "accept":[r"ionique.*NaCl|NaCl.*ionique"]},

    {"theme":"Tableau périodique",
     "recap":"Organisation par Z ; périodicité ; colonnes = familles.",
     "question":"À quelle famille appartient le chlore ?",
     "solution":"Aux halogènes (colonne 17).",
     "accept":[r"halog[èe]nes?"]},

    {"theme":"Tendance périodique – valence",
      "recap":"Même colonne → même nb d’électrons de valence → propriétés proches.",
      "question":"Compare Mg (Z=12) et Ca (Z=20).",
      "solution":"Même colonne (alcalino-terreux), 2 électrons de valence.",
      "accept":[r"m[êe]me colonne|alcalino.?terreux|2 (é|e)lectrons"]},

    {"theme":"Masse atomique relative",
     "recap":"Moyenne pondérée des isotopes naturels → pas toujours entière.",
     "question":"Pourquoi la masse atomique du Cl (~35,45) n’est pas entière ?",
     "solution":"Mélange d’isotopes 35Cl et 37Cl.",
     "accept":[r"isotopes?|35.?Cl|37.?Cl|m[ée]lange"]},

    {"theme":"Réactions : conservation",
     "recap":"Les atomes se réarrangent ; nombre et nature conservés.",
     "question":"Dans H₂ + O₂ → H₂O, que deviennent les atomes ?",
     "solution":"Ils se réorganisent en molécules d’eau ; aucun atome créé/détruit.",
     "accept":[r"r[ée]organisent|pas cr[ée]s?|pas d[ée]truits?"]},

    {"theme":"Atomes et étoiles",
     "recap":"Éléments lourds formés dans les étoiles et supernovæ (nucléosynthèse).",
     "question":"En une phrase : comment naissent les éléments ?",
     "solution":"Fusion stellaire et supernovæ.",
     "accept":[r"fusion|supernov|nucl[ée]osynth[èe]se"]},

    {"theme":"Radioactivité (intro)",
     "recap":"Transformation spontanée de noyaux instables (α, β, γ).",
     "question":"Cite un usage médical d’un radioisotope.",
     "solution":"Imagerie/Traitement (iode-131, technétium-99m).",
     "accept":[r"iode.?131|techn[ée]tium.?99m|imagerie|traitement|scintigraphie"]},
]

# ---------------------- État & utilitaires ----------------------
if "scores" not in st.session_state:
    st.session_state.scores = {i+1: None for i in range(24)}  # 1 correct, 0 faux, None non évalué
if "answers" not in st.session_state:
    st.session_state.answers = {i+1: "" for i in range(24)}
if "log" not in st.session_state:
    st.session_state.log = []  # liste de dicts {timestamp, day, answer, correct, student_id}

def french_date_for(day:int):
    return f"{day} déc."

def evaluate(day:int, text:str) -> int:
    patt = DAYS[day-1]["accept"]
    if not patt:
        return 0
    text = (text or "").strip().lower()
    hits = 0
    for p in patt:
        if re.search(p, text, flags=re.I):
            hits += 1
    return 1 if (len(patt) >= 2 and hits >= 2) or (len(patt) == 1 and hits >= 1) else 0

# ---------------------- Barre latérale ----------------------

student_id = st.sidebar.text_input("Identifiant élève (ex: Prénom_Nom ou code)", value="", placeholder="Ex: Lea_Dupont ou 2nde3-05")
lock = st.sidebar.toggle("Verrouiller par date (1–24 décembre)", value=False)
today = date.today()
st.sidebar.markdown(f"**Aujourd’hui :** {today.day} {today.strftime('%b')}.")

# Stats globales
values = [v for v in st.session_state.scores.values() if v is not None]
total = sum(v for v in values) if values else 0
done = len(values)
colA, colB = st.sidebar.columns(2)
colA.metric("Jours validés", f"{done}/24")
colB.metric("Score total", f"{total}/24")
st.sidebar.progress(total/24 if total else 0.0, text="Progression")

# Boutons admin
colx, coly = st.sidebar.columns(2)
if colx.button("🔄 Réinitialiser", use_container_width=True):
    st.session_state.scores = {i+1: None for i in range(24)}
    st.session_state.answers = {i+1: "" for i in range(24)}
    st.session_state.log = []
    st.rerun()

# Export CSV (journal des tentatives)
if st.session_state.log:
    # Préparer CSV en mémoire
    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=["timestamp","student_id","day","answer","correct"])
    writer.writeheader()
    for row in st.session_state.log:
        writer.writerow(row)
    csv_bytes = output.getvalue().encode("utf-8")
    st.sidebar.download_button("⬇️ Exporter journal CSV", data=csv_bytes, file_name="avent_atomes_resultats.csv", mime="text/csv", use_container_width=True)
else:
    st.sidebar.caption("Aucun résultat à exporter pour l’instant.")

# ---------------------- Titre ----------------------

st.caption("Écris ta réponse puis clique « Vérifier ». Feedback immédiat ✅/❌, score enregistré (1 point par bonne réponse).")

# ---------------------- Affichage des jours ----------------------
cols = st.columns(4, gap="small")
for i in range(24):
    day = i + 1
    with cols[i % 4]:
        locked = lock and not (today.month == 12 and day <= min(24, today.day))
        badge = "🔒" if locked else ("✅" if st.session_state.scores[day] == 1 else ("❌" if st.session_state.scores[day] == 0 else "🗓️"))
        with st.expander(f"{badge} Jour {day} — {DAYS[i]['theme']}", expanded=False):
            st.markdown(f"**À ouvrir le :** {french_date_for(day)}")
            st.markdown(f"> *Rappel express* : {DAYS[i]['recap']}")
            st.markdown(f"**Question :** {DAYS[i]['question']}")

            if locked:
                st.info("Cette case est verrouillée (mode calendrier). Reviens le bon jour !")
            else:
                key_ans = f"ans_{day}"
                key_btn = f"btn_{day}"

                st.session_state.answers[day] = st.text_input(
                    "Ta réponse :", value=st.session_state.answers[day],
                    key=key_ans, placeholder="Écris ici ta réponse…"
                )

                if st.button("Vérifier", key=key_btn, use_container_width=True):
                    res = evaluate(day, st.session_state.answers[day])
                    if st.session_state.scores[day] is None:
                        st.session_state.scores[day] = res
                    # Feedback + log
                    ts = datetime.now().isoformat(timespec="seconds")
                    st.session_state.log.append({
                        "timestamp": ts,
                        "student_id": student_id or "anonyme",
                        "day": day,
                        "answer": st.session_state.answers[day],
                        "correct": int(res),
                    })
                    if res == 1:
                        st.success("✅ Correct ! " + (DAYS[i]["solution"] or ""))
                    else:
                        st.error("❌ Incorrect. Indice : " + (DAYS[i]["recap"] or ""))

                # Si déjà évalué, afficher l'état et la solution
                if st.session_state.scores[day] is not None:
                    if st.session_state.scores[day] == 1:
                        st.success("✅ Bonne réponse enregistrée.")
                    else:
                        with st.expander("Voir un élément de solution", expanded=False):
                            st.write(DAYS[i]["solution"])

# ---------------------- Footer ----------------------
st.divider()
st.caption("« Tout est fait d’atomes. » — Richard Feynman | Conçu pour le niveau Seconde • Structure de l’atome • Z • Isotopes • Config. électronique • Ions • Liaisons • Tableau périodique.")
