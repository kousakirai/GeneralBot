pip install -U pip==21.2.4
pip install -U poetry
pip install "pymongo[srv]"
poetry install
poetry update
python3 main.py