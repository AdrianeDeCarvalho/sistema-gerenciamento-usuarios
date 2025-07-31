from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import os # Importante para gerenciar caminhos de arquivo

app = Flask(__name__)

# Configurações do SQLAlchemy para o banco de dados SQLite
# Define o caminho base do diretório atual do arquivo (sistema_usuarios_v2)
basedir = os.path.abspath(os.path.dirname(__file__))

# Configura o URI (Uniform Resource Identifier) do banco de dados
# 'sqlite:///' indica que é um banco de dados SQLite baseado em arquivo
# os.path.join(basedir, 'site.db') constrói o caminho completo para o arquivo 'site.db'
# Este arquivo será criado no mesmo diretório do seu 'app.py'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'site.db')

# Desabilita o rastreamento de modificações de objetos SQLAlchemy para economizar memória.
# É recomendado desabilitar isso a menos que você precise explicitamente.
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Cria uma instância do SQLAlchemy, vinculando-o ao aplicativo Flask
# 'db' será usado para definir modelos e interagir com o banco de dados
db = SQLAlchemy(app)

# Definição do Modelo de Dados
class Usuario(db.Model):
    # Nome da Tabela no Banco de Dados
    __tablename__ = 'usuario'

    id = db.Column(db.Integer, primary_key=True)
    nome_usuario = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    senha_hash = db.Column(db.String(128), nullable=False)

    def __repr__(self):
        return f'<Usuario {self.nome_usuario}>'
    
    # Método para difinir e gerar a senha hash 
    def set_senha(self, senha):
        self.senha_hash = generate_password_hash(senha) # Esta função pega uma senha em texto puro e retorna seu hash seguro.
    
    # Método para verificar se a senha fornecida corresponde ao hash
    def check_senha(self, senha):
        return check_password_hash(self.senha_hash, senha) # Esta função pega uma senha em texto puro e retorna seu hash seguro.


@app.route('/usuarios', methods=['POST'])
def registrar_usuario():
    # Obter os dados JSON da requisição
    dados = request.json

    # Debug: Imprime os dados recebidos para ajudar na depuração
    print('Dados recebidos para registro:', dados)

    # Validação básica: verifica se os campos essenciais estão presentes
    if not dados or not all(k in dados for k in ('nome_usuario', 'email', 'senha')):
        print('Validação falhou: Dados incompletos.')
        return jsonify({'mensagem': 'Dados incompletos para registro. Campos esperados: nome_usuario, email, senha'}), 400
    
    nome_usuario_input = dados['nome_usuario']
    email_input = dados['email']
    senha_input = dados['senha']

    # Verifica se o nome de usuário ou e-mail já existem no banco
    if Usuario.query.filter_by(nome_usuario=nome_usuario_input).first():
        print(f"Erro: Nome de usuário '{nome_usuario_input}' já existe.")
        return jsonify({'mensagem': 'Nome de usuário já existe.'}), 409
    
    if Usuario.query.filter_by(email=email_input).first():
        print(f"Erro: Email '{email_input}' já existe.")
        return jsonify({'mensagem': 'Email já existe.'}), 409
    

    # Cria uma nova instância de Usuario
    novo_usuario = Usuario(nome_usuario=nome_usuario_input, email=email_input)
    # Define a senha, o que automaticamente gera o hash e armazena em 'senha_hash'
    novo_usuario.set_senha(senha_input)

    db.session.add(novo_usuario)
    db.session.commit()

    # Retorna a resposta de sucesso com os dados do novo usuário (SEM A SENHA HASH)
    print(f"Usuário '{novo_usuario.nome_usuario}' registrado com sucesso. ID: {novo_usuario.id}")
    return jsonify({
        'id': novo_usuario.id,
        'nome_usuario': novo_usuario.nome_usuario,
        'email': novo_usuario.email
    }), 201


# Rota: Listar Todos os Usuários
@app.route('/usuarios', methods=['GET'])
def listar_usuarios():
    # Consulta todos os usuários do banco de dados
    usuarios = Usuario.query.all()

    # Converte a lista de objetos Usuario para uma lista de dicionários Python
    usuarios_json = [
        {
            'id': usuario.id,
            'nome_usuario': usuario.nome_usuario,
            'email': usuario.email
        }
        for usuario in usuarios
    ]

    print(f'Retornando {len(usuarios_json)} usuários.')
    return jsonify(usuarios_json), 200


# Rota: Buscar Usuário por ID 
@app.route('/usuarios', methods=['GET'])
def buscar_usuario_por_id(id):
    # Tenta encontrar o usuário pelo ID, ou retorna 404 Not Found se não encontrar
    usuario = Usuario.query.get_or_404(id)

    # Converte o objeto Usuario para um dicionário (sem a senha hash)
    usuario_json = {
        'id': usuario.id,
        'nome_usuario': usuario.nome_usuario,
        'email': usuario.email
    }

    print(f'Usuário com ID {id} encontrado: {usuario.nome_usuario}')
    return jsonify(usuario_json), 200


# Rota: Atualizar Usuário por ID
@app.route('/usuarios/<int:id>', methods=['PUT'])
def atualizar_usuario(id):
    # Buscar o usuário pelo ID, ou retornar 404 Not Found
    usuario = Usuario.query.get_or_404(id)

    # Obter os dados JSON da requisição
    dados = request.json
    if not dados:
        print('Validaçao falhou: Nenhum dado fornecido para atualização.')
        return jsonify({'mensagem': 'Nenhum dado fornecido para atualização.'}), 400
    
    # Atualiza nome_usuario se for fornecido
    if 'nome_usuario' in dados:
        novo_nome_usuario = dados['nome_usuario']

        # Validação: verifica se o novo nome de usuário já existe (excluindo o próprio usuário)
        # Usamos filter() com expressões para combinar condições AND
        if Usuario.query.filter(Usuario.nome_usuario == novo_nome_usuario, Usuario.id != id). first():
            print(f"Erro: Novo nome de usuário '{novo_nome_usuario}' já existe para outro usuário.")
            return jsonify({'mensage': 'Nome do usuário já existe.'}), 409
    usuario.nome_usuario = novo_nome_usuario
    print(f'Usuário de ID {id}: Nome do usuário atualizado para "{novo_nome_usuario}".')



    # Atualiza email se for fornecido
    if 'email' in dados:
        novo_email = dados['email']

        # Validação: verifica se o novo email já existe (excluindo o próprio usuário)
        if Usuario.query.filter(Usuario.email == novo_email, Usuario.id != id).first():
            print(f'Erro: Novo email "{novo_email}" já existe para outro usuário.')
            return jsonify({'mensagem': 'Email já existe.'}), 409
        usuario.email = novo_email
        print(f'Usuário ID {id}: Email atualizado para "{novo_email}".')


    db.session.commit()

    # Retornar os dados atualizados do usuário
    return jsonify({
        'id': usuario.id,
        'nome_usuario': usuario.nome_usuario,
        'email': usuario.email
    }), 200


# Rota: Excluir Usuário por ID
@app.route('/usuarios/<int:id>', methods=['DELETE'])
def excluir_usuario(id):
    usuario = Usuario.query.get_or_404(id)

    db.session.delete(usuario)
    db.session.commit()

    print(f'Usuário com ID {id} excluído com sucesso.')
    return jsonify({'mensagem': 'Usuário excluido com sucesso!'}), 204


# Rota de Teste Simples (para verificar se o Flask está funcionando)
@app.route('/')
def home():
    """
    Define a rota para a URL raiz ('/').
    Quando alguém acessa a raiz do seu servidor, esta função é executada.
    """
    return 'API de Gerenciamento de Usuários está funcionando! (V1)'


# Execução do Aplicativo
if __name__ == '__main__':
    app.run(debug=True)

