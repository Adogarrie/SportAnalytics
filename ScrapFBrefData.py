import pandas as pd
import requests

def get_html(url: str) -> str:
    """Descarga el HTML de la página y elimina los comentarios HTML."""
    response = requests.get(url)
    html = response.text.replace('<!--', '').replace('-->', '')
    return html

def extract_table(html: str, table_id: str) -> pd.DataFrame:
    """Extrae una tabla por ID del HTML."""
    return pd.read_html(html, attrs={'id': table_id}, index_col=0)[0]

def scrape_fbref_tables(url: str, table_ids: list[str], save_csv: bool = False) -> dict:
    """Extrae múltiples tablas de FBref por sus IDs y devuelve un diccionario de DataFrames."""
    html = get_html(url)
    tables = {}
    for table_id in table_ids:
        try:
            df = extract_table(html, table_id)
            tables[table_id] = df
            print(f"[✓] Tabla '{table_id}' extraída. Filas: {len(df)}")
            if save_csv:
                df.to_csv(f"{table_id}.csv")
        except Exception as e:
            print(f"[✗] Error con tabla '{table_id}': {e}")
    return tables

if __name__ == "__main__":
    # URL de ejemplo — reemplaza con la que estás usando
    fbref_url = "https://fbref.com/en/comps/Big5/stats/players/Big-5-European-Leagues-Stats"
    
    # Lista de IDs de tablas que deseas extraer — personaliza según tus necesidades
    table_list = ["stats_standard", "stats_misc", "stats_possession", "stats_shooting", "stats_passing", 
                  "stats_gca", "stats_defense"]


    # Ejecutar extracción
    scrape_fbref_tables(fbref_url, table_list, save_csv=True)
