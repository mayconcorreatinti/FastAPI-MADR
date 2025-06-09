# 📚 MADR FastAPI 

Meu Acervo Digital de Romances é um Trabalho de Conclusão de Curso (TCC) desenvolvido com base nos conhecimentos adquiridos no curso, focado no uso do framework FastAPI para construção de APIs modernas e performáticas. O MADR é uma aplicação web que permite aos usuários gerenciar um acervo digital de romances, oferecendo funcionalidades para cadastro, consulta, edição e exclusão de informações sobre livros, usuários e autores. A aplicação foi projetada para ser intuitiva, escalável e eficiente, utilizando as capacidades assíncronas do FastAPI e boas práticas de desenvolvimento de software.
## Pré-requisitos

- Python 3.8 ou superior
- Git
- Pipx e Poetry (instalados conforme os passos abaixo)

## Como Usar

Para executar o projeto localmente, siga os passos abaixo:

1. Clone o repositório:
   ```bash
   git clone git@github.com:mayconcorreatinti/FastAPI-MADR.git
   ```
2. Abra o arquivo:
   ```bash
   cd FastAPI-MADR 
   ```
3. Instale as ferramentas necessárias:
   ```bash
   pip install pipx
   pipx install poetry
   ```

4. Instale as dependências do projeto:
   ```bash
   poetry install
   ```

5. Ative o ambiente virtual:
   ```bash
   poetry shell
   ```

6. Subir contêiner:
   ```bash
   docker compose up
   ```

7. Execute os testes:
   ```bash
   task test
   ```

8. Inicie a aplicação:
   ```bash
   task run
   ```

## Notas

- Certifique-se de que o Python,Git e docker estão instalados no seu sistema antes de iniciar.
- Em caso de erros, verifique se o arquivo `pyproject.toml` está presente e configurado corretamente.


## Autor

Desenvolvido por Maycon Corrêa Tinti, baseado no curso de FastAPI ministrado por Eduardo Mendes.
