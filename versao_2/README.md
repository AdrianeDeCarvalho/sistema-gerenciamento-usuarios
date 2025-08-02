# Sistema de Gerenciameneto de Usuários - Versão 2: Melhorias e Buscas

Esta versão foca na **evolução das funcionalidades básicas** da Versão 1, introduzindo melhorias na experiência do usuário e na robustez do sistema.

---

### Funcionalidades:
* **Cadastro de Usuário**: Com validação aprimoradas para maior segurança e integridade dos dados.
* **Login de Usuário**: Autenticação melhorada.
* **Listar Usuário**: Exibe todos os usuários cadastrados.
* **Buscar Usuário**: Nova funcionalidade para encontrar usuários por critérios específico.

---

### O que esta versão demonstra:
* **Implementação de Validação de Entrada:** Adição de verificações rigorosas para garantir a qualidade e segurança dos dados inseridos, minimizando erros e comportamentos inesperados.
* **Melhoria na Entrada do Código:** Refatoração e organização do código para maior modularidade e legibilidade, facilitando a manutenção e a adição de novas funcionalidades.
* **Funcionalidade de Busca:** Desenvolvimento de uma lógica para permitir a busca eficiente de usuários, aprimorando a usabilidade do sistema.

---

### Como Rodar:
Siga os passos abaixo para executar esta versão do sistema:

1. Certifique-se de ter **Python** instalado em sua máquina.
2. Navegue até esta pasta (`versao_2/`) no seu terminal.
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




