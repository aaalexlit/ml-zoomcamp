FROM public.ecr.aws/lambda/python:3.9

RUN pip install -U pip
RUN pip install pipenv

COPY Pipfile* ./

RUN pipenv install --system --deploy

COPY lambda_function.py ./
COPY model.py ./

CMD [ "lambda_function.lambda_handler" ]