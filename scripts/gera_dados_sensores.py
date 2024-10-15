import csv
import os
from datetime import datetime, timedelta
import random

# Definindo as áreas e sensores
areas = [1, 2, 3]  # Exemplo de 3 áreas
sensor_umidade = 1  # S1 - Umidade do Solo
sensor_ph = 2       # S2 - Alcalinidade (PH)
sensor_npk = 3      # S3 - Nutrientes (Nitrogênio, Fósforo e Potássio)

# Funções para gerar valores simulados para cada tipo de sensor
def gerar_valor_umidade():
    return round(random.uniform(10, 80), 2)  # Umidade (%)

def gerar_valor_ph():
    return round(random.uniform(4.0, 9.0), 2)  # Alcalinidade (PH)

def gerar_valor_nutriente(nutriente):
    ranges = {
        'N': (50, 300),  # Nitrogênio
        'P': (20, 200),  # Fósforo
        'K': (40, 250),  # Potássio
    }
    return round(random.uniform(*ranges[nutriente]), 2)

# Gerando o CSV com 10 leituras para cada tipo de sensor
script_dir = os.path.dirname(os.path.abspath(__file__))
csv_output_file = os.path.join(script_dir, 'dados_sensores.csv')

with open(csv_output_file, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['id_area', 'id_sensor', 'dt_leitura', 'valor', 'tipo_valor'])  # Cabeçalhos

    now = datetime.now()

    for area in areas:
        for i in range(10):
            # Gerar leituras para umidade (S1)
            dt_leitura = now - timedelta(hours=i)
            valor_umidade = gerar_valor_umidade()
            writer.writerow([area, sensor_umidade, dt_leitura.strftime('%Y-%m-%d %H:%M'), valor_umidade, "umidade"])

            # Gerar leituras para PH (S2)
            valor_ph = gerar_valor_ph()
            writer.writerow([area, sensor_ph, dt_leitura.strftime('%Y-%m-%d %H:%M'), valor_ph, "ph"])

            # Gerar leituras para Nitrogênio (N), Fósforo (P), Potássio (K) (S3 - NPK)
            valor_n = gerar_valor_nutriente('N')
            valor_p = gerar_valor_nutriente('P')
            valor_k = gerar_valor_nutriente('K')

            writer.writerow([area, sensor_npk, dt_leitura.strftime('%Y-%m-%d %H:%M'), valor_n, "nitrogenio"])
            writer.writerow([area, sensor_npk, dt_leitura.strftime('%Y-%m-%d %H:%M'), valor_p, "fosforo"])
            writer.writerow([area, sensor_npk, dt_leitura.strftime('%Y-%m-%d %H:%M'), valor_k, "potassio"])
