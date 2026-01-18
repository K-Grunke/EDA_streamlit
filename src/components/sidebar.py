import streamlit as st

def render_eda_sidebar():
    """Renderuje sidebar z nawigacją dla sekcji EDA."""
    st.sidebar.markdown("## 📚 Nawigacja EDA")
    st.sidebar.markdown("""
- [💼 Analiza Wynagrodzeń 2020–2025](#intro)
- [📊 Przegląd danych](#dataset_overview)
  - [📈 Podstawowe statystyki](#statistics)
- [⏳ Trendy wynagrodzeń w czasie](#time_trends)
- [💰 Analiza wynagrodzeń](#salary_analysis)
  - [🏆 Top 10 najlepiej płatnych](#salary_top10)
  - [🔍 Analiza stanowiska](#salary_detail)
- [🌍 Analiza geograficzna](#geo_analysis)
  - [🌎 Globalne wynagrodzenia](#geo_global)
  - [🗺️ Mapa wynagrodzeń](#geo_map)
  - [📌 Porównanie krajów](#geo_compare)
- [📊 Rozkład wynagrodzeń (USD)](#salary_distribution)
  - [📈 Statystyki rozkładu](#salary_stats)
""", unsafe_allow_html=True)