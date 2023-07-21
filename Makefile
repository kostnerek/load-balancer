default: 
	start-headless

run:
	python3 compose.py ${replicas}
	docker-compose build
	docker-compose up

run-headless:
	python3 compose.py ${replicas}
	docker-compose build
	docker-compose up -d

start: 
	docker-compose up

start-headless: 
	docker-compose up -d

build:
	docker-compose build

compose:
	python3 compose.py ${replicas}

load-test:
	python3 load_test.py