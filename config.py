import os
from environs import Env

# Cria uma instância do objeto Env da biblioteca environs, que é usada para carregar as variáveis de ambiente a partir de um arquivo .env.
env = Env()

#if os.environ.get('FLASK_ENV') is None or os.environ.get('FLASK_ENV') == 'production':
#    env.read_env()
#else:
# Carrega as variáveis de ambiente do arquivo .env.development no ambiente.
env.read_env('.env.development')

# You need to replace the next values with the appropriate values for your configuration

basedir = os.path.abspath(os.path.dirname(__file__))
# Define se as queries SQL executadas serão mostradas no terminal. Nesse caso, está definido como False.
SQLALCHEMY_ECHO = False
# Habilita o rastreamento de modificações no SQLAlchemy. Está definido como True.
SQLALCHEMY_TRACK_MODIFICATIONS = True
# Define a URI de conexão com o banco de dados PostgreSQL usando as variáveis de ambiente carregadas.
SQLALCHEMY_DATABASE_URI = f"postgresql://{env.str('DB_USER')}:{env.str('DB_PWD')}@{env.str('DB_HOST')}:{env.str('DB_PORT')}/{env.str('DB_NAME')}"
# Define a chave secreta usada para codificar e decodificar tokens JWT.
JWT_SECRET_KEY = 'secret'
#  Define o diretório onde os dados brutos do pré-processamento serão armazenados.
PRE_PROCESSING_RAW = 'data/pre_processing'
# Define o diretório onde os modelos treinados serão armazenados.
TRAIN_MODELS = 'data/models'
# Define o diretório onde os pipelines treinados serão armazenados.
TRAIN_PIPELINES = 'data/pipelines'
# Define o diretório onde as saídas do TPOT durante o treinamento serão armazenadas.
TRAIN_TPOT_OUTPUT = 'data/tpot/output'
# Define o diretório onde os dados enriquecidos após o pré-processamento serão armazenados.
PRE_PROCESSING_ENRICHED = 'data/enriched'
#  Define o diretório onde os recursos de treinamento serão armazenados.
TRAIN_FEATURES = 'data/train/features'
# Define o diretório onde os alvos de treinamento serão armazenados.
TRAIN_TARGET = 'data/train/target'
# Define o diretório onde os recursos de teste serão armazenados.
TEST_FEATURES = 'data/test/features'
#  Define o diretório onde os alvos de teste serão armazenados.
TEST_TARGET = 'data/test/target'
# Define a URL base da sua aplicação.
BASE_URL = 'http://localhost:5000'
# Define o diretório onde os arquivos enviados pelos usuários serão armazenados.
UPLOAD_FOLDER = 'data/upload'

# Essas configurações são essenciais para o funcionamento da sua aplicação Flask e para garantir que ela tenha acesso às informações corretas, como as credenciais do banco de dados e as chaves secretas necessárias. Elas devem ser definidas de acordo com o ambiente em que a aplicação está sendo executada (desenvolvimento, produção, etc.).