-------quick run-------
alembic upgrade head
pip install -r requirements.txt
add .env
BOT_TOKEN=
ADMIN_ID=
cd app
python3 main.py run 












--------alembic--------
JUST FOR REMIND
ONLY IF START NEW PROJECT

alembic init -t async alembic


add your config in env.py
from app.database import Base, database_url
# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.

config.set_main_option("sqlalchemy.url", database_url)
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here

from app.models import User, Message  # импортируйте ваши модели
target_metadata = Base.metadata

alembic revision --autogenerate -m "Initial migration"
alembic upgrade head