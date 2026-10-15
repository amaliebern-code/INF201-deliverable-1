import requests
import pandas as pd
import matplotlib.pyplot as plt

# Lim inn din Client ID her
client_id = '5f634a81-f21f-48c0-b433-b26eea644b96'

# 1. Funksjon som beregner 7-dagers glidende gjennomsnitt
def calculate_moving_average(series, window=7):
    """
    Beregner glidende gjennomsnitt for en Pandas Series over valgt vindulengde.
    """
    return series.rolling(window=window).mean()

# 2. Hent gjennomsnittstemperatur for 2025 (fra Task 1)
endpoint = 'https://frost.met.no/observations/v0.jsonld'
parameters = {
    'sources': 'SN17850',
    'elements': 'mean(air_temperature P1D)',
    'referencetime': '2025-01-01/2025-12-31',
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
    df = df.sort_values('referenceTime')
    
    # Bruk funksjonen til å beregne 7-dagers glidende gjennomsnitt
    df['moving_avg'] = calculate_moving_average(df['value'], window=7)
    
    # 3. Plott daglig temperatur som punkter og glidende gjennomsnitt som linje
    plt.figure(figsize=(12, 6))
    
    # Daglig temperatur skrives ut som punkter (scatter)
    plt.scatter(
        df['referenceTime'], 
        df['value'], 
        color='skyblue', 
        alpha=0.7, 
        s=15, 
        label='Daglig gjennomsnittstemperatur'
    )
    
    # Glidende gjennomsnitt skrives ut som linje
    plt.plot(
        df['referenceTime'], 
        df['moving_avg'], 
        color='darkblue', 
        linewidth=2, 
        label='7-dagers glidende gjennomsnitt'
    )
    
    plt.title('Daglig temperatur og 7-dagers glidende gjennomsnitt i Ås (2025)', fontsize=14)
    plt.xlabel('Tid', fontsize=12)
    plt.ylabel('Temperatur (°C)', fontsize=12)
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.legend()
    plt.tight_layout()
    
    plt.show()

else:
    print(f'Error! Returned status code {r.status_code}')
    