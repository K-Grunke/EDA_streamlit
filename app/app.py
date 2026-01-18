import streamlit as st
import os
import sys

# 🔧 WAŻNE: Streamlit nie dodaje automatycznie katalogów do sys.path
# Musimy ręcznie dodać ścieżkę do src, żeby importy działały
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

try:
    from src.data_loader import load_data
    from src.eda import show_eda
    from src.components.sidebar import render_eda_sidebar
except ImportError as e:
    st.error(f"Błąd importu: {e}")
    st.info("Uruchom z głównego katalogu projektu: streamlit run app/app.py")
    st.stop()

# 🎨 CUSTOM CSS DLA STREAMLIT
# Streamlit pozwala na custom stylizację przez unsafe_allow_html=True
# To jedyne miejsce gdzie używamy HTML/CSS bezpośrednio
st.markdown(""" 
<style>
div.stButton > button {
    background-color: #181818;
    color: white;
    border-radius: 8px;
    padding: 0.6rem 1.2rem;
    border: 1px solid #181818;
    transition: 0.3s;
    font-weight: 600;
}
div.stButton > button:hover {
    background-color: #1DB954;
    border-color: #1DB954;
    color: #000;
    transform: scale(1.03);
}
body {
    background: linear-gradient(135deg, #0b0d19 0%, #15172d 40%, #1c0f2e 100%);
}
[data-testid="stSidebar"] a {
    color: inherit !important;
    text-decoration: none !important;
    font-weight: normal !important;
}
[data-testid="stSidebar"] a:hover {
    color: inherit !important;
    text-decoration: none !important;
}
</style>
""", unsafe_allow_html=True)

# ⚙️ KONFIGURACJA STRONY STREAMLIT
# set_page_config MUSI być pierwszym wywołaniem Streamlit
st.set_page_config(
    page_title="Data Science Salaries Dashboard",
    page_icon="💼",
    layout="wide"
)

# 💾 CACHE DANYCH - KLUCZOWA OPTYMALIZACJA
# Bez @st.cache_data Streamlit wczytywałby dane przy KAŻDYM rerunie
# Decorator cache'uje wynik funkcji między rerunami
@st.cache_data
def load_cached_data():
    # Ładuje i cache'uje dane.
    # Uwaga: @st.cache_data automatycznie wykrywa zmiany w argumentach
    # Jeśli zmieni się plik CSV, cache się unieważni.
    
    # Używamy ścieżki względnej od lokalizacji app.py
    data_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'DataScience_salaries_2025.csv')
    return load_data(data_path)

# 🚀 GŁÓWNA FUNKCJA APLIKACJI 
def main():
    try:
        # ⚡ DANE SĄ CACHE'OWANE - szybkie ładowanie przy kolejnych interakcjach
        df = load_cached_data()
    except FileNotFoundError as e:
        st.error(f"Nie znaleziono pliku z danymi: {e}")
        st.info("Upewnij się, że plik data/DataScience_salaries_2025.csv istnieje")
        return
    
     #SIDEBAR - główna nawigacja
    st.sidebar.title("📊 Data Science Salaries")
    st.sidebar.markdown("---")
    
    # Wybór sekcji
    menu = st.sidebar.radio(
        "Wybierz sekcję:",
        ["🏠 Strona główna", "📈 Analiza danych (EDA)", "🤖 Model predykcyjny"],
        index=1
    )
    
    if menu == "🏠 Strona główna":
        st.title("💼 Dashboard Wynagrodzeń Data Science")
        st.markdown("""
        ### Witaj w interaktywnym dashboardzie analizy wynagrodzeń w Data Science!
        
        Ten projekt powstał w ramach pracy studenckiej i ma na celu:
        - 📊 Analizę trendów wynagrodzeń w latach 2020-2025
        - 🌍 Porównania geograficzne
        - 💰 Identyfikację najlepiej płatnych stanowisk
        - 📈 Wizualizację rozkładu wynagrodzeń
        
        **Jak korzystać:**
        1. Wybierz "Analiza danych (EDA)" w menu po lewej
        2. Eksploruj różne sekcje analizy
        3. Korzystaj z interaktywnych wykresów
        """)
        
        st.info("💡 Projekt jest otwarty na dyskusję, rozwój i współpracę! Jeśli masz pomysły, sugestie lub chcesz się przyłączyć - zapraszam do kontaktu!")
        
    # 📈 SEKCJA EDA - główny showcase Streamlit
    elif menu == "📈 Analiza danych (EDA)":
        # Sidebar z nawigacją dla EDA
        render_eda_sidebar()
        # Główna zawartość EDA
        show_eda(df)
        
    # 🤖 SEKCJA MODEL PREDYKCYJNY - placeholder na przyszłość
    elif menu == "🤖 Model predykcyjny":
        st.title("🤖 Model Predykcyjny")
        st.warning("🎯 Sekcja w przygotowaniu! Pracuję nad modelem predykcyjnym wynagrodzeń.")
        st.markdown("""
        Planowane funkcjonalności:
        - Predykcja wynagrodzenia na podstawie doświadczenia, lokalizacji i stanowiska
        - Analiza trendów przyszłych wynagrodzeń
        - Porównanie z rzeczywistymi danymi
        """)

if __name__ == "__main__":
    main()