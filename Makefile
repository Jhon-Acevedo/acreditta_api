imageName=test-acreditta
containerName=test-acreditta

build:

	docker build -t $(imageName) -f Dockerfile .

run:

	docker-compose build
	docker-compose down
	docker-compose up -d

remove:

	docker-compose down

logs:

	docker-compose logs -f