# https://fastapi.tiangolo.com/deployment/docker/#docker-image-with-poetry
FROM python:3.10 as requirements-stage

WORKDIR /tmp

RUN pip install "poetry==1.5.1"
COPY ./pyproject.toml ./poetry.lock* /tmp/
RUN poetry export -f requirements.txt --output requirements.txt --without-hashes


FROM python:3.10

WORKDIR /code
COPY --from=requirements-stage /tmp/requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
COPY ./api /code/api

CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "9000"]
