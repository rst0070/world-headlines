REMOTE := harbor.rst0070.com
REPOSITORY := world-headlines
IMAGE_TAG := latest
PWD := $(shell pwd)
PLATFORM := linux/amd64

login:
	docker login $(REMOTE)

build-be:
	docker build --platform=$(PLATFORM) -t $(REMOTE)/$(REPOSITORY)/backend:$(IMAGE_TAG) $(PWD)/backend

build-fe:
	docker build --platform=$(PLATFORM) -t $(REMOTE)/$(REPOSITORY)/frontend:$(IMAGE_TAG) $(PWD)/frontend

build-all: build-be build-fe

push-be:
	docker push $(REMOTE)/$(REPOSITORY)/backend:$(IMAGE_TAG)
	
push-fe:
	docker push $(REMOTE)/$(REPOSITORY)/frontend:$(IMAGE_TAG)

push-all: login push-be push-fe

build-n-push: build-all push-all

deploy:
	cd kubernetes && make upgrade