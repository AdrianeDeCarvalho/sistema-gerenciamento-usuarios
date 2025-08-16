# Sistema de Gerenciamento de Usuários - Versão 1: Funcionalidade Básica

Esta é a primeira iteração do sistema de gerenciamento de usuários, focada em estabelecer as funcionalidades essenciais.

---

### Funcionalidades:
* **Cadastro de Usuário** Permite criar novas contas com nome de usuário e senha.
* **Login de Usuário** Autentica usuários existentes no sistema.
* **Listar Usuários** Exibe todos os usuários cadastrados.

---

### O que esta versão demonstra:
* A **estrutura inicial** para o desenvolvimento de um sistema.
* A implementação de **operações CRUD (Create, Read)** básicas.
* O entendimento do **fluxo de autenticação** simples.

---

### Como Rodar:

Siga os passos abaixo para executar esta versão do sistema:

1. Certifique-se de ter **Python** instalado em sua máquina.
2. Navegue até esta pasta (`versao_1/`) no seu terminal.
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
