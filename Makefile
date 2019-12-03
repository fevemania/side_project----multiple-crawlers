CATEGORY_WORKER_VERSION_NUMBER ?= 0.0.1 #Remeber to modify version number by each time
CATEGORY_WORKER_VERSION ?= v$(CATEGORY_WORKER_VERSION_NUMBER)
CATEGORY_WORKER_REPOPATH := category_worker

PRODUCT_WORKER_VERSION_NUMBER ?= 0.0.1 #Remeber to modify version number by each time
PRODUCT_WORKER_VERSION ?= v$(PRODUCT_WORKER_VERSION_NUMBER)
PRODUCT_WORKER_REPOPATH := product_worker


BUILDTIME = $(shell date --rfc-3339=seconds)
COMMITID = $(shell git rev-parse HEAD)

.PHONY: build_category_worker
build_category_worker:
		docker build -t registry.gitlab.com/fevemania/$(CATEGORY_WORKER_REPOPATH):$(CATEGORY_WORKER_VERSION) -f ./conf/category_worker/Dockerfile .

.PHONY: build_product_worker
build_product_worker:
		docker build -t registry.gitlab.com/fevemania/$(PRODUCT_WORKER_REPOPATH):$(PRODUCT_WORKER_VERSION) -f ./conf/product_worker/Dockerfile .
