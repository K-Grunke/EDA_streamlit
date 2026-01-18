# 🗺️ MODUŁ: Mapy i wizualizacje geograficzne

# Demonstruje integrację Streamlit z:
# 1. Plotly Express (mapy choropleth)
# 2. PyCountry (konwersja kodów krajów)
# 3. Pandas (agregacja danych)

# WAŻNE: Plotly wymaga kodów ISO-3 dla map świata
# Nasze dane mają ISO-2, więc konwertujemy.


import plotly.express as px
import pycountry
import pandas as pd

# 🔄 KONWERSJA: ISO-2 → ISO-3
    
#     Problem: Nasze dane mają kody 2-literowe (US, PL, DE)
#     Plotly chce 3-literowe (USA, POL, DEU) dla map świata
    
#     Uwagi:
#     - Nie wszystkie kody da się skonwertować (np. 'EU', 'XX')
#     - PyCountry wymaga pip install pycountry
#     - Zwraca None dla nieznanych kodów (obsługa błędów)

def iso2_to_iso3(code):
    """
    Konwertuje kod kraju ISO-2 na ISO-3.
    
    Args:
        code: Kod ISO-2 (np. 'US', 'PL')
    
    Returns:
        str: Kod ISO-3 lub None jeśli konwersja się nie powiedzie
    """
    try:
        return pycountry.countries.get(alpha_2=code).alpha_3
    except:
        return None

def create_world_map(df, location_column="company_location"):
    #  🗺️ TWORZENIE MAPY ŚWIATA
    
    # Args:
    #     df: DataFrame z danymi
    #     location_column: 'company_location' lub 'employee_residence'
    
    # Returns:
    #     plotly.graph_objects.Figure: Gotowa mapa
    
    # Demonstruje:
    # - Grupowanie danych z Pandas
    # - Konwersję kodów krajów
    # - Tworzenie mapy choropleth z Plotly
    # - Obsługę brakujących wartości (dropna)
    
    # 📊 AGREGUJ DANE - średnie wynagrodzenie per kraj
    location_stats = (
        df.groupby(location_column)
        .agg(mean_salary=("salary_in_usd", "mean"))
        .reset_index()
    )
    
    # 🔄 KONWERTUJ KODY KRAJÓW
    # Uwaga: To może być wolne dla dużych datasetów
    location_stats["iso3"] = location_stats[location_column].apply(iso2_to_iso3)
    
    # Usuń kraje bez poprawnego kodu ISO3
    location_stats = location_stats.dropna(subset=['iso3'])
    
    # Tworzenie mapy
    if location_column == "company_location":
        title = "Średnie wynagrodzenia — lokalizacja firm"
    else:
        title = "Średnie wynagrodzenia — lokalizacja pracowników"
    
    # 🗺️ TWORZENIE MAPY CHOROPLETH
    # Plotly automatycznie skaluje kolory do zakresu wartości
    fig = px.choropleth(
        location_stats,
        locations="iso3",
        color="mean_salary",
        hover_name=location_column,
        color_continuous_scale="Viridis",
        title=title,
        labels={"mean_salary": "Średnie wynagrodzenie (USD)"}
    )
    
    return fig

def create_company_vs_employee_maps(df):
    # Tworzy dwie mapy: dla lokalizacji firm i pracowników.
    
    # Args:
    #     df: DataFrame z danymi
    
    # Returns:
    #     tuple: (fig_company, fig_employee) - dwie mapy
    # Mapa dla firm
    fig_company = create_world_map(df, "company_location")
    fig_company.update_layout(title="📍 Średnie wynagrodzenia — lokalizacja firm")
    
    # Mapa dla pracowników
    fig_employee = create_world_map(df, "employee_residence")
    fig_employee.update_layout(title="👤 Średnie wynagrodzenia — lokalizacja pracowników")
    
    return fig_company, fig_employee