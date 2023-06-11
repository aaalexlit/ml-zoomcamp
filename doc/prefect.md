To start prefect server locally

```bash
prefect server start
```

and it will run on http://127.0.0.1:4200

and to run python scripts and get the proper paths run it from the main directory like this in a new terminal

```bash
python prefect/flows/orchestrate.py
```

and then to be able to see mlflow experiments in the UI run the following from the same directory

```bash
mlflow ui --backend-store-uri sqlite:///mlflow.db
```