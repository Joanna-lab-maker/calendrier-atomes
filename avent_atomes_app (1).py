
import io, csv
from datetime import date, datetime
import streamlit as st

st.set_page_config(page_title="Calendrier de l’Avent — QCM Atomes (Seconde – J.A.)",
                   page_icon="⚛️", layout="wide")
# Masquer le menu, l’icône GitHub et la déco du header
st.markdown("""
<style>
#MainMenu {visibility: hidden;}                 /* menu "⋮" */
footer {visibility: hidden;}                   /* pied de page */
[data-testid="stToolbar"]{display:none!important;}      /* barre du haut */
header [data-testid="stDecoration"]{display:none!important;} /* ruban coloré */
header a[href*="github.com"]{display:none!important;}   /* icône/lien GitHub */
header button[kind="header"]{display:none!important;}   /* autres boutons header */
</style>
""", unsafe_allow_html=True)


DAYS = [
    {
        "theme": "Devinette — Quel atome ?",
        "recap": "Atome neutre : nbre d’électrons = Z. e = 1,60 × 10⁻¹⁹ C.",
        "question": "Mon cortège électronique a une charge égale à −6,4 × 10⁻¹⁹ C et ma charge totale est nulle. Mon noyau contient un neutron de plus que de protons. Qui suis-je ?",
        "qcm": {"a": "Hydrogène-1 (protium)", "b": "Hydrogène-2 (deutérium)", "c": "Béryllium-9"},
        "answer": "c",
        "solution": "−6,4×10⁻¹⁹ C = −4e ⇒ 4 e− ⇒ Z=4 (béryllium). « Un neutron de plus » ⇒ N=5 ⇒ ⁹Be."
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
        "solution": "A ≈ (5,0×10⁻²⁶) / (1,67×10⁻²⁷) ≈ 30."
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
        "recap": "Isotopes stables : ⁶³Cu et ⁶⁵Cu (Z=29).",
        "question": "Quel isotope contient le plus de neutrons ?",
        "qcm": {"a": "⁶³Cu", "b": "⁶⁵Cu", "c": "Ils ont le même N"},
        "answer": "b",
        "solution": "Même Z, A plus grand ⇒ plus de neutrons."
    },
    {
        "theme": "Isotopes du carbone — Électrons",
        "recap": "Atome neutre : nbre d’électrons = Z. Pour C, Z=6.",
        "question": "Combien d’électrons possède l’atome neutre de carbone-14 ?",
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
        "solution": "Z = 6."
    },
    {
        "theme": "Électrons de valence",
        "recap": "Les électrons de la couche externe déterminent la réactivité.",
        "question": "Config : 1s² 2s² 2p⁶ 3s² 3p³. Combien d’électrons sur la couche externe ?",
        "qcm": {"a": "3", "b": "5", "c": "7"},
        "answer": "b",
        "solution": "Couche n=3 : 3s²3p³ ⇒ 2 + 3 = 5."
    },
    {
        "theme": "Famille chimique — azote vs phosphore",
        "recap": "Même colonne ⇒ même motif externe ns² np³ ; P est une période en dessous de N.",
        "question": "L’azote a 1s² 2s² 2p³. Pour le phosphore (période suivante), quelle configuration ?",
        "qcm": {"a": "1s² 2s² 2p⁵", "b": "1s² 2s² 2p⁶ 3s² 3p³", "c": "1s² 2s² 2p⁶ 3s² 3p⁵"},
        "answer": "b",
        "solution": "Même motif externe mais niveau n=3 : 1s² 2s² 2p⁶ 3s² 3p³."
    },
  {
  "theme": "Famille chimique — Configuration électronique",
  "recap": "Deux éléments appartiennent à la même famille chimique s’ils ont le même nombre d’électrons sur leur couche externe.",
  "question": "Deux atomes ont pour configuration électronique 1s² 2s² 2p² et 1s² 2s² 2p⁴. Appartiennent-ils à la même famille chimique ?",
  "qcm": {
      "a": "Oui, car ils ont le même nombre d’électrons de valence.",
      "b": "Non, car ils n’ont pas le même nombre d’électrons de valence.",
      "c": "Oui, car ils sont dans la même période."
  },
  "answer": "b",
  "solution": "Le premier atome a 4 électrons de valence, le second en a 6. Ils n’appartiennent donc pas à la même famille chimique.",
  "image": "https://raw.githubusercontent.com/Joanna-lab-maker/calendrier-atomes/main/images/jour11.png"
},
  {
  "theme": "Ions de NaCl — L’ion chlorure Cl⁻",
  "recap": "Un ion négatif (anion) résulte du gain d’électron(s). Pour le chlore : Z = 17 (→ 17 protons). Cl⁻ possède donc 18 électrons.",
  "question": "À propos de l’ion chlorure Cl⁻, quelle proposition est correcte ?",
  "qcm": {
      "a": "Il a perdu 1 électron ; c’est un cation ; 17 p⁺ et 16 e⁻.",
      "b": "Il a gagné 1 électron ; c’est un anion ; 17 p⁺ et 18 e⁻.",
      "c": "Il a gagné 1 électron ; c’est un cation ; 18 p⁺ et 17 e⁻."
  },
  "answer": "b",
  "solution": "Cl a Z = 17 ⇒ 17 protons. En devenant Cl⁻, il gagne 1 e⁻ ⇒ 18 électrons. Un ion de charge négative est un anion.",
  # "image": "https://raw.githubusercontent.com/Joanna-lab-maker/calendrier-atomes/main/images/jour12.png"
},

] + [
    {
        "theme": "À compléter",   # <-- on enlève "Jour {d} —"
        "recap": "Ajoute ta question + image (optionnel).",
        "question": "Question QCM…",
        "qcm": {"a": "Réponse A", "b": "Réponse B", "c": "Réponse C"},
        "answer": "a",
        "solution": "Explication de la bonne réponse."
    } for d in range(11, 25)
]
