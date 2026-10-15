import requests
import pandas as pd
import matplotlib.pyplot as plt

# Lim inn din Client ID her
client_id = '5f634a81-f21f-48c0-b433-b26eea644b96'

endpoint = 'https://frost.met.no/observations/v0.jsonld'
parameters = {
    'sources': 'SN17850',
    'elements': 'mean(air_temperature P1D),sum(precipitation_amount P1D)',
    'referencetime': '2025-01-01/2025-12-31',
}

r = requests.get(endpoint, parameters, auth=(client_id, ''))
json = r.json()

if r.status_code == 200:
    data = json['data']
    
    rows = []
    for item in data:
        ref_time = item['referenceTime']
        for obs in item['observations']:
            rows.append({
                'referenceTime': ref_time,
                'elementId': obs['elementId'],
                'value': obs['value']
            })
    
    df = pd.DataFrame(rows)
    df['referenceTime'] = pd.to_datetime(df['referenceTime'])
    
    df_temp = df[df['elementId'] == 'mean(air_temperature P1D)']
    df_precip = df[df['elementId'] == 'sum(precipitation_amount P1D)']
    
    # --- 1. SKRIV UT MELDING I TERMINALEN FØRST ---
    print("Data for temperatur og nedbør hentet fra frost.met.no!")
    print(f"Antall temperaturmålinger: {len(df_temp)}")
    print(f"Antall nedbørsmålinger: {len(df_precip)}")

    # --- 2. VIS PLOTTET TIL SLUTT ---
    fig, ax1 = plt.subplots(figsize=(12, 6))

    color_temp = 'tab:red'
    ax1.set_xlabel('Tid', fontsize=12)
    ax1.set_ylabel('Temperatur (°C)', color=color_temp, fontsize=12)
    ax1.plot(df_temp['referenceTime'], df_temp['value'], color=color_temp, linewidth=1.5, label='Temperatur')
    ax1.tick_params(axis='y', labelcolor=color_temp)

    ax2 = ax1.twinx()  
    color_precip = 'tab:blue'
    ax2.set_ylabel('Nedbør per døgn (mm)', color=color_precip, fontsize=12)
    ax2.bar(df_precip['referenceTime'], df_precip['value'], color=color_precip, alpha=0.5, width=1.0, label='Nedbør')
    ax2.tick_params(axis='y', labelcolor=color_precip)

    plt.title('Daglig temperatur og nedbør i Ås (2025)', fontsize=14)
    fig.tight_layout()
    
    plt.show()

else:
    print('Error! Returned status code %s' % r.status_code)
    print('Message: %s' % json['error']['message'])
    print('Reason: %s' % json['error']['reason'])