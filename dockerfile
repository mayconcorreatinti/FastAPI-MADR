FROM python:3.12

ENV POETRY_VIRTUALENVS_CREATE=false

WORKDIR app/

COPY . .

RUN pip install poetry

RUN poetry config installer.max-workers 10 
# Increase the number of workers to speed up the parallel installation of dependencies

RUN poetry install --no-root

EXPOSE 8000
CMD poetry run uvicorn --host 0.0.0.0 tcc_my_project.app:app

