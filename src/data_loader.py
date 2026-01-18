import pandas as pd

def load_data(path: str):
    # Wczytuje plik CSV i konwertuje kolumny do odpowiednich typów.
    
    df = pd.read_csv(path)

    # Upewnij się, że salary_in_usd jest float
    df['salary_in_usd'] = df['salary_in_usd'].astype(float)
    
    # work_year jako int
    df['work_year'] = df['work_year'].astype(int)
    
    return df