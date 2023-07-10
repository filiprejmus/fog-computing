run-cloud: 
	poetry run python cloud-server.py

run-server-one: 
	poetry run python client/sensor-device-one.py

build:
	docker buildx build --platform linux/amd64 -t fog-cloud-component .
	docker tag fog-cloud-component europe-west3-docker.pkg.dev/ardent-disk-387514/fog-computing-assignment/fog-cloud-component:latest
	docker push europe-west3-docker.pkg.dev/ardent-disk-387514/fog-computing-assignment/fog-cloud-component:latest



