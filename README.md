# RiverLevelForecastRSL

## Descrição

Este projeto tem como objetivo prever o nível do Rio do Sul utilizando variáveis hidrometeorológicas provenientes das cidades de Ituporanga e Taió, por meio de um modelo de **regressão linear multivariada** implementado em Python. As variáveis utilizadas como preditoras incluem:

- Nível do rio em Ituporanga  
- Volume de chuva em Ituporanga  
- Nível do rio em Taió  
- Volume de chuva em Taió

Essas localidades foram escolhidas por sua relevância na bacia hidrográfica da região. A previsão é feita com base em dados históricos e técnicas de aprendizado de máquina.

---

## Funcionalidades

- Implementação de modelo de regressão linear multivariada;
- Visualização dos dados e do desempenho do modelo via **Jupyter Notebook** (`main.ipynb`);
- Interface gráfica interativa executada via `init.py` para explorar previsões e resultados;
- Código modular e documentado.

---

## Estrutura do Projeto

```bash
RiverLevelForecastRSL/
├── requirements.txt        # Lista de dependências do projeto
├── init.py                 # Interface gráfica para execução do modelo
├── functions.py            # Arquivo com funções auxiliares
├── main.ipynb              # Jupyter Notebook com análise e testes do modelo
├── dataset.csv             # CSV dos dados analisados
├── FinalRL                  # Artigo do trabalho - Notebook
└── models/                 # Modelos treinados

```

## Requisitos

- Python 3.8 ou superior
- Jupyter Lab ou Jupyter Notebook
- Bibliotecas listadas no requirements.txt

## Instalação

Clone o repositório:

```bash
git clone https://github.com/seuusuario/RiverLevelForecastRSL.git
cd RiverLevelForecastRSL
``` 
Crie um ambiente virtual (opcional, mas recomendado):
```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows
```
Instale as dependências:
```bash
pip install -r requirements.txt
```

## Execução

### Opção 1: Interface Gráfica
Execute o seguinte comando para abrir a interface de exploração do modelo:

```bash
python init.py
```
A interface permite inserir valores de entrada, visualizar os resultados do modelo e comparar com dados reais (caso disponíveis).


### Opção 2: Jupyter Notebook
Inicie o Jupyter Lab ou Notebook:

```bash
jupyter lab
```
Abra o arquivo main.ipynb e execute célula por célula para visualizar as análises e testes.

# Autor
Pedro Daniel de Oliveira Hoeller 
Estudante de Ciência da Computação – Instituto Federal Catarinense (IFC)
GitHub: github.com/Pedro-IFC
