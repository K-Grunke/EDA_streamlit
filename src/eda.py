
# 🎯 MODUŁ GŁÓWNY DASHBOARDU EDA

# Ten moduł demonstruje jak organizować duży dashboard Streamlit:
# 1. Każda sekcja to osobna funkcja - modularność
# 2. Używamy anchorów HTML do nawigacji (ograniczenie Streamlit)
# 3. Separacja UI od logiki biznesowej
# 4. Integracja z komponentami wizualizacji

# STRUKTURA:
# - show_eda() - główna funkcja orchestrator
# - Każda podsekcja to osobna funkcja
# - Użycie st.container() do grupowania


import streamlit as st
import pandas as pd
import numpy as np
from src.visualization.charts import (
    create_salary_trend_chart,
    create_top_jobs_chart,
    create_salary_distribution_chart,
    create_country_comparison_chart
)
from src.visualization.maps import create_world_map, create_company_vs_employee_maps
from src.components.menu import show_intro_section

def show_dataset_overview(df):
     
    # 📊 SEKCJA: Przegląd danych
    
    # Pokazuje:
    # - Raw danych w expanderze (optymalizacja pamięci)
    # - Podstawowe informacje o dataset
    
    # Uwaga: st.dataframe(df) może być wolne dla dużych datasetów
    # Dlatego umieszczamy w expanderze (ładowane na żądanie)
    
    # 🎯 ANCHOR HTML - pozwala na nawigację wewnątrz strony
    # Streamlit nie ma natywnego routing, więc używamy HTML anchor
    """Pokazuje przegląd danych."""
    st.markdown('<a id="dataset_overview"></a>', unsafe_allow_html=True)
    st.header("📊 Przegląd danych")
    with st.expander("Rozwiń dane", expanded=False):
        st.dataframe(df)

def show_statistics(df):
    # 📈 SEKCJA: Podstawowe statystyki
    
    # Pokazuje:
    # - Metryki w kolumnach (st.columns)
    # - Szczegółowe statystyki w expanderze
    
    # Demonstruje:
    # - st.metric() dla KPI
    # - st.columns() dla layoutu
    # - df.describe() integracja z Pandas
    """Pokazuje podstawowe statystyki."""
    st.markdown('<a id="statistics"></a>', unsafe_allow_html=True)
    st.subheader("📈 Podstawowe statystyki")
    
     # 🎪 LAYOUT KOLUMNOWY - responsive design w Streamlit
    col1, col2, col3 = st.columns(3)
    col1.metric("Liczba rekordów", f"{df.shape[0]:,}", border=True)
    col2.metric("Unikalne stanowiska", f"{df['job_title'].nunique():,}", border=True)
    col3.metric("Kraje (firmy)", f"{df['company_location'].nunique():,}", border=True)

    col4, col5, col6 = st.columns(3)
    col4.metric("Średnie wynagrodzenie", f"{int(df['salary_in_usd'].mean()):,} USD", border=True)
    col5.metric("Mediana", f"{int(df['salary_in_usd'].median()):,} USD", border=True)
    col6.metric("Maksymalne", f"{int(df['salary_in_usd'].max()):,} USD", border=True)

    # 📦 EXPANDER ZE SZCZEGÓŁOWYMI STATYSTYKAMI
    # Pandas .describe() daje pełny przegląd
    with st.expander("Szczegółowe statystyki", expanded=False):
        st.write(df[['work_year', 'salary', 'salary_in_usd']].describe())
    
    st.divider()

def show_time_trends(df):
    # ⏳ SEKCJA: Trendy czasowe
    
    # Demonstruje:
    # - Przyciski zamiast radio (lepsze UX w dashboardzie)
    # - Dynamiczne zmiany wykresów
    # - Integracja z Plotly przez custom komponenty
    
    # Uwaga: Streamlit rerunuje przy każdym kliknięciu przycisku
    # Dlatego używamy przycisków zamiast on_change

    """Pokazuje trendy czasowe."""
    st.markdown('<a id="time_trends"></a>', unsafe_allow_html=True)
    st.header("⏳ Trendy wynagrodzeń w czasie")
    
    col1, col2, col3 = st.columns(3)
    
    # 🔘 KAŻDY PRZYCISK WYWOŁUJE RERUN I POKAZUJE INNY WYKRES
    if col1.button("Średnie wynagrodzenie", use_container_width=True):
        fig = create_salary_trend_chart(df, 'mean')
        st.plotly_chart(fig, use_container_width=True)
    
    if col2.button("Mediana", use_container_width=True):
        fig = create_salary_trend_chart(df, 'median')
        st.plotly_chart(fig, use_container_width=True)
    
    if col3.button("Liczba ofert", use_container_width=True):
        fig = create_salary_trend_chart(df, 'count')
        st.plotly_chart(fig, use_container_width=True)
    
    st.divider()

def show_salary_analysis(df):
    # 💰 SEKCJA: Analiza wynagrodzeń
    
    # Najbardziej złożona sekcja pokazująca:
    # - Interaktywne filtry (slider)
    # - Dynamiczne tabele i wykresy
    # - Selectbox z live filtering
    # - Multiple layout patterns
    
    """Analiza wynagrodzeń."""
    st.markdown('<a id="salary_analysis"></a>', unsafe_allow_html=True)
    st.header("💰 Analiza wynagrodzeń")
    
    # Top 10 stanowisk
    st.markdown('<a id="salary_top10"></a>', unsafe_allow_html=True)
    st.subheader("🏆 Top 10 najlepiej płatnych stanowisk")

    # 🎚️ SLIDER DO FILTROWANIA DANYCH
    # Pokazuje jak dane wejściowe wpływają na wyniki
    min_count = st.slider("Minimalna liczba rekordów:", 10, 300, 50, 10)
    
    job_stats = (
        df.groupby('job_title')
        .agg(mean_salary=('salary_in_usd', 'mean'), count=('salary_in_usd', 'count'))
        .reset_index()
    )
    job_stats_filtered = job_stats[job_stats['count'] >= min_count]
    top10 = job_stats_filtered.sort_values('mean_salary', ascending=False).head(10)
    
     # 2-KOLUMNOWY LAYOUT: tabela + wykres
    col1, col2 = st.columns(2)
    with col1:
        # 📋 TABELA DANYCH - st.dataframe z custom headers
        st.dataframe(
            top10.rename(columns={
                "job_title": "Stanowisko",
                "mean_salary": "Średnie wynagrodzenie (USD)",
                "count": "Liczba rekordów"
            }),
            use_container_width=True
        )
    
    with col2:
        # 📈 WYKRES POZIOMY - lepszy dla długich nazw
        fig = create_top_jobs_chart(top10)
        st.plotly_chart(fig, use_container_width=True)
    
    st.divider()
    
    # Analiza wybranego stanowiska
    st.markdown('<a id="salary_detail"></a>', unsafe_allow_html=True)
    st.subheader("🔍 Szczegółowa analiza stanowiska")
    
    # 🔽 SELECTBOX Z WSZYSTKIMI STANOWISKAMI
    jobs = sorted(df['job_title'].unique())
    selected_job = st.selectbox("Wybierz stanowisko:", jobs)
    
    # 🎯 FILTROWANIE DANYCH W CZASIE RZECZYWISTYM
    job_df = df[df['job_title'] == selected_job]
    
     # 📊 3 METRYKI W KOLUMNACH
    colA, colB, colC = st.columns(3)
    colA.metric("Średnie", f"{int(job_df['salary_in_usd'].mean()):,} USD")
    colB.metric("Mediana", f"{int(job_df['salary_in_usd'].median()):,} USD")
    colC.metric("Rekordy", job_df.shape[0])
    
    # 📈 WYKRES TRENDU DLA WYBRANEGO STANOWISKA
    trend_data = job_df.groupby('work_year')['salary_in_usd'].mean().reset_index()
    if not trend_data.empty:
        import plotly.express as px
        fig = px.line(
            trend_data,
            x='work_year',
            y='salary_in_usd',
            title=f"Trend wynagrodzeń — {selected_job}",
            markers=True
        )
        st.plotly_chart(fig, use_container_width=True)
    
    st.divider()

def show_geography_analysis(df):
    # 🌍 SEKCJA: Analiza geograficzna
    
    # Pokazuje zaawansowane features:
    # - Mapy choropleth z Plotly
    # - Konwersje kodów krajów (ISO2 → ISO3)
    # - Multipleksy (multiselect)
    # - Porównanie dwóch map obok siebie
    """Analiza geograficzna."""
    st.markdown('<a id="geo_analysis"></a>', unsafe_allow_html=True)
    st.header("🌍 Analiza geograficzna")
    
    # Statystyki krajów
    st.markdown('<a id="geo_global"></a>', unsafe_allow_html=True)
    st.subheader("🌎 Globalne wynagrodzenia według krajów")
    # Tablica krajów z metrykami
    country_stats = (
        df.groupby("company_location")
        .agg(
            mean_salary=("salary_in_usd", "mean"), 
            median_salary=("salary_in_usd", "median"),
            count=("salary_in_usd", "count")
        )
        .reset_index()
        .sort_values("mean_salary", ascending=False)
    )
    st.dataframe(
        country_stats.rename(columns={
            "company_location": "Kraj",
            "mean_salary": "Średnia (USD)",
            "median_salary": "Mediana (USD)",
            "count": "Liczba rekordów"
        }),
        use_container_width=True
    )
    
    # Mapa
    st.markdown('<a id="geo_map"></a>', unsafe_allow_html=True)
    st.subheader("🗺️ Mapa średnich wynagrodzeń")
    fig = create_world_map(df, "company_location")
    st.plotly_chart(fig, use_container_width=True)
    
    # Porównanie krajów
    st.markdown('<a id="geo_compare"></a>', unsafe_allow_html=True)
    st.subheader("📌 Porównanie krajów")
    unique_countries = sorted(df["company_location"].unique())
    selected_countries = st.multiselect(
        "Wybierz kraje do porównania:",
        unique_countries,
        default=["US", "GB", "DE", "PL"] if "US" in unique_countries else unique_countries[:4]
    )
    # Jeśli wybrano kraje, pokaż wykres porównawczy
    if selected_countries:
        fig = create_country_comparison_chart(df, selected_countries)
        st.plotly_chart(fig, use_container_width=True)
    
    # Mapa firmy vs pracownika
    st.subheader("🏙️ Lokalizacja pracownika vs lokalizacja firmy")
    st.markdown("""
    Porównanie map pokazuje różnice między:
    - 🌐 **lokalizacją firmy** 
    - 🧑‍💻 **lokalizacją pracownika**
    """)
    
    fig_company, fig_employee = create_company_vs_employee_maps(df)
    
    # 2-KOLUMNOWY LAYOUT DLA MAP
    colA, colB = st.columns(2)
    colA.plotly_chart(fig_company, use_container_width=True)
    colB.plotly_chart(fig_employee, use_container_width=True)
    
    st.divider()

def show_salary_distribution(df):
    # 📊 SEKCJA: Rozkład wynagrodzeń
    
    # Demonstruje:
    # - Interaktywne filtrowanie danych
    # - Histogram z dynamicznym bins
    # - Statystyki pozycyjne (kwartyle)
    # - Integracja NumPy dla obliczeń
    """Rozkład wynagrodzeń."""
    st.markdown('<a id="salary_distribution"></a>', unsafe_allow_html=True)
    st.header("📊 Rozkład wynagrodzeń")
    
     # 🎚️ SLIDER DO USUWANIA OUTLIERÓW
    # Pokazuje jak filtrować dane w czasie rzeczywistym
    cutoff = st.slider("Usuń górne % wynagrodzeń:", 0, 10, 2)
    
     # 🎯 FILTROWANIE DANYCH Z NUMPY
    # percentile() to czysty NumPy - integracja z ekosystemem Python
    if cutoff > 0:
        threshold = np.percentile(df['salary_in_usd'], 100 - cutoff)
        df_plot = df[df['salary_in_usd'] <= threshold].copy()
    else:
        df_plot = df.copy()
    
     # 📈 HISTOGRAM Z PLOTLY
    # Pokazuje rozkład po filtracji
    fig = create_salary_distribution_chart(df_plot)
    st.plotly_chart(fig, use_container_width=True)
    
    # Statystyki
    st.markdown('<a id="salary_stats"></a>', unsafe_allow_html=True)
    st.subheader("📈 Statystyki rozkładu")
    q1 = int(df_plot['salary_in_usd'].quantile(0.25))
    q3 = int(df_plot['salary_in_usd'].quantile(0.75))
    iqr = q3 - q1
    
    # 3 METRYKI W KOLUMNACH
    col1, col2, col3 = st.columns(3)
    col1.metric("Q1 (25%)", f"{q1:,} USD")
    col2.metric("Q3 (75%)", f"{q3:,} USD")
    col3.metric("IQR", f"{iqr:,} USD")
    
    st.divider()

def show_eda(df):

    # 🚀 GŁÓWNA FUNKCJA EDA - ORCHESTRATOR
    
    # Łączy wszystkie sekcje w jeden dashboard.
    # Demonstruje modularną architekturę Streamlit.
    
    # Uwaga: Kolejność wywołań = kolejność na stronie
    # Streamlit renderuje sekwencyjnie od góry do dołu.
    # 🎪 SEKWENCJA SEKCJI
    # Każda sekcja to osobny "blok" w dashboardzie
    show_intro_section()
    show_dataset_overview(df)
    show_statistics(df)
    show_time_trends(df)
    show_salary_analysis(df)
    show_geography_analysis(df)
    show_salary_distribution(df)