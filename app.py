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

@app.get('/v1/<int:start_date>/<int:end_date>')
def index(start_date, end_date):
    return {
        "start_date": start_date,
        "end_date": end_date
    }