To convert a notebook to a script

```bash
jupyter nbconvert --to script score.ipynb
```

to run a script using pipenv
```bash
pipenv run python score.py green 2021 4
```

To create a prefect deployment for batch scoring programmatically

```bash
python score_deployment.py
```

And a worker needs to be started before running the deployment

```bash
prefect worker start -p mlops-zoomcamp-pool
```
