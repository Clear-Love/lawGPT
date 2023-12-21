docker compose up -d
pip install poetry
poetry build
pip install .\dist\lawgpt-0.1.0-py3-none-any.whl
lawgpt server -p 8000