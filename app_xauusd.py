
import streamlit as st
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from gtts import gTTS
import os

def scrape_fxstreet_xauusd():
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

def analyze_sentiment(text):
    if any(word in text.lower() for word in ["rally", "bullish", "buy"]):
        return "📈 Haussier"
    elif any(word in text.lower() for word in ["drop", "bearish", "sell"]):
        return "📉 Baissier"
    else:
        return "➖ Neutre"

def get_myfxbook_news():
    simulated_news = [
        {"heure": "14:30", "event": "Core PCE Price Index (USD)", "impact": "High", "prévu": "0.3%", "précédent": "0.2%"},
        {"heure": "16:00", "event": "Michigan Consumer Sentiment (USD)", "impact": "Medium", "prévu": "67.0", "précédent": "65.0"}
    ]
    return simulated_news

def generate_summary(articles, news):
    summary = "Résumé de l'analyse XAUUSD du jour. "
    if not articles:
        summary += "Aucun article pertinent n'a été trouvé aujourd'hui sur FXStreet."
    else:
        sentiments = [analyze_sentiment(a) for a in articles]
        summary += f"{len(articles)} articles trouvés. Sentiments détectés : {', '.join(sentiments)}."
    summary += " Côté économique, voici les événements importants : "
    for n in news:
        summary += f"À {n['heure']}, {n['event']} avec un impact {n['impact']}, prévu à {n['prévu']}, précédent {n['précédent']}. "
    return summary

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
    st.markdown("**Stratégie propulsée par l'intelligence artificielle.**")

    if st.button("Lancer l'analyse du jour"):
        with st.spinner('Analyse en cours...'):
            articles = scrape_fxstreet_xauusd()
            news = get_myfxbook_news()

            st.subheader("📰 Articles FXStreet")
            if not articles:
                st.warning("Aucun article pertinent trouvé aujourd'hui.")
            else:
                for article in articles:
                    sentiment = analyze_sentiment(article)
                    st.markdown(f"**{article}**\n> Sentiment détecté : {sentiment}")

            st.subheader("📅 News économiques du jour (simulation)")
            for event in news:
                st.markdown(f"- ⏰ {event['heure']} - **{event['event']}** | Impact: `{event['impact']}` | Prévu: `{event['prévu']}` | Précédent: `{event['précédent']}`")

            if st.button("🎙️ Générer résumé audio"):
                summary_text = generate_summary(articles, news)
                tts = gTTS(text=summary_text, lang='fr')
                audio_path = "resume_xauusd.mp3"
                tts.save(audio_path)
                audio_file = open(audio_path, "rb")
                st.audio(audio_file.read(), format='audio/mp3')
                audio_file.close()

if __name__ == "__main__":
    main()
