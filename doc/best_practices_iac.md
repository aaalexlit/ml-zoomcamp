First we need to create an s3 bucket that terraform will use to store configuration manually
In our case it's name is terraform-state-mlops-zoomcamp

It can be done using AWS CLI
```shell
aws s3 mb s3://terraform-state-mlops-zoomcamp
```

Initialize TF configuration
```shell
terraform init
```

To bump the provider version

```shell
terraform init -upgrade
```

To see execution plan
```shell
terraform plan
```

It will ask to provide a value for producer stream name which in this case is `start-ride-events`

Lambda depends on the image in the ECR repository. So we need to build and push it first.
Also, it depends on the s3 bucket with the model in the runtime. So it needs to be created first.

In practice, the Image build-and-push step is handled by CI/CD pipeline and not the IaC script.