from flask import Flask
import pandas as pd

frota = pd.read_csv('simu-frota-mun_T.csv')
carteira = pd.read_csv('simu-carteira-mun_T.csv')
acidentes = pd.read_csv('simu-acidentes-mun_T.csv')

app = Flask(__name__)

@app.get('/')
def health_check() -> str:
    """
    This function is a health check endpoint for the API.
    It returns a simple string message to indicate that the API is running.

    :return: str - "Api is running"
    """
    return "Api is running"


# Essa função tem que retornar o indice de variação dos acidentes de trânsito por ano
@app.get('/v1/<int:start_date>/<int:end_date>')
def index(start_date, end_date):
    
    # Obtem a porcentagem da frota de transporte coletivo das cidades
    filtered_frota = frota[(frota['ano'] >= start_date) & (frota['ano'] <= end_date)][['Município', 'ano', 'TOTAL_VEICULOS', 'BONDE', 'MICRO-ONIBUS', 'ONIBUS']]
    filtered_frota['porcentagem_transporte_coletivo'] = 100 * (filtered_frota['BONDE'] + filtered_frota['MICRO-ONIBUS'] + filtered_frota['ONIBUS']) / filtered_frota['TOTAL_VEICULOS']
    filtered_frota = filtered_frota.groupby(['Município', 'ano']).agg({'porcentagem': 'mean'}).reset_index()
    
    # Obtem a quantidade de acidentes por 100 mil habitantes das cidades
    filtered_acidentes = acidentes[(acidentes['ano'] >= start_date) & (acidentes['ano'] <= end_date)][['Município', 'ano', 'taxa_mun_mortes', 'taxa_mun_feridos']]
    filtered_acidentes['acidentes_por_cem_mil'] = (filtered_acidentes['taxa_mun_mortes'] + filtered_acidentes['taxa_mun_feridos'])
    filtered_acidentes = filtered_acidentes.groupby(['Município', 'ano']).agg({'acidentes_por_mil': 'sum'}).reset_index()
    
    # Junta as duas informações em um único DataFrame
    result = pd.merge(filtered_frota, filtered_acidentes, on=['Município', 'ano'], how='inner')
    
    # Converter o DataFrame resultante para JSON
    result = result.to_json(orient='records')
    
    # Retorna o resultado como resposta JSON
    return result