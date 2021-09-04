pip install -U poetry
poetry install
poetry update
pip install alembic
cd alembic
alembic upgrade head
alembic revision --autogenerate;alembic upgrade head
cd ..