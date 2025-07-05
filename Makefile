REMOTE := harbor.rst0070.com
REPOSITORY := world-headlines
IMAGE_TAG := latest
PWD := $(shell pwd)
PLATFORM := linux/arm64

login:
	docker login $(REMOTE)

build-be:
	docker build --platform=$(PLATFORM) -t $(REMOTE)/$(REPOSITORY)/backend:$(IMAGE_TAG) $(PWD)/backend

build-fe:
	docker build --platform=$(PLATFORM) -t $(REMOTE)/$(REPOSITORY)/frontend:$(IMAGE_TAG) $(PWD)/frontend_web

build-all: build-be build-fe

push-be:
	docker push $(REMOTE)/$(REPOSITORY)/backend:$(IMAGE_TAG)
	
push-fe:
	docker push $(REMOTE)/$(REPOSITORY)/frontend:$(IMAGE_TAG)

push-all: login push-be push-fe

build-n-push: build-all push-all

deploy-all:
	helm upgrade --install world-headlines \
		$(PWD)/helm/world-headlines \
		--namespace world-headlines \
		--create-namespace \
		--set image.tag=$(IMAGE_TAG) \
		--set image.repository=$(REMOTE)/$(REPOSITORY)