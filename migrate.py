from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from Model import db
from run import create_app

# Esse trecho de código configura o Flask-Migrate, uma extensão que fornece suporte para migrações de banco de dados em aplicativos Flask
# As migrações de banco de dados são usadas para gerenciar as alterações no esquema do banco de dados conforme a aplicação evolui.

# Cria uma instância da aplicação Flask usando as configurações definidas no arquivo 'config'.
app = create_app('config')

# Inicializa a extensão Flask-Migrate, passando a instância da aplicação e a instância do SQLAlchemy.
migrate = Migrate(app, db)
# Cria uma instância do objeto Manager e associa a instância da aplicação a ela.
manager = Manager(app)
# Adiciona o comando db à instância do Manager, permitindo que você execute migrações de banco de dados usando a linha de comando.
manager.add_command('db', MigrateCommand)

# Verifica se o script está sendo executado diretamente (não sendo importado como um módulo).
# Inicia o gerenciador de comandos do Flask, que permite executar vários comandos de linha de comando relacionados à aplicação, incluindo migrações de banco de dados.
if __name__ == '__main__':
    manager.run()

# Basicamente, esse script permite que você execute migrações de banco de dados e gerencie o esquema do banco de dados usando comandos de linha de comando, como python manage.py db migrate e python manage.py db upgrade. Isso é útil para manter o esquema do banco de dados atualizado à medida que a aplicação evolui.