# Como rodar

Utilizar python e pip. Python 3.11 foi a versão específica utilizada no desenvolvimento, e no qual
é garantido que o programa rode.

É indicado que inicie um ambiente virtual python (venv):

```
pip -m venv .venv
```

ative-o

```
source .venv/bin/activate
```

então instale o pacote localmente definido:

```
pip install -e .
```

Agora já é possível rodar a simulação utilizando o comando:

```
python main.py -p t/p_mem_block.txt -f files.txt
```


Caso deseje rodar o verificador estático de código ou algum teste unitário, instale os requerimentos:

```
pip install -r requirements.txt
```

E use ruff

```
ruff check .
```

ou pytest
```
pytest tests
```
