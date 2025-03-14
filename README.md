# Sistema de Alocação de Professores

Este é um sistema desenvolvido em Python com interface gráfica Tkinter para gerenciar a alocação de professores em disciplinas.

## Funcionalidades

- Cadastro de professores com:
  - Nome
  - Área de atuação
  - Disponibilidade de horários
  - Modalidade de ensino

- Cadastro de disciplinas com:
  - Nome
  - Tipo
  - Necessidade de laboratório
  - Horários disponíveis

- Alocação automática de professores às disciplinas
- Exportação da grade em formato JSON e CSV
- Interface gráfica intuitiva
- Gerenciamento de dados persistente

## Como usar

1. Execute o arquivo `main.py`
2. Cadastre os professores com suas disponibilidades
3. Cadastre as disciplinas com seus requisitos
4. Clique em "Alocar Professores" para realizar a alocação automática
5. Exporte os resultados em JSON ou CSV conforme necessário

## Requisitos

- Python 3.x
- Tkinter (geralmente já vem com Python)

## Instalação

```bash
git clone https://github.com/seu-usuario/alocacao-professores.git
cd alocacao-professores
python main.py
``` 