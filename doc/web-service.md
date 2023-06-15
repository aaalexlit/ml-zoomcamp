# Create a virtual environment for the service

Switch to the service directory and run
```bash
pipenv install scikit-learn==1.2.2 flask --python=3.9
```
to install the version of scikit-learn that was used to train the model

# Activate the virtual environment

```bash
pipenv shell
```

# The main functinality of the service will be in [`predict.py`](../web-service/predict.py)

# Serve the model with a production server (eg `gunicorn`)

In the same directory (eg. web-service) install `gunicorn` in pipenv

```bash
pipenv install gunicorn
```

and then run the server

```bash
gunicorn --bind=0.0.0.0:9696 predict:app
```

# To test the served model

Execute [test.py](../web-service/test.py)

it requires `requests` library to be installed. 
It can be either installed in the same pipenv as a dev requirement like this
```bash
pipenv install --dev requests
```

or the main project conda environtent that already has this dependency can be used.