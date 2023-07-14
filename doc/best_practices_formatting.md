Install `black` for formatting and `isort` for sorting imports

```shell
pipenv install --dev black isort
```

Like this black will show the diff without applying
with `-S` option it doesn't try to replace single quotes with double quotes

```shell
black -S --diff . | less
```

it's config can be added to [pyproject.toml](../best_practices/code/pyproject.toml) file