FROM svizor/zoomcamp-model:mlops-3.10.0-slim

RUN pip install -U pip
RUN pip install pipenv

WORKDIR /app

COPY Pipfile* ./
RUN pipenv install --system --deploy

COPY starter.py ./

ENTRYPOINT [ "python", "starter.py", "yellow", "2022", "4" ]