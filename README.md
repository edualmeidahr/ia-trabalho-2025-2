# Evolução da Inteligência Artificial: De Sistemas Simbólicos a Bioinspirados
[![SO][Ubuntu-badge]][Ubuntu-url]
[![IDE][vscode-badge]][vscode-url]
[![Language][python-badge]][python-url]

Este repositório contém o código-fonte do **Trabalho 2 da disciplina de Inteligência Artificial**, ministrada pelo docente Tiago Alves de Oliveira, no CEFET-MG, campus V. O projeto aborda quatro pilares fundamentais da IA, integrando desde a lógica simbólica clássica até heurísticas bioinspiradas modernas.

---

## 📂 Estrutura do Trabalho

O projeto está organizado em quatro módulos independentes que representam diferentes paradigmas da computação:

* **Parte 1: Árvore de Decisão Manual** (`src/part1_tree_manual/`)
    * Implementação de um Sistema Especialista simbólico focado em orientação vocacional.
* **Parte 2: Aprendizado de Máquina Supervisionado** (`src/part2_ml/`)
    * Modelagem preditiva e classificação utilizando KNN, SVM (com Grid Search) e Árvores de Decisão.
* **Parte 3: Algoritmos Genéticos (AG)** (`src/part3_ga/`)
    * Otimização combinatória aplicada à geração automática de provas com restrições multiobjetivo.
* **Parte 4: Inteligência de Enxame e Sistemas Imunológicos** (`src/part4_swarm_immune/`)
    * Resolução de problemas complexos via **ACO** (*Ant Colony Optimization*) e **CLONALG** (*Clonal Selection Algorithm*).

---

## 📥 Clone do Repositório

Para configurar o projeto localmente, clone o repositório através do terminal:

```bash
# via HTTPS
git clone [https://github.com/edualmeidahr/ia-trabalho-2025-2.git](https://github.com/edualmeidahr/ia-trabalho-2025-2.git)

# via SSH
git clone git@github.com:edualmeidahr/ia-trabalho-2025-2.git

# Acesse a pasta do projeto
cd ia-trabalho-2025-2
```

## 🚀 Requisitos

- Sistema Operacional: Linux (recomendado) ou Windows.

- Python: Versão 3.10 ou superior.

- Ferramentas: pip (gerenciador de pacotes) e make (para automação).

## ⚙️ Instalação das Dependências

O gerenciamento de dependências é realizado através do arquivo `requirements.txt`. 

Nota: Não é necessário criar o ambiente virtual manualmente. O script de execução principal (`run.sh`) já está configurado para criar automaticamente o diretório .venv, ativar o ambiente e realizar a instalação de todas as bibliotecas necessárias (como `scikit-learn`, `numpy`, `pandas` e `matplotlib`).

Caso deseje realizar a instalação manual apenas das bibliotecas:

```BASH
pip install -r requirements.txt
```

## 📂 Detalhes do Projeto

### Estrutura de Diretórios

```Markdown

ia-trabalho-2025-2/
├── data/               # Bases de dados (Adult Census e Banco de Questões)
├── reports/            # Relatórios e figuras geradas (Curvas de convergência, etc.)
├── src/                # Código-fonte dividido por paradigmas
├── Makefile            # Comandos para execução modular
├── requirements.txt    # Dependências do projeto
└── run.sh              # Script principal de automação total

```

## 🏃‍♂️ Execução

Para rodar o projeto, basta usar o script `run.sh` na raiz do projeto. Ele executa o pipeline completo: cria o ambiente virtual, instala as dependências e roda as quatro partes do trabalho sequencialmente.

```Bash
chmod +x run.sh
./run.sh
```

## 💻 Máquinas de Teste

O projeto foi validado nas seguintes configurações de hardware:

| Máquina | Processador            | Memória RAM | Sistema Operacional |
|------------------|------------------------|-------------|---------------------|
| Intel inspiron 15 5000 |Intel(R) Core(TM) i7-11390H    | 16 GB       | Ubunto 22.04     |
| Lenovo ideaPad 3i    | AMD Ryzen 7 5700U       | 12 GB        | Ubuntu 22.04       |

## 📄 Relatório Técnico

Para uma compreensão aprofundada dos fundamentos teóricos, análise detalhada dos resultados experimentais e discussões sobre o desempenho de cada algoritmo, acesse o documento completo:

* ### [➡️ Visualizar Relatório Técnico (PDF)](./Algoritmos_Aprendizagem.pdf)

O relatório abrange:
* **Fundamentação Teórica**: Detalhamento matemático e biológico dos algoritmos.
* **Metodologia**: Justificativa da escolha de cada hiperparâmetro e métrica.
* **Análise Comparativa**: Confronto de dados entre os modelos de Machine Learning e algoritmos de otimização.

## 📨 Autores

<div align="center">
<i>Eduardo Henrique Queiroz Almeida - Computer Engineering Student @ CEFET-MG</i>
<br><br>

[![Gmail][gmail-badge]][gmail-autor1]
[![Linkedin][linkedin-badge]][linkedin-autor1]
[![Telegram][telegram-badge]][telegram-autor1]

<br><br>


<i>Joaquim Cézar Santana da Cruz - Computer Engineering Student @ CEFET-MG</i>
<br><br>

[![Gmail][gmail-badge]][gmail-autor4]
[![Linkedin][linkedin-badge]][linkedin-autor4]
[![Telegram][telegram-badge]][telegram-autor4]


</div>

[linkedin-badge]: https://img.shields.io/badge/-LinkedIn-0077B5?style=for-the-badge&logo=Linkedin&logoColor=white
[telegram-badge]: https://img.shields.io/badge/Telegram-2CA5E0?style=for-the-badge&logo=telegram&logoColor=white
[gmail-badge]: https://img.shields.io/badge/-Gmail-D14836?style=for-the-badge&logo=Gmail&logoColor=white

[linkedin-autor1]: https://www.linkedin.com/in/eduardo-henrique-queiroz-almeida-61378a124/
[telegram-autor1]: https://t.me
[gmail-autor1]: mailto:eduardohenriquecruzeiro123@gmail.com

[linkedin-autor4]: https://www.linkedin.com/in/joaquim-cruz-b760bb350/
[telegram-autor4]: https://t.me/
[gmail-autor4]: mailto:joaquimcezar930@gmail.com

[ubuntu-badge]: https://img.shields.io/badge/Ubuntu-E95420?style=for-the-badge&logo=ubuntu&logoColor=white
[Ubuntu-url]: https://ubuntu.com/
[vscode-badge]: https://img.shields.io/badge/Visual%20Studio%20Code-0078d7.svg?style=for-the-badge&logo=visual-studio-code&logoColor=white
[vscode-url]: https://code.visualstudio.com/docs/?dv=linux64_deb
[make-badge]: https://img.shields.io/badge/_-MAKEFILE-427819.svg?style=for-the-badge
[make-url]: https://www.gnu.org/software/make/manual/make.html
[python-badge]: https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54
[python-url]: https://www.python.org/





