FROM public.ecr.aws/lambda/python:3.9

RUN pip install -U pip
RUN pip install pipenv

COPY Pipfile* ./

RUN pipenv install --system --deploy

COPY *.py ./

CMD [ "lambda_function.lambda_handler" ]