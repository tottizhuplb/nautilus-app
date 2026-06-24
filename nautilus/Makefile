COMPOSE_BASE = docker compose -f ../docker-compose.yml
COMPOSE_DEV  = $(COMPOSE_BASE) -f ../docker-compose.dev.yml
COMPOSE_PROD = $(COMPOSE_BASE) -f ../docker-compose.prod.yml

.PHONY: dev-up dev-down dev-shell prod-up prod-down live smoke redis-ping ib-ping

dev-up:
	$(COMPOSE_DEV) up -d

dev-down:
	$(COMPOSE_DEV) down

dev-shell:
	docker exec -it nautilus bash

prod-up:
	$(COMPOSE_PROD) up -d --build

prod-down:
	$(COMPOSE_PROD) down

live:
	python -m app.run_live

smoke:
	python -m app.smoke

redis-ping:
	python -c "import os,redis; r=redis.Redis(host=os.environ.get('REDIS_HOST','redis'), port=int(os.environ.get('REDIS_PORT','6379'))); print(r.ping())"

ib-ping:
	python -c "import os,socket; h=os.environ.get('IB_HOST','ib-gateway'); p=int(os.environ.get('IB_PORT','4003')); s=socket.create_connection((h,p),5); s.close(); print(f'OK {h}:{p}')"
