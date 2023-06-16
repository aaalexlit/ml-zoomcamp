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