SHELL := /bin/bash

include .env

env:
	python3 -m venv env

delete_env:
	rm -r env

install:
	pip install --upgrade pip
	pip install -r requirements.txt

set-project:
	gcloud config set project ${PROJECT_ID}

deploy:
	gcloud builds submit --substitutions=_SERVICE_NAME=${SERVICE_NAME},_TASKS=${TASKS_CONTENT},_TASK_OFFSET=${TASK_OFFSET}

deploy-titles:
	gcloud builds submit --substitutions=_SERVICE_NAME=${SERVICE_NAME_TITLES},_TASKS=${TASKS_TITLES}
