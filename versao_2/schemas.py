from pydantic import BaseModel, Field, EmailStr
from typing import Optional

# Schema para o registro de um novo usuário (dados de entrada POST)
class UsuarioCreate(BaseModel):
     # Field(...) indica que o campo é obrigatório
    # min_length e max_length para validação do tamanho da string
    nome_usuario: str = Field(..., min_length=3, max_length=50, description='Nome de usuário único para o registro.')

    # EmailSTR valida o formato do email
    email: EmailStr = Field(..., description='Endereço de email único para o registro.')

    senha: str = Field(..., min_length=6, max_length=100, description='Senha do usuário (será hashificada).')

# Schema para a atualização de um usuário (dados de entrada PUT)
class UsuarioUpdate(BaseModel):
    # Optional[str] significa que o campo é opcional e pode ser uma string ou None
    nome_usuario: Optional[str] = Field(None, min_length=3, max_length=50, description='Novo nome de usuário (opcional).')

    email: Optional[EmailStr] = Field(None, description='Novo endereço de email (ocional).')
    # Não incluímos a senha aqui, pois a atualização de senha deve ser feita em uma rota separada
    # para maior segurança (geralmente exigindo a senha atual).


# Schema para a resposta de um usuário (dados de saída da API)
# Isso garante que a senha_hash NUNCA seja retornada
class UsuarioResponse(BaseModel):
    id: int
    nome_usuario: str
    email: str

    # Configuração para permitir que o Pydantic crie um modelo a partir de uma instância de ORM (SQLAlchemy)
    model_config = {'from_attributes': True}
