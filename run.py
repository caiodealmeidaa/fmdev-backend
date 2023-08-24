from flask import Flask
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, create_access_token

# O código que você forneceu cria uma instância do Flask para iniciar sua aplicação. 

# Cria uma instância da classe Flask, que é o núcleo da sua aplicação.
app = Flask(__name__)
# Inicializa a extensão Flask-Bcrypt, que é usada para criptografar senhas.
bcrypt = Bcrypt(app)
#  Inicializa a extensão Flask-JWT-Extended, que é usada para lidar com autenticação por tokens JWT (JSON Web Tokens).
jwt = JWTManager(app)


# Essa função é responsável por configurar e inicializar a aplicação. Ela recebe um nome de arquivo de configuração como entrada, carrega as configurações definidas nesse arquivo, registra blueprints (conjuntos de rotas) da API, inicializa o banco de dados usando o SQLAlchemy e configura o tratamento de CORS (Cross-Origin Resource Sharing) usando a extensão Flask-CORS. Por fim, ela retorna a instância da aplicação.
def create_app(config_filename):
    app.config.from_object(config_filename)

    from app import api_bp
# Registra o blueprint api_bp com um prefixo de URL '/api'. Isso significa que todas as rotas definidas no blueprint terão '/api' como prefixo de URL.
    app.register_blueprint(api_bp, url_prefix='/api')


# Importa a instância do SQLAlchemy definida no módulo Model.
    from Model import db
# Inicializa o SQLAlchemy com a instância da aplicação. Isso conecta o banco de dados à aplicação.
    db.init_app(app)

# Configura a extensão Flask-CORS para permitir solicitações de outros domínios. Isso é útil para permitir que sua API seja acessada por diferentes origens (origins).
    CORS(app)

    return app

# Essa parte do código verifica se o script está sendo executado diretamente (não sendo importado como um módulo). Se for o caso, cria a aplicação usando a função create_app, e em seguida inicia o servidor de desenvolvimento com o método run. Isso permite que você execute a aplicação diretamente ao executar o script, por exemplo, no ambiente de desenvolvimento.
if __name__ == "__main__":
    app = create_app("config")
    app.run(debug=True, host='127.0.0.1')

# Resumindo, esse código é um ponto de entrada para a sua aplicação Flask. Ele cria e configura a instância do Flask, inicializa extensões importantes, registra rotas da API e inicia o servidor de desenvolvimento quando o script é executado diretamente.