FROM python:3.10

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# sqlite3 can be removed if DB is moved to other engine
RUN apt-get -y update && apt-get install -y --no-install-recommends sqlite3
RUN pip install --no-cache-dir --upgrade pip setuptools poetry

WORKDIR /app
COPY poetry.lock pyproject.toml ./

RUN poetry config virtualenvs.create false
RUN poetry install --no-interaction

COPY . .
