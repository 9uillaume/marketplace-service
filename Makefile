USER_ID := $(shell id -u)
GROUP_ID := $(shell id -g)

dev-env:
	@if [ "$(shell docker image inspect --format='exists' marketplace_webapp:dev)" != "exists" ]; then docker-compose build --build-arg USER_ID=${USER_ID} --build-arg GROUP_ID=${GROUP_ID} webapp; fi;
	@if [ ! -d "webapp/__pypackages__" ]; then docker run --rm -v $(PWD)/webapp:/app marketplace_webapp:dev bash -c 'pdm install && pdm install --group dev'; fi;

up: dev-env
	docker-compose up

bash: dev-env
	docker-compose run --rm webapp bash
	docker-compose down

down:
	docker-compose down

test: dev-env
	docker-compose run --rm webapp pdm run python manage.py test --settings=settings.testing
	docker-compose down

rm:
	docker rmi -f marketplace_webapp:dev || true
	rm -rf webapp/__pypackages__/ || true

build:
	@if [ -z ${VERSION} ]; then echo Usage: make build VERSION=0.0.0 && exit 1; fi;

	echo "Building dev image"
	docker-compose build --build-arg USER_ID=${USER_ID} --build-arg GROUP_ID=${GROUP_ID}

	echo "Creating an optimised build for marketplace ${VERSION}"
	docker build --file webapp/production.Dockerfile --tag marketplace_webapp:${VERSION} webapp

push:
	@if [ -z ${VERSION} ]; then echo Usage: make push VERSION=0.0.0 && exit 1; fi;

	echo "Tagging and pushing marketplace webapp ${VERSION}"
	docker tag marketplace_webapp:${VERSION} ghcr.io/mnako/marketplace/marketplace_webapp:${VERSION}
	docker push ghcr.io/mnako/marketplace/marketplace_webapp
	docker rmi marketplace_webapp:${VERSION}

.PHONY: dev-image up bash down test rm build push
