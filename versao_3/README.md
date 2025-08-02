# Sistema de Gerenciamento de Usuários - Versão 3: Refatoração e Otimização

Esta é a versão mais avançada do sistema de gerenciamento de usuários, com foco em **refatoração, robustez e otimização do código**, aplicando boas práticas de desenvolvimento para um sistema mais maduro e sustentável.

---

### Funcionalidades:
* **Cadastro de Usuários:** Com validação rigorosa e feedback aprimorado.
* **Login de Usuário:** Autenticação segura e eficiente.
* **Listar Usuários:** Exibe todos os usuários registrados.
* **Buscar Usuários:** Funcionalidades aprimorada para busca rápida por critérios.
* **Excluir Usuários:** Nova funcionalidade para remoção segura de contas.

---

### O que esta versão demonstra:
* **Refatoração para Maior Modularidade:** O código foi extensivamente reorganizado em **funções e/ou classes bem definidas**, promovendo a **reutilização de código**, facilitando a **manutenção** e tornando o sistema mais **escalável** para futuras expansões.
* **Tratamento de Exceções Robusto:** Implementação de mecanismos de **tratamento de erros (try-except)** para gerenciar situações inesperadas de forma elegante, prevenindo falhas do programa e oferecendo uma **experiência do usuário mais estável e confiável**.
* **Otimização de Operações:** Melhorias na lógica interna para **otimizar a performance** de operações críticas, como busca e persistência de dados.
* **Aplicações de Boas Práticas de Código:** Demonstração do uso de convenções de código, comentários claros e estrutura lógica para um código de alta qualidade.

---

### Como Rodar:
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


