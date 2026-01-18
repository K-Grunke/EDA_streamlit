
# 🧪 MODUŁ: Testy jednostkowe

# Cel: Testowanie funkcji ładowania danych z pliku CSV

# Uruchomienie: pytest tests/ -v


import pytest
import pandas as pd
import sys
import os

# Dodanie ścieżki do src
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from data_loader import load_data

def test_load_data_returns_dataframe():
    """Test czy funkcja load_data zwraca DataFrame."""
    # Zakładając, że testy są uruchamiane z głównego katalogu projektu
    test_data_path = "data/DataScience_salaries_2025.csv"
    
    try:
        df = load_data(test_data_path)
        assert isinstance(df, pd.DataFrame), "Funkcja powinna zwracać DataFrame"
        assert not df.empty, "DataFrame nie powinien być pusty"
    except FileNotFoundError:
        pytest.skip(f"Plik {test_data_path} nie istnieje")

def test_load_data_columns_exist():
    """Test czy wczytane dane mają oczekiwane kolumny."""
    test_data_path = "data/DataScience_salaries_2025.csv"
    
    try:
        df = load_data(test_data_path)
        expected_columns = [
            'work_year', 'experience_level', 'employment_type', 
            'job_title', 'salary', 'salary_currency', 'salary_in_usd',
            'employee_residence', 'remote_ratio', 'company_location', 
            'company_size'
        ]
        
        for col in expected_columns:
            assert col in df.columns, f"Brak kolumny: {col}"
    except FileNotFoundError:
        pytest.skip(f"Plik {test_data_path} nie istnieje")

def test_load_data_types():
    """Test czy kolumny mają poprawne typy."""
    test_data_path = "data/DataScience_salaries_2025.csv"
    
    try:
        df = load_data(test_data_path)
        assert df['salary_in_usd'].dtype == float, "salary_in_usd powinno być float"
        assert df['work_year'].dtype == int, "work_year powinno być int"
    except FileNotFoundError:
        pytest.skip(f"Plik {test_data_path} nie istnieje")