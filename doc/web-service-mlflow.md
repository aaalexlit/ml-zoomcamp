# Run a notebook that uses S3 as an artifact store

[random-forest.ipynb](../web-service-mlflow/random-forest.ipynb)

To be able to run it we need to install AWS CLI to be able to access S3

```bash
echo "Installing AWS CLI"
pushd /tmp
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip -qq awscliv2.zip
sudo ./aws/install
rm -rf awscliv2.zip ./aws
popd
```

Then set up AWS profile
```bash
aws configure
```

And then withing the notebook set the AWS_PROFILE env var
```python
os.environ["AWS_PROFILE"] = "default"
```

To launch [predict.py](../web-service-mlflow/predict.py) first we need to start local mlflow server from [wweb-service-mlflow](../web-service-mlflow/) folder

```bash
mlflow server --backend-store-uri sqlite:///mlflow.db --default-artifact-root s3://mlopszoomcamp-alex
```

Then we also need to install 2 more dependencies in the pipenv and activate the environment
```bash
pipenv install mlflow
pipenv install boto3
pipenv shell
```

Then we can run the Flask App and test it
```bash
python predict.py
python test.py
```