From the command line:

In the [best_practices/code/](../best_practices/code/) in pipenv install pylint wiht

```shell
pipenv install --dev pylint
```

Run pylint on all the files
```shell
pipenv run pylint --recursive=y .
```

Run pylint on an individual file

```shell
pipenv run pylint model.py
```

---

There are various ways of controlling linter's behaviour

one of them is through a [pyproject.toml](../pyproject.toml) file
and ignoring some checks eg
```
[tool.pylint.messages_control]

disable = [
    "missing-function-docstring",
    "missing-class-docstring",
    "missing-module-docstring",
    "invalid-name",
    "too-few-public-methods"
]
```

or ignoring them directly in a function code eg:

```python
def test_end_to_end():
    # pylint: disable=missing-function-docstring
    response = requests.post(url=URL, json=event)
```