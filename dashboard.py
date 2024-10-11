import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import numpy as np
import matplotlib.pyplot as plt
from sensores import get_current, get_voltage, get_temperature, get_acceleration
import random
import time

# Inicializa a aplicação Dash
app = dash.Dash(__name__)

# Layout do Dashboard
app.layout = html.Div(
    children=[
        html.H1("Dashboard de Sensores - Tempo Real", style={'textAlign': 'center'}),

        # Exibe os dados dos sensores em tempo real
        html.Div(id='sensor-data', style={'textAlign': 'center'}),

        # Gráfico de corrente
        dcc.Graph(id='current-graph'),

        # Gráfico de voltagem
        dcc.Graph(id='voltage-graph'),

        # Gráfico de temperatura
        dcc.Graph(id='temperature-graph'),

        # Gráfico de aceleração
        dcc.Graph(id='acceleration-graph'),

        # Atualização automática a cada 1 segundo
        dcc.Interval(
            id='interval-component',
            interval=1*1000,  # em milissegundos (1 segundo)
            n_intervals=0
        )
    ]
)

# Função para ler dados e printar no dashboard
@app.callback(
    Output('sensor-data', 'children'),
    Input('interval-component', 'n_intervals')
)
def update_sensor_data(n):
    # Leitura dos sensores
    current = get_current()
    voltage = get_voltage()
    temperature = get_temperature()
    acceleration = get_acceleration()

    # Formatação dos dados em texto
    return [
        html.H3(f"Corrente: {current} A"),
        html.H3(f"Voltagem: {voltage} V"),
        html.H3(f"Temperatura: {temperature} °C"),
        html.H3(f"Aceleração (X): {acceleration['x']} m/s²"),
        html.H3(f"Aceleração (Y): {acceleration['y']} m/s²"),
        html.H3(f"Aceleração (Z): {acceleration['z']} m/s²"),
    ]

# Função para atualizar o gráfico de corrente
@app.callback(
    Output('current-graph', 'figure'),
    Input('interval-component', 'n_intervals')
)
def update_current_graph(n):
    current_values = [get_current() for _ in range(10)]
    time_values = list(range(1, 11))
    
    return {
        'data': [go.Scatter(x=time_values, y=current_values, mode='lines', name='Corrente')],
        'layout': go.Layout(title='Corrente em Tempo Real', xaxis={'title': 'Tempo (s)'}, yaxis={'title': 'Corrente (A)'})
    }

# Função para atualizar o gráfico de voltagem
@app.callback(
    Output('voltage-graph', 'figure'),
    Input('interval-component', 'n_intervals')
)
def update_voltage_graph(n):
    voltage_values = [get_voltage() for _ in range(10)]
    time_values = list(range(1, 11))

    return {
        'data': [go.Scatter(x=time_values, y=voltage_values, mode='lines', name='Voltagem')],
        'layout': go.Layout(title='Voltagem em Tempo Real', xaxis={'title': 'Tempo (s)'}, yaxis={'title': 'Voltagem (V)'})
    }

# Função para atualizar o gráfico de temperatura
@app.callback(
    Output('temperature-graph', 'figure'),
    Input('interval-component', 'n_intervals')
)
def update_temperature_graph(n):
    temperature_values = [get_temperature() for _ in range(10)]
    time_values = list(range(1, 11))

    return {
        'data': [go.Scatter(x=time_values, y=temperature_values, mode='lines', name='Temperatura')],
        'layout': go.Layout(title='Temperatura em Tempo Real', xaxis={'title': 'Tempo (s)'}, yaxis={'title': 'Temperatura (°C)'})
    }

# Função para atualizar o gráfico de aceleração
@app.callback(
    Output('acceleration-graph', 'figure'),
    Input('interval-component', 'n_intervals')
)
def update_acceleration_graph(n):
    accel_x = [get_acceleration()['x'] for _ in range(10)]
    accel_y = [get_acceleration()['y'] for _ in range(10)]
    accel_z = [get_acceleration()['z'] for _ in range(10)]
    time_values = list(range(1, 11))

    return {
        'data': [
            go.Scatter(x=time_values, y=accel_x, mode='lines', name='Aceleração X'),
            go.Scatter(x=time_values, y=accel_y, mode='lines', name='Aceleração Y'),
            go.Scatter(x=time_values, y=accel_z, mode='lines', name='Aceleração Z')
        ],
        'layout': go.Layout(title='Aceleração em Tempo Real', xaxis={'title': 'Tempo (s)'}, yaxis={'title': 'Aceleração (m/s²)'})
    }

# Inicia o servidor do Dash
if __name__ == "__main__":
    app.run_server(debug=True)
