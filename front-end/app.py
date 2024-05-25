import requests
from flask import Flask, render_template, request, flash, redirect, url_for, jsonify
from flask_bootstrap import Bootstrap
from functools import wraps
from flask import session
import json

app = Flask(__name__)
bootstrap = Bootstrap(app)
app.secret_key = 'secret_key'  # Defina uma chave secreta para o Flash

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in to access this page.', 'error')
            return render_template('login.html')
        return f(*args, **kwargs)
    return decorated_function

@app.route('/logout')
def logout():
    session.pop('user_id', None)  # Remove o usuário da sessão
    flash('Logout realizado com sucesso!', 'success')
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        url = 'http://127.0.0.1:8000/login/'

        headers = {'Content-Type': 'application/json'}

        data = {'login': username, 'senha': password}

        response = requests.post(url, json=data, headers=headers)

        if response.status_code == 200:
            try:
                user_id = response.json().get('id')
                if user_id:
                    session['user_id'] = user_id
                    flash('Login realizado com sucesso!', 'success')
                    return redirect(url_for('index'))
                else:
                    flash('Usuário ou senha inválidos!', 'error')
            except json.decoder.JSONDecodeError:
                flash('Erro ao decodificar a resposta do servidor.', 'error')
        else:
            flash('Erro no login', 'error')

    return render_template('login.html')

# Rota para a página inicial
@app.route('/')
@login_required
def index():
    # Lista de atividades
    request = requests.get('http://127.0.0.1:8000/atividades/')
    atividades = request.json()
    atividades = atividades['atividades']

    print(atividades)

    return render_template('index.html', atividades=atividades, user_id=session['user_id'])

# Rota para a página de resposta das questões
@app.route('/responder_questoes', methods=['GET', 'POST'])
@login_required
def responder_questoes():
    if request.method == 'POST':
        if 'resposta_questao' in request.files:
            resposta = request.files['resposta_questao']
            # Aqui você pode fazer o processamento necessário com a resposta
            # Por exemplo, salvar o arquivo, extrair dados, etc.
            flash('Resposta enviada com sucesso!', 'success')  # Flash de sucesso
            return redirect(url_for('resultado'))
        else:
            flash('Nenhum arquivo enviado!', 'error')  # Flash de erro
    
    # Certifique-se de definir user_id, atividade_id e questoes aqui
    user_id = session.get('user_id')  # Usamos .get() para evitar erros se 'user_id' não estiver na sessão
    atividade_id = request.args.get('atividade_id')  # Obtemos atividade_id dos argumentos da requisição
    questoes = request.args.get('questao_id')  # Obtemos questoes dos argumentos da requisição

    return render_template('responder_questoes.html', user_id=user_id, atividade_id=atividade_id, questao_id=questoes)

# Rota para a página de resultado (pontuação total do grupo)
@app.route('/resultado')
@login_required
def resultado():
    # Aqui você pode calcular a pontuação total do grupo e passar para o template
    # Neste exemplo, retornamos uma pontuação de exemplo
    pontuacao_total = 85
    return render_template('resultado.html', pontuacao_total=pontuacao_total)

# Rota para processar as respostas enviadas pelo formulário
@app.route('/processar_respostas', methods=['POST'])
@login_required
def processar_respostas():
    if request.method == 'POST':
        # Obtemos os dados enviados pelo formulário
        user_id = session.get('user_id')  # Usamos .get() para evitar erros se 'user_id' não estiver na sessão
        atividade_id = request.form.get('atividade_id')  # Obtemos atividade_id do formulário
        questao_id = request.form.get('questao_id')  # Obtemos questao_id do formulário
        resposta_questao = request.form.get('resposta_questao')  # Obtemos a resposta enviada pelo formulário

        print(user_id)
        print(atividade_id)
        print(questao_id)
        print(resposta_questao)

        # Construímos o payload para a requisição POST
        payload = {
            'aluno_id': user_id,
            'atividade_id': atividade_id,
            'questao_id': questao_id,
            'resposta': resposta_questao
        }

        try:
            response = requests.post('http://127.0.0.1:8000/resposta/', json=payload)
            response.raise_for_status()  # Levanta uma exceção para códigos de status HTTP 4xx/5xx
            flash('Respostas enviadas com sucesso!', 'success')
            return redirect(url_for('index'))
        except requests.exceptions.RequestException as e:
            flash(f'Erro ao enviar respostas: {str(e)}', 'error')
            try:
                response = requests.get('http://127.0.0.1:8000/atividades/')
                response.raise_for_status()
                atividades = response.json().get('atividades', [])
            except requests.exceptions.RequestException as e:
                atividades = []
                flash(f'Erro ao carregar atividades: {str(e)}', 'error')
            return render_template('index.html', atividades=atividades, user_id=session['user_id'])

@app.route('/criar_atividade', methods=['GET', 'POST'])
@login_required
def criar_atividade():
    if request.method == 'POST':
        titulo = request.form['titulo']
        descricao = request.form['descricao']
        nome_questao = request.form.getlist('nome_questao')
        gabarito_questao = request.form.getlist('gabarito_questao')
        enunciado_questao = request.form.getlist('enunciado_questao')
        pontuacao_questao = request.form.getlist('pontuacao_questao')

        print(request.form)

        # Cria nova atividade com as questões
        nova_atividade = {
            'titulo': titulo,
            'descricao': descricao,
            'questoes': [
                {
                    'id': i + 1,
                    'nome': nome_questao[i],
                    'gabarito': gabarito_questao[i],
                    'enunciado': enunciado_questao[i],
                    'pontuacao': pontuacao_questao[i]
                } for i in range(len(nome_questao))
            ]
        }

        # Adiciona a nova atividade à lista de atividades
        atividades.append(nova_atividade)
        flash('Atividade criada com sucesso!', 'success')
        return redirect(url_for('index'))
    
    return render_template('criar_atividade.html')


if __name__ == '__main__':
    app.run(debug=True)
