import streamlit as st

def show_intro_section():
    """Pokazuje sekcję wprowadzającą."""
    st.markdown('<a id="intro"></a>', unsafe_allow_html=True)
    st.title("💼 Analiza Wynagrodzeń w Data Science — Lata 2020–2025")
    
    st.markdown("""
    Witaj w interaktywnym dashboardzie prezentującym ewolucję globalnych wynagrodzeń w branży Data Science 
    na przestrzeni lat 2020–2025. Opracowanie powstało na podstawie bogatego zbioru danych obejmującego 
    ponad 93 000 rekordów z całego świata.
    
    ### 🔍 Co oferuje ta analiza?
    - **Trendy w czasie**: wzrosty i spadki wynagrodzeń
    - **Porównania stanowisk**: od analityków po badaczy AI
    - **Analizy geograficzne**: różnice między krajami i regionami
    - **Rozkład wynagrodzeń**: statystyki i dystrybucja zarobków
    
    ### 🌍 Dlaczego warto to sprawdzić?
    Zrozumienie trendów wynagrodzeń jest kluczowe dla:
    - Profesjonalistów planujących karierę w data science
    - Studentów wybierających ścieżkę zawodową
    - Firm rekrutujących talenty
    - Wszystkich zainteresowanych rynkiem pracy w tech
    """)
    
    st.divider()