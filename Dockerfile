FROM python:3.12-slim AS builder
WORKDIR /install
COPY ./requirements.txt /install/requirements.txt
RUN pip install --no-cache-dir --prefix=/install -r /install/requirements.txt
COPY ./pyproject.toml /install/pyproject.toml

FROM python:3.12-slim AS runtime
WORKDIR /code
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*
RUN groupadd -r appgroup && useradd -r -g appgroup appuser
COPY --from=builder /install /usr/local
COPY ./app /code/app
COPY ./alembic /code/alembic
COPY ./seed.py /code/seed.py
COPY ./alembic.ini /code/alembic.ini
RUN mkdir -p /code/static

RUN chown -R appuser:appgroup /code
USER appuser
EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]