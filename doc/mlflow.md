To start mlflow with UI and the backend to store models

```bash
conda activate mlops
mlflow ui --backend-store-uri sqlite:///data/mlflow.db
```

For some reason auto port forwarding doesn't forward it to localhost and gives an error so I had to stop port forwarding on 5000 and add it manually again and then it works