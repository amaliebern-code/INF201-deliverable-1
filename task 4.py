import requests
import pandas as pd
import yaml

# Lim inn din Client ID her
CLIENT_ID = '5f634a81-f21f-48c0-b433-b26eea644b96'

def count_heatwaves(station_id, year, client_id, yml_filename=None):
    """
    Teller antall hetebølger (>= 5 dager på rad med maks temp >= 27 °C)
    for en stasjon og et år, og lagrer sammendraget i en .yml-fil.
    """
    if yml_filename is None:
        yml_filename = f"heatwaves_{station_id}_{year}.yml"
        
    endpoint = 'https://frost.met.no/observations/v0.jsonld'
    parameters = {
        'sources': station_id,
        'elements': 'max(air_temperature P1D)',
        'referencetime': f'{year}-01-01/{year}-12-31',
    }
    
    # Hent data fra Frost
    r = requests.get(endpoint, parameters, auth=(client_id, ''))
    json_data = r.json()
    
    if r.status_code != 200:
        print(f"Feil ved henting av data for {station_id} ({year}): Status {r.status_code}")
        print(json_data.get('error', {}).get('message', ''))
        return None
        
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
    
    # Algoritme for å telle hetebølger
    current_streak = 0
    heatwave_count = 0
    
    for temp in df['value']:
        if temp >= 27:
            current_streak += 1
        else:
            if current_streak >= 5:
                heatwave_count += 1
            current_streak = 0
            
    # Sjekk om en hetebølge varte helt ut årets siste dag
    if current_streak >= 5:
        heatwave_count += 1
        
    # Lagre sammendraget i en ordbok (dict)
    summary = {
        'station_id': station_id,
        'year': int(year),
        'element': 'max(air_temperature P1D)',
        'heatwave_threshold_temp_celsius': 27,
        'min_consecutive_days': 5,
        'number_of_heatwaves': heatwave_count
    }
    
    # Skriv til .yml-fil
    with open(yml_filename, 'w', encoding='utf-8') as f:
        yaml.dump(summary, f, default_flow_style=False, sort_keys=False)
        
    print(f"--- Resultat for stasjon {station_id} ({year}) ---")
    print(f"Antall hetebølger funnet: {heatwave_count}")
    print(f"Sammendrag lagret i filen: {yml_filename}\n")
    
    return heatwave_count


# --- Kjøring for Ås stasjon (SN17850) i 2025 ---
count_heatwaves(station_id='SN17850', year=2025, client_id=CLIENT_ID)