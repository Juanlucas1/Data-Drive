import pandas as pd

def load_data(file_path):
    """Carrega os dados de um arquivo CSV e retorna um DataFrame."""
    try:
        data = pd.read_csv(file_path)
        return data
    except Exception as e:
        print(f"Erro ao carregar dados: {e}")
        return None

def process_data(df):
    """Realiza algum processamento nos dados e retorna os resultados."""
    # Exemplo: calcular média de uma coluna
    if df is not None:
        return df.describe()  # Retorna uma descrição estatística básica
    return None
