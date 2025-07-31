from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import os # Importante para gerenciar caminhos de arquivo
from pydantic import ValidationError 
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity

# Importar os schemas criados
from schemas import UsuarioCreate, UsuarioResponse, UsuarioUpdate


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

# **NOVA CONFIGURAÇÃO DO JWT**
# A chave secreta é usada para assinar os tokens. Use uma string aleatória e segura.
# Em produção, você deve obter isso de uma variável de ambiente!
app.config["JWT_SECRET_KEY"] = "super-secreto-e-aleatorio-12345"

# Inicializa a extensão JWT
jwt = JWTManager(app)

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

# Rota de registro (POST) - SEM ALTERAÇÃO, pois deve ser pública
@app.route('/usuarios', methods=['POST'])
def registrar_usuario():
    try:
        # 1. Valida os dados de entrada com Pydantic
        # O Pydantic irá levantar ValidationError se os dados forem inválidos
        dados_usuario = UsuarioCreate(**request.json)
    except ValidationError as e:
        # Retorna uma mensagem de erro detalhada do Pydantic
        print(f"Erro de validação ao registrar usuário: {e.errors()}")
        return jsonify({"mensagem": "Dados de entrada inválidos", "erros": e.errors()}), 400
    except Exception as e:
        print(f"Erro inesperado ao parsear JSON: {e}")
        return jsonify({"mensagem": "Requisição inválida. Certifique-se de que o Body é um JSON válido."}), 400
    

    # Verifica se o nome de usuário ou e-mail já existem no banco
    # Usamos dados_usuario.nome_usuario e dados_usuario.email pois já foram validados pelo Pydantic
    if Usuario.query.filter_by(nome_usuario=dados_usuario.nome_usuario).first():
        print(f"Erro: Nome de usuário '{dados_usuario.nome_usuario}' já existe.")
        return jsonify({'mensagem': 'Nome de usuário já existe.'}), 409
    
    if Usuario.query.filter_by(email=dados_usuario.email).first():
        print(f"Erro: Email '{dados_usuario.email}' já existe.")
        return jsonify({'mensagem': 'Email já existe.'}), 409
    

    # Cria uma nova instância de Usuario
    novo_usuario = Usuario(nome_usuario=dados_usuario.nome_usuario, email=dados_usuario.email)
    novo_usuario.set_senha(dados_usuario.senha)  # A senha já veio validada pelo Pydantic

    db.session.add(novo_usuario)
    db.session.commit()

    # Retorna a resposta de sucesso usando o Schema UsuarioResponse
    print(f"Usuário '{novo_usuario.nome_usuario}' registrado com sucesso. ID: {novo_usuario.id}")
    return jsonify(UsuarioResponse.model_validate(novo_usuario).model_dump()), 201


# Rota: Autenticação de Usuário e Geração de Token (POST)
@app.route('/auth', methods=['POST'])
def login():
    # 1. Obtém os dados de login (nome do usuário e senha)
    dados = request.json
    if not dados or 'nome_usuario' not in dados or 'senha' not in dados:
        return jsonify({"mensagem": "Nome de usuário e senha são obrigatórios"}), 400
    
    nome_usuario = dados.get('nome_usuario', None)
    senha_usuario = dados.get('senha', None)

    # 2. Buscar o usuário no banco de dados
    usuario = Usuario.query.filter_by(nome_usuario=nome_usuario).first()

    # 3. Verifica se o usuário existe e se a senha está correta
    # Usamos o método check_senha() do nosso modelo
    if not usuario or not usuario.check_senha(senha_usuario):
        print(f'Tentativa de login falhou para o usuário "{nome_usuario}".')
        return jsonify({"mensagem": "Nome de usuário ou senha inválidos"}), 401 # Unauthorized

    # 4. Se a autenticação for bem-sucedida, cria um token de acesso
    # O 'identity' será o valor que 'get_jwt_identity()' irá retornar
    access_token = create_access_token(identity=str(usuario.id))
    print(f'Login bem-sucedido para o usuário "{nome_usuario}". Token gerado.')

    # 5. Retorna o token para o cliente
    return jsonify(access_token=access_token), 200


# Rota: Listar Todos os Usuários - AGORA PROTEGIDA
@app.route('/usuarios', methods=['GET'])
@jwt_required()
def listar_usuarios():
    # Esta função só será executada se um token válido for fornecido
    # Você pode até obter a identidade do usuário logado, se precisar
    usuario_logado_id = get_jwt_identity()
    print(f'Requisição GET /usuarios feita pelo usuário com ID: {usuario_logado_id}')

    # Consulta todos os usuários do banco de dados
    usuarios = Usuario.query.all()

    # Converte a lista de objetos Usuario para uma lista de dicionários Python
    usuarios_json = [UsuarioResponse.model_validate(usuario).model_dump() for usuario in usuarios]

    return jsonify(usuarios_json), 200


# Rota: Buscar Usuário por ID - AGORA PROTEGIDA
@app.route('/usuarios', methods=['GET'])
@jwt_required()
def buscar_usuario_por_id(id):
    # Verificação de Autorização: O usuário só pode ver o próprio perfil
    # Vamos pegar o ID do usuário logado
    usuario_logado_id = get_jwt_identity()

    if id != usuario_logado_id:
        return jsonify({"mensagem": "Você não tem permissão para visualizar este perfil."}), 403 # Forbidden
    
    usuario = Usuario.query.get_or_404(id)
    # Converte o objeto Usuario para um dicionário usando UsuarioResponse
    usuario_json = UsuarioResponse.model_validate(usuario).model_dump()

    print(f'Usuário com ID {id} encontrado: {usuario.nome_usuario}')
    return jsonify(usuario_json), 200


# Rota: Atualizar Usuário por ID - AGORA PROTEGIDA
@app.route('/usuarios/<int:id>', methods=['PUT'])
@jwt_required()
def atualizar_usuario(id):
    usuario_logado_id = get_jwt_identity()
    if id != usuario_logado_id:
        return jsonify({"mensagem": "Você mão tem permissão para atualizar este perfil."}), 403 # Forbidden

    # Buscar o usuário pelo ID, ou retornar 404 Not Found
    usuario = Usuario.query.get_or_404(id)

    try:
        if not request.is_json:
            raise ValidationError("Conte´do da requisição não é JSON.")
        dados_atualizacao = UsuarioUpdate.model_validate(request.json)
    except ValidationError as e:
        print(f'Erro de validação ao atualizar usuário: {e.errors()}')
        return jsonify({"mensagem": "Dados de entrada inválidos", "erros": e.errors()}), 400
    except ValueError as e:
        print(f'Erro ao processar requisição: {e}')
        return jsonify({"mensagem": str(e)}), 400
    except Exception as e:
        print(f'Erro inesperado ao parsear JSON: {e}')
        return jsonify({"mensagem": "Requisição inválida. Certifique-se de que o Body é um JSON válido."}), 400


    if dados_atualizacao.nome_usuario is not None:
        if Usuario.query.filter(Usuario.nome_usuario == dados_atualizacao, Usuario.id != id). first():
            print(f"Erro: Novo nome de usuário '{dados_atualizacao.nome_usuario}' já existe para outro usuário.")
        return jsonify({'mensagem': 'Nome de usuário já existe.'}), 409
    usuario.nome_usuario = dados_atualizacao.nome_usuario
    print(f'Usuário de ID {id}: Nome do usuário atualizado para "{dados_atualizacao.nome_usuario}".')


    if dados_atualizacao is not None:
        if Usuario.query.filter(Usuario.email == dados_atualizacao.email, Usuario.id != id).first():
            print(f"Erro: Novo email '{dados_atualizacao.email}' já existe para outro usuário.")
            return jsonify({'mensagem': 'Email já cadastrado.'}), 409
        usuario.email = dados_atualizacao.email
        print(f"Usuário ID {id}: Email atualizado para '{dados_atualizacao.email}'.")


    db.session.commit()

    # Retorna os dados atualizados do usuário usando o Schema UsuarioResponse
    return jsonify(UsuarioResponse.model_validate(usuario).model_dump()), 200


# Rota: Excluir Usuário por ID - AGORA PROTEGIDA
@app.route('/usuarios/<int:id>', methods=['DELETE'])
@jwt_required()
def excluir_usuario(id):
    # Verificação de Autorização: O usuário só pode deletar o próprio perfil
    usuario_logado_id = get_jwt_identity()
    if id != usuario_logado_id:
        return jsonify({"mensagem": "Você não tem permissão para excluir este perfil."}), 403 # Forbidden

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
    return 'API de Gerenciamento de Usuários está funcionando! (V3)'


# Execução do Aplicativo
if __name__ == '__main__':
    app.run(debug=True)

