# Sistema de Gerenciamento de Usuários - Versão 3: Implementando as Rotas da API - CRUD de Usuários e Validação de Dados Mais Robusta com Pydantic


Implementando as funções para lidar com as operações Create, Read, Update e Delete (CRUD) de usuários, usando o Flask e o SQLAlchemy

---

*** Funcionalidades:
* ****
* ****
* ****

---

*** O que esta versão demonstra:
* Implementado todas as rotas CRUD para gerenciar usuários.
* Aprendendo sobre métodos HTTP e códigos de status relevantes.
* Entendendo como usar request.json e jsonify() para lidar com dados JSON.
* Utilizando os métodos de consulta do SQLAlchemy (.query.all(), .query.get_or_404(), .query.filter(), .first()) para interagir com o banco de dados.
* Incorpora validações para campos obrigatórios e unicidade.
* Criou um arquivo schemas.py para definir os modelos de validação de entrada (UsuarioCreate, UsuarioUpdate) e um modelo de saída (UsuarioResponse).
* Atualizou as rotas POST e PUT no app.py para usar os schemas Pydantic para validar os dados de entrada e lidar com ValidationError.
* Atualizou as rotas GET para usar o UsuarioResponse para formatar a saída, garantindo que senha_hash nunca seja exposta.

---

*** Como Rosar:
Siga os passos abaixo para executar esta versão do sistema:

1. Certifique-se de ter **Python** instalado em sua máquina.
2. Navegue até esta pasta (`versao_3/`) no seu terminal.
3. **Crie e ative um ambiente virtual** (opcional, mas recomendado para isolar as dependências):
   ```bash
   python -m venv venv
   # No Windows:
   .\venv\Scripts\activate
   # No macOS/Linux:
   source venv/bin/activate
   ```
4. **Instale as dependências** do projeto:
   ```bash
   pip install -r requirements.txt
   ```
5. **Execute o script principal:**
   ```bash
   python app.py
   ```

---

### 📁 Código:
* [app.py](app.py)
* [create_db.py](create_db.py)

---

[⬅️ Voltar ao README Principal](https://github.com/AdrianeDeCarvalho/sistema-gerenciamento-usuarios)
