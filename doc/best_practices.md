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

1. The following env vars need to be exported

    ```bash
    export RUN_ID=a4b217a84e3a44ad870271b75331eb6c
    export TEST_RUN=True
    ```

1. Build docker image from [Dockerfile](../best_practices/code/Dockerfile)
    ```bash
    docker build -t stream-model-duration:v2 .
    ```

1. Run the built docker image
    ```bash
    docker run -it --rm \
    -p 8080:8080 \
    -e PREDICTIONS_STREAM_NAME="ride-predictions" \
    -e RUN_ID="a4b217a84e3a44ad870271b75331eb6c" \
    -e TEST_RUN="True" \
    -v ~/.aws:/root/.aws \
    stream-model-duration:v2    
    ```

1. Run tests from CLI

    ```shell
    pipenv run pytest tests/