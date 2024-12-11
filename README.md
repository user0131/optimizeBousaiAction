### Python Installation

Install Python dependencies using Poetry:

```sh
poetry install
```

Activate the virtual environment:

```sh
source .venv/bin/activate
```

## もし.venvがでなかったら
```sh
poetry config --local virtualenvs.in-project true
poetry env remove python
poetry install  
```


## Run Application
```
python src/owl/main.py
```