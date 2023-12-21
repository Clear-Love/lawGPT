docker compose up -d
pip install poetry
poetry build
pip install ./dist/*.whl
lawgpt -p 8000