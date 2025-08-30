# JUST FOR REMIND - ONLY IF START NEW PROJECT

bash
# Initialize Alembic with async support
alembic init -t async alembic
Configuration

Add your config in env.py:

python
from app.database import Base, database_url

# This is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
config.set_main_option("sqlalchemy.url", database_url)

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Add your model's MetaData object here
from app.models import User, Message  # import your models
target_metadata = Base.metadata
Migration Commands

bash
# Create migration
alembic revision --autogenerate -m "Initial migration"

# Apply migration
alembic upgrade head