
# Prototype final : Analyse AI XAUUSD (avec Résumés Français et Importance)
import streamlit as st
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from gtts import gTTS
import os

# ----- NOUVEAU : Analyse et résumé intelligent -----
def get_relevant_fxstreet_articles():
    url = "https://www.fxstreet.com/news"
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')

    articles = []
    for link in soup.find_all('a', href=True):
        title = link.get_text(strip=True)
        if "gold" in title.lower() or "xauusd" in title.lower():
            articles.append(title)
    return articles

# ----- Détection de sentiment et résumé simulé -----
def generate_french_summary(title):
    title_lower = title.lower()
    if any(word in title_lower for word in ["fed", "pivot", "inflation", "banking crisis"]):
        importance = "🟥 Article critique"
    elif any(word in title_lower for word in ["target", "breakout", "rally", "safe haven"]):
        importance = "🟧 Article influent"
    else:
        importance = "🟨 Article modéré"

    if any(word in title_lower for word in ["rally", "bullish", "rise", "bid"]):
        sentiment = "📈 Haussier"
    elif any(word in title_lower for word in ["drop", "bearish", "fall", "weaken"]):
        sentiment = "📉 Baissier"
    else:
        sentiment = "➖ Neutre"

    resume = f"Résumé : Cet article suggère que {title}."
    return importance, resume, sentiment

# ----- Simule les news économiques -----
def get_myfxbook_news():
    return [
        {"heure": "14:30", "event": "Core PCE Price Index (USD)", "impact": "High", "prévu": "0.3%", "précédent": "0.2%"},
        {"heure": "16:00", "event": "Michigan Consumer Sentiment (USD)", "impact": "Medium", "prévu": "67.0", "précédent": "65.0"}
    ]

# ----- STREAMLIT UI -----
def main():
    st.set_page_config(page_title="Analyse AI XAUUSD", layout="centered")
    st.markdown("""
        <style>
        .stButton>button {
            background-color: #007BFF;
            color: white;
            border-radius: 10px;
            padding: 0.5em 2em;
            font-weight: bold;
            border: none;
        }
        .stButton>button:hover {
            background-color: #0056b3;
        }
        </style>
    """, unsafe_allow_html=True)

    st.title("🔍 Analyse AI XAUUSD")
    st.markdown("**Résumé des nouvelles économiques et des articles influents sur l'or.**")

    if st.button("Lancer l'analyse du jour"):
        with st.spinner("Analyse des articles en cours..."):
            articles = get_relevant_fxstreet_articles()
            news = get_myfxbook_news()

            st.subheader("📰 Résumés intelligents des articles FXStreet")
            if not articles:
                st.warning("Aucun article pertinent trouvé aujourd'hui.")
            else:
                for article in articles:
                    importance, resume, sentiment = generate_french_summary(article)
                    st.markdown(f"### {importance}")
                    st.markdown(f"**{article}**")
                    st.markdown(f"{resume}")
                    st.markdown(f"➡️ Sentiment détecté : **{sentiment}**\n---")

            st.subheader("📅 News économiques du jour")
            for event in news:
                st.markdown(f"- ⏰ {event['heure']} - **{event['event']}** | Impact: `{event['impact']}` | Prévu: `{event['prévu']}` | Précédent: `{event['précédent']}`")

if __name__ == "__main__":
    main()
