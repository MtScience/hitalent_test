FROM python:3.13.7

ENV PYTHONBEFFERED=1
ENV PYTHONWRITEBYTECODE=1
ENV POETRY_VIRTUALENVS_IN_PROJECT=true
ENV PROJECTDIR="/code"
ENV PATH="/root/.local/bin:${PATH}"

WORKDIR /code

RUN curl -sSL https://install.python-poetry.org/ | python3 -
COPY pyproject.toml poetry.lock ./

RUN poetry install

COPY main.py ./
COPY ./src ./src

EXPOSE 8000

CMD [""]
