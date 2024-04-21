# app/Dockerfile

FROM python:3.9

RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    software-properties-common \
    git \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /opt
RUN python -m venv venv
RUN pip install poetry
COPY pyproject.toml poetry.lock ./
RUN poetry config virtualenvs.create false
RUN poetry install --no-interaction --no-root --only main

WORKDIR /app
COPY . .
EXPOSE 8501

HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

ENV DEBUG=false
ENTRYPOINT ["streamlit", "run", "Main_Page.py", "--server.port=8501", "--server.address=0.0.0.0"]
