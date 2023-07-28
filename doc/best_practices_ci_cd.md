create secrets in GitHub Settings => Secrets and Variables => Actions => New repository secret

To test actions created `develop` branch and then create a PR to it (for instance from master branch)


To destroy infra created by github actions:
```shell
terraform init -backend-config="key=mlops-zoomcamp-prod.tfstate" --reconfigure
terraform destroy --var-file vars/prod.tfvars
```