from flask import Flask, render_template, redirect, url_for, request, session
from sensores import get_current, get_voltage, get_temperature, get_acceleration  # Importa as funções do sensores.py

app = Flask(__name__)
app.secret_key = "supersecretkey"

users = {}

corridas_anteriores = [
    {"id": 1, "forno": "Forno 1", "data": "2024-10-10", "status": "Concluída"},
    {"id": 2, "forno": "Forno 2", "data": "2024-10-09", "status": "Concluída"},
    {"id": 3, "forno": "Forno 3", "data": "2024-10-08", "status": "Cancelada"},
]

fornos_disponiveis = ["Forno 1", "Forno 2", "Forno 3"]

@app.route("/", methods=['GET'])
def home():
    return render_template("home.html")

@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if username in users and users[username]['password'] == password:
            session['user'] = username
            return redirect(url_for('nova_corrida'))
        else:
            return render_template('login.html', error="Usuário ou senha inválidos.")

    return render_template('login.html')

@app.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        forno = request.form['forno']
        
        if username in users:
            return render_template('register.html', fornos=fornos_disponiveis, error="Usuário já existe.")
        
        users[username] = {'password': password, 'forno': forno}
        session['user'] = username
        return redirect(url_for('nova_corrida'))
    
    return render_template('register.html', fornos=fornos_disponiveis)

@app.route("/nova-corrida")
def nova_corrida():
    if 'user' not in session:
        return redirect(url_for('login'))
    
    user = session['user']
    forno = users[user]['forno']

    # Coleta os dados dos sensores
    current = get_current()         
    voltage = get_voltage()         
    temperature = get_temperature() 
    acceleration = get_acceleration()['x']  

    return render_template(
        "nova_corrida.html", 
        user=user, 
        forno=forno, 
        current=current, 
        voltage=voltage, 
        temperature=temperature, 
        acceleration=acceleration
    )

@app.route("/corridas-anteriores")
def corridas_anteriores_view():
    return render_template("corridas_anteriores.html", corridas=corridas_anteriores)

@app.route("/logout")
def logout():
    session.pop('user', None)
    return redirect(url_for('home'))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
