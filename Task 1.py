import requests
import pandas as pd
import matplotlib.pyplot as plt

# Lim inn din Client ID her
client_id = '5f634a81-f21f-48c0-b433-b26eea644b96' 

# Definer endpoint og parametere for 2025
endpoint = 'https://frost.met.no/observations/v0.jsonld'
parameters = {
    'sources': 'SN17850',
    'elements': 'mean(air_temperature P1D)',
    'referencetime': '2025-01-01/2025-12-31',
}

# Send forespørselen
r = requests.get(endpoint, parameters, auth=(client_id, ''))
json = r.json()

if r.status_code == 200:
    data = json['data']
    print('Data hentet fra frost.met.no!')
    
    # Legg dataene inn i en Pandas DataFrame
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
    
    # --- 1. SKRIV UT OPPSUMMERINGSTABELL FØRST ---
    summary_data = {
        'Mean': [df['value'].mean()],
        'Median': [df['value'].median()],
        'Min': [df['value'].min()],
        'Max': [df['value'].max()]
    }
    
    summary_table = pd.DataFrame(summary_data)
    print("\n--- Oppsummeringstabell for temperatur i Ås (2025) ---")
    print(summary_table.to_string(index=False))

    # --- 2. VIS PLOTTET TIL SLUTT ---
    plt.figure(figsize=(12, 6))
    plt.plot(df['referenceTime'], df['value'], color='blue', label='Daglig snittemperatur')
    
    plt.title('Daglig gjennomsnittstemperatur i Ås (2025)', fontsize=16)
    plt.xlabel('Tid', fontsize=12)
    plt.ylabel('Temperatur (°C)', fontsize=12)
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.legend()
    plt.tight_layout()
    
    plt.show()

else:
    print('Error! Returned status code %s' % r.status_code)
    print('Message: %s' % json['error']['message'])
    print('Reason: %s' % json['error']['reason'])