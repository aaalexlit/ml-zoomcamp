LOCAL_TAG:=$(shell date +"%Y-%m-%d-%H-%M")
LOCAL_IMAGE_NAME:=stream-model-duration:${LOCAL_TAG}

test:
	pytest tests/

quality_checks:
	isort .
	black .
	pylint --recursive=y .


integration_test: test	
	./integration-test/run.sh

build: quality_checks test
	docker build -t ${LOCAL_IMAGE_NAME} .


publish: integration_test build
	LOCAL_IMAGE_NAME=${LOCAL_IMAGE_NAME} ./scripts/publish.sh

setup:
	pipenv install --dev
	pre-commit install