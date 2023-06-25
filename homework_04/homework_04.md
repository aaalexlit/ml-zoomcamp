## To convert notebook to a script 


```bash
jupyter nbconvert --to script starter.ipynb
```

## Create pipenv environment
```bash
pipenv install scikit-learn==1.2.2 pyarrow pandas --python=3.9
```

## Run the script for March 2022

```bash
pipenv run python starter.py yellow  2022 3
```

## Build and run from docker

```bash
docker build -t aaalexlit/zoomcampl-model:v1 .
docker run --rm --name zoomcamp-model -v $HOME/.aws:/root/.aws:ro aaalexlit/zoomcampl-model:v1
```
