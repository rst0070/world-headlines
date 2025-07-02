REMOTE := harbor.rst0070.com
REPOSITORY := world-headlines/gnews-crawling
IMAGE_TAG := latest

login:
	docker login $(REMOTE)

build:
	docker build --platform linux/amd64 -t $(REMOTE)/$(REPOSITORY):$(IMAGE_TAG) .

push:
	docker push $(REMOTE)/$(REPOSITORY):$(IMAGE_TAG)

all: login build push
