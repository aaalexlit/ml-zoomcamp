Install pre-commit tool that helps to define git's pre-commit hook

```shell
pipenv install --dev pre-commit
```

To pretend that [best_practices/code/](../best_practices/code/) is a standalone repo for the purposes of demonstration

```shell
git init
```

create a sample config
```shell
pre-commit sample-config > .pre-commit-config.yaml
```

and create a hook in [.git/hooks/](../best_practices/code/.git/hooks/)

```shell
pre-commit install
```

And then we can add isort, black, etc by modifying [.pre-commit-config.yaml](../best_practices/code/.pre-commit-config.yaml)