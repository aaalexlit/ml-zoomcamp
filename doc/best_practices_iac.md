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


# Run e2e test

1. apply terraform configuration for staging from [infrastructure](../best_practices/code/infrastructure/) directory

```shell
terraform apply -var-file="vars/stg.tfvars"
```

2. copy the model to the newly created s3 bucket by running [deploy-manual.sh](../best_practices/code/scripts/deploy-manual.sh)
```shell 
./deploy-manual.sh
```

3. run e2e test [test-cloud-e2e.sh](../best_practices/code/scripts/test-cloud-e2e.sh)
```shell
./test-cloud-e2e.sh
```

4. destroy the infrastructure
```shell
terraform destroy -var-file="vars/stg.tfvars"
```