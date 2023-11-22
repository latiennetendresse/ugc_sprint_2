create_network:
	docker network create shared_network
recreate_project:
	docker-compose -f docker-compose.yaml up  --build --force-recreate
