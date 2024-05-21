.DEFAULT_GOAL := up

rm-cache: stop
	find . -type f -name "*.py[co]" -delete
	find . -type d -name "__pycache__" -delete
	rm -rf .coverage
stop:
	docker-compose down --remove-orphans
build: stop
	docker-compose build
up: stop rm-cache
	docker-compose up
entry:
	docker-compose exec web /bin/bash
