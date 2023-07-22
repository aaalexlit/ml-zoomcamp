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