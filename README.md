# Sistema de Alocação de Professores

Este é um sistema desenvolvido em Python com interface gráfica Tkinter para gerenciar a alocação de professores em disciplinas acadêmicas.

## Funcionalidades

- Cadastro e gerenciamento de professores
- Cadastro e gerenciamento de disciplinas
- Alocação automática de professores considerando:
  - Disponibilidade de horários
  - Modalidade de ensino (presencial/EAD/híbrido)
  - Necessidade de laboratório
  - Distribuição equilibrada de carga horária
- Exportação de dados em formatos JSON e CSV
- Interface gráfica intuitiva e responsiva

## Requisitos

- Python 3.x
- Tkinter (geralmente já vem instalado com Python)

## Como Usar

1. Execute o arquivo `main.py`
2. Cadastre os professores com suas informações e disponibilidades
3. Cadastre as disciplinas com seus requisitos
4. Clique em "Alocar Professores" para realizar a alocação automática
5. Exporte os resultados em JSON ou CSV conforme necessário

## Estrutura de Dados

O sistema utiliza dois arquivos JSON para persistência:
- `professores.json`: Armazena dados dos professores
- `disciplinas.json`: Armazena dados das disciplinas

## Contribuição

Sinta-se à vontade para contribuir com o projeto através de pull requests ou reportando issues. 