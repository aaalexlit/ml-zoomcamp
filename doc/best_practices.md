1. Copy files from streaming lecture to a new folder
    From the project root

    ```shell
    cp -r kinesis/ best_practices/code 
    ```
1. Create a pipenv virtual environment

    ```shell
    pipenv install
    ```

1. Add dev dependency `pytest`
    ```shell
    pipenv install --dev pytest
    ```

1. check that it's properly installec
    ```shell
    pipenv run which pytest
    ```
1. Configure Testing tab in Visual Studio Code and select pytest