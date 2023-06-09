## To start prefect server locally

Prefect server is an orchestration environment (Where Prefect Cloud or Server runs)
The execution environment is not cretated yet

```bash
prefect server start
```

and it will run on http://127.0.0.1:4200

## Run a script
and to run python scripts and get the proper paths run it from the main directory like this in a new terminal

```bash
python prefect/flows/orchestrate.py
```

## See mlflow runs in the UI
and then to be able to see mlflow experiments in the UI run the following from the same directory

```bash
mlflow ui --backend-store-uri sqlite:///mlflow.db
```
# Getting help 

For instance 
```bash
prefect deploy --help
```

# Deploying the workflow

## Initialize prefect project

```bash
prefect project init
```

## Create a work pool or use existing one
1. From prefect UI `Work pools` ==> `Create a Work pool`
1. Give it a name (eg `mlops-zoomcamp-pool`)
1. Set pool type to `Process`

## Create a deployment (using created work pool)

```bash
prefect deploy prefect/flows/orchestrate.py:main_flow -n taxi1 -p mlops-zoomcamp-pool
```

## Start worker (specifying created work pool)

```bash
prefect worker start -p mlops-zoomcamp-pool
```

## Run a deployment
From the deployment UI page Run it using `Quick run` to run immediately.

if the used data is not commited to github at this moment, the run will fail with `FileNotFoundError` (and the same for mlflow.db, a new one will be created) because prefect fetches the things from git to run a deployment. 
So we need to put data to S3 for instance not to keep in on github

# Put the data to an S3 bucket

## Create s3 bucket block

Can be done with the code or through UI
Done with the code in [create_s3_bucket_block.py](../prefect/infra/create_s3_bucket_block.py)

```bash
python prefect/infra/create_s3_bucket_block.py
```

To run a flow to download the needed data locally and then upload it to S3 run the following

```bash
python prefect/flows/load_data_to_s3.py 
```
 
 To create a deploy from it

 ```bash
 prefect deploy prefect/flows/load_data_to_s3.py:web_to_s3 -n load-data-to-s3 -p mlops-zoomcamp-pool
 ```

 ## Create a new flow to work with S3 and deploy it

```bash
prefect deploy prefect/flows/orchestrate_s3.py:main_training_pipeline -n predict-from-s3 -p mlops-zoomcamp-pool
```

# Create deployments using [`deployment.yaml`](../deployment.yaml)

To apply the changes from the file run 

```bash
prefect deploy --all
```

## Run a Deployment from CLI

```bash
prefect deployment run main-training-pipeline/taxi-s3-data
```

# Sheduling a deployment

1. Through the UI
1. On CLI  
eg setting it every 2 minutes
    ```bash
    prefect deployment set-schedule main-training-pipeline/taxi-s3-data --interval 120
    ```

# Using prefect cloud

## Create a new profile to use with the cloud and use it

```bash
prefect profile create cloud
prefect profile use cloud
```

## Log in to prefect cloud either though browser or using the API key
```bash
prefect cloud login
```

## Add blocks (that were created programmatically)
```bash
python prefect/infra/create_s3_bucket_block.py
```
And an email block with [create_email_server_creds.py](../prefect/infra/create_email_server_creds.py)

```bash
python prefect/infra/create_email_server_creds.py
```

## Create work pool from CLI
With the same name as a local one to be able to seamlessly transfer all the deployments

```bash
prefect work-pool create --type process mlops-zoomcamp-pool
```

### Add all the deployments

```bash
prefect deploy --all
```

### Before running a deployment start a worker that pulls work from the 'mlops-zoomcamp-pool' work pool

```bash
prefect worker start -p mlops-zoomcamp-pool 
```