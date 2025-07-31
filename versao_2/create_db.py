from app import app, db, Usuario   # Importe 'Usuario' para que o SQLAlchemy saiba do modelo
import os

with app.app_context():
    # Remove o arquivo do banco de dados se ele já existir (útil para recomeçar do zero no desenvolvimento)
    # CUIDADO: Não use isso em produção, pois apagaria todos os dados!

    if os.path.exists('sitedb'):
        os.remove('site.db') #  Lembre-se de remover ou comentar essa linha em um ambiente de produção
        print('Arquivo "site.db" existente removido.')

    # Cria todas as tabelas definidas nos modelos do SQLAlchemy
    db.create_all()
    print('Tabelas do banco de dados criadas com sucesso!')

