.PHONY: build clean

IMAGE_NAME ?= sugar-optimizer
VERSION := $(shell cat VERSION)

build:
	docker build -t $(IMAGE_NAME):$(VERSION) .

run:
	docker run -it $(IMAGE_NAME):$(VERSION)

