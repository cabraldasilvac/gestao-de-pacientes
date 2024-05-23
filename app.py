import sqlite3

from flask import Flask, redirect, render_template, request, url_for

app = Flask(__name__)

# Connection to database
conn = sqlite3.connect('gestao_hospitalar.db')
cursor = conn.cursor()

#Create table if it doesn't exist
cursor.execute(''' 
               CREATE TABLE IF NOT EXISTS pacientes(
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   nome TEXT NOT NULL,
                   idade INTEGER,
                   sexo TEXT,
                   cpf TEXT UNIQUE,
                   endereco TEXT,
                   telefone TEXT
               )
            ''')

conn.commit() #save
conn.close() #close

#Create route and query in the Database
@app.route('/')
def index():
    conn = sqlite3.connect('gestao_hospitalar.db')
    cursor.execute('SELECT * FROM pacientes')
    pacientes = cursor.fetchall()
    conn.close()
    return render_template('index.html', pacientes=pacientes)

#Create route novo_paciente and methods
@app.route('/novo_paciente', methods=['GET', 'POST'])
def novo_paciente():
    if request.method == 'POST':
        nome = request.form['nome']
        idade = request.form['idade']
        sexo = request.form['sexo']
        cpf = request.form['cpf']
        endereco = request.form['endereco']
        telefone = request.form['telefone']
        #enter the database
        conn = sqlite3.connect('gestao_hospitalar.db')
        cursor = conn.cursor()
        #synchronizes information with the database
        cursor.execute('''
            INSERT INTO pacientes(nome, idade, sexo, cpf, endereco, telefone)
            VALUES(?, ?, ?, ?, ?, ?)        
            ''', (nome, idade, sexo, cpf, endereco, telefone))
        conn.commit()
        conn.close()
        return redirect(url_for('index.html'))
    return render_template('novo_paciente.html')

