import requests
import pandas as pd
import matplotlib.pyplot as plt

client_id = '5f634a81-f21f-48c0-b433-b26eea644b96' 

endpoint = 'https://frost.met.no/observations/v0.jsonld'

# Hjelpefunksjon for å hente temperaturdata for et gitt år
def hent_temperatur_data(aar):
    parameters = {
        'sources': 'SN17850',
        'elements': 'mean(air_temperature P1D)',
        'referencetime': f'{aar}-01-01/{aar}-12-31',
    }
    r = requests.get(endpoint, parameters, auth=(client_id, ''))
    json_data = r.json()
    
    if r.status_code == 200:
        data = json_data['data']
        rows = []
        for item in data:
            ref_time = item['referenceTime']
            for obs in item['observations']:
                rows.append({
                    'referenceTime': ref_time,
                    'value': obs['value']
                })
        df = pd.DataFrame(rows)
        df['referenceTime'] = pd.to_datetime(df['referenceTime'])
        # Finn dag i året (1-365) slik at vi kan overlappe årene i plottet
        df['day_of_year'] = df['referenceTime'].dt.dayofyear
        return df
    else:
        print(f'Feil ved henting av data for {aar}: Status {r.status_code}')
        return None

# Henter data for både 1925 og 2025
df_1925 = hent_temperatur_data(1925)
df_2025 = hent_temperatur_data(2025)

if df_1925 is not None and df_2025 is not None:
   # --- 1. Lag og skriv ut oppsummeringstabell FØRST ---
    summary_data = {
        'År': ['1925', '2025'],
        'Mean': [df_1925['value'].mean(), df_2025['value'].mean()],
        'Median': [df_1925['value'].median(), df_2025['value'].median()],
        'Min': [df_1925['value'].min(), df_2025['value'].min()],
        'Max': [df_1925['value'].max(), df_2025['value'].max()]
    }
    
    summary_table = pd.DataFrame(summary_data)
    print("\n--- Oppsummeringstabell: 1925 vs 2025 ---")
    print(summary_table.to_string(index=False))

    # --- 2. Vis plottet TIL SLUTT ---
    plt.figure(figsize=(12, 6))
    
    plt.plot(df_1925['day_of_year'], df_1925['value'], label='1925 (100 år siden)', color='navy', alpha=0.75, linewidth=1.2)
    plt.plot(df_2025['day_of_year'], df_2025['value'], label='2025', color='firebrick', alpha=0.85, linewidth=1.2)
    
    plt.title('Temperatursammenligning i Ås: 1925 vs. 2025', fontsize=14)
    plt.xlabel('Dag i året (1–365)', fontsize=12)
    plt.ylabel('Temperatur (°C)', fontsize=12)
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.legend()
    plt.tight_layout()
    
    plt.show()