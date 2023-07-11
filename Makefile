run-cloud: 
	poetry run python cloud/cloud-server.py

run-server-one: 
	poetry run python client/sensor-device-one.py --ip=$(ip)

run-server-two:
	poetry run python client/sensor-device-one.py --id=2 --ip=$(ip)

build:
	docker buildx build --platform linux/amd64 -t fog-cloud-component .
	docker tag fog-cloud-component europe-west3-docker.pkg.dev/ardent-disk-387514/fog-computing-assignment/fog-cloud-component:latest
	docker push europe-west3-docker.pkg.dev/ardent-disk-387514/fog-computing-assignment/fog-cloud-component:latest

build-local:
	docker buildx build -t fog-cloud-component .

run-local: build-local
	docker run -d --rm -p 5700:5700 fog-cloud-component




