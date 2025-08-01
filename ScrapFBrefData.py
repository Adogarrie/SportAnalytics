import pandas as pd
import requests
from io import StringIO

def get_html(url: str) -> str:
    """Descarga el HTML de la página y elimina los comentarios HTML."""
    response = requests.get(url)
    html = response.text.replace('<!--', '').replace('-->', '')
    return html

def extract_table(html: str, table_id: str) -> pd.DataFrame:
    """Extrae una tabla por ID del HTML."""
    return pd.read_html(StringIO(html), attrs={'id': table_id}, index_col=0)[0]

def scrape_fbref_tables(table_url_dict: dict[str, str], save_csv: bool = False) -> dict:
    """
    Extrae múltiples tablas de FBref por sus IDs y URLs y devuelve un diccionario de DataFrames.
    table_url_dict: dict donde la clave es el table_id y el valor es la URL correspondiente.
    """
    tables = {}
    for table_id, url in table_url_dict.items():
        try:
            html = get_html(url)
            df = extract_table(html, table_id)
            tables[table_id] = df
            print(f"[✓] Tabla '{table_id}' extraída de {url}. Filas: {len(df)}")
            if save_csv:
                df.to_csv(f"datasets/{table_id}.csv")
        except Exception as e:
            print(f"[✗] Error con tabla '{table_id}': {e}")
    return tables

if __name__ == "__main__":
    # Diccionario de IDs de tablas y sus URLs correspondientes
    table_url_dict = {
        "stats_standard": "https://fbref.com/en/comps/Big5/stats/players/Big-5-European-Leagues-Stats",
        "stats_misc": "https://fbref.com/en/comps/Big5/misc/players/Big-5-European-Leagues-Stats",
        "stats_possession": "https://fbref.com/en/comps/Big5/possession/players/Big-5-European-Leagues-Stats",
        "stats_shooting": "https://fbref.com/en/comps/Big5/shooting/players/Big-5-European-Leagues-Stats",
        "stats_passing": "https://fbref.com/en/comps/Big5/passing/players/Big-5-European-Leagues-Stats",
        "stats_gca": "https://fbref.com/en/comps/Big5/gca/players/Big-5-European-Leagues-Stats",
        "stats_defense": "https://fbref.com/en/comps/Big5/defense/players/Big-5-European-Leagues-Stats",
        "compare_keeper": "https://fbref.com/en/comps/Big5/keepers/players/Big-5-European-Leagues-Stats",           
        "compare_keeper_adv": "https://fbref.com/en/comps/Big5/keepersadv/players/Big-5-European-Leagues-Stats",         
        "compare_passing_types": "https://fbref.com/en/comps/Big5/passing_types/players/Big-5-European-Leagues-Stats",   
        "stats_playing_time": "https://fbref.com/en/comps/Big5/playingtime/players/Big-5-European-Leagues-Stats"       
    }

    # Ejecutar extracción
    scrape_fbref_tables(table_url_dict, save_csv=True)