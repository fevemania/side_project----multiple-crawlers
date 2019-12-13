CATEGORY_WORKER_VERSION_NUMBER ?= 0.0.2 #Remeber to modify version number by each time you modify this part
CATEGORY_WORKER_VERSION ?= v$(CATEGORY_WORKER_VERSION_NUMBER)
CATEGORY_WORKER_REPOPATH := category_worker

PRODUCT_WORKER_VERSION_NUMBER ?= 0.0.2 #Remeber to modify version number by each time you modify this part
PRODUCT_WORKER_VERSION ?= v$(PRODUCT_WORKER_VERSION_NUMBER)
PRODUCT_WORKER_REPOPATH := product_worker

MYSQL_DB_VERSION_NUMBER ?= 0.0.2 #Remeber to modify version number by each time you modify this part
MYSQL_DB_WORKER_VERSION ?= v$(MYSQL_DB_VERSION_NUMBER)
MYSQL_DB_WORKER_REPOPATH := mysqldb

FLUENTD_VERSION_NUMBER ?= 0.0.3 #Remeber to modify version number by each time you modify this part
FLUENTD_VERSION ?= v$(FLUENTD_VERSION_NUMBER)
FLUENTD_REPOPATH := fluentd

CATEGORY_CRAWLER_VERSION_NUMBER ?= 0.0.1 #Remeber to modify version number by each time you modify this part
CATEGORY_CRAWLER_VERSION ?= v$(CATEGORY_CRAWLER_VERSION_NUMBER)
CATEGORY_CRAWLER_REPOPATH := category_crawler

SEND_CATEGORIES_VERSION_NUMBER ?= 0.0.1
SEND_CATEGORIES_VERSION ?= v$(SEND_CATEGORIES_VERSION_NUMBER)
SEND_CATEGORIES_REPOPATH := send_categories

BUILDTIME = $(shell date --rfc-3339=seconds)
COMMITID = $(shell git rev-parse HEAD)

.PHONY: build_category_worker
build_category_worker:
		docker build -t registry.gitlab.com/fevemania/shopee_side_project/$(CATEGORY_WORKER_REPOPATH):$(CATEGORY_WORKER_VERSION) -f ./conf/category_worker/Dockerfile .

.PHONY: push_category_worker
push_category_worker:
		docker push registry.gitlab.com/fevemania/shopee_side_project/$(CATEGORY_WORKER_REPOPATH):$(CATEGORY_WORKER_VERSION)

#####

.PHONY: build_product_worker
build_product_worker:
		docker build -t registry.gitlab.com/fevemania/shopee_side_project/$(PRODUCT_WORKER_REPOPATH):$(PRODUCT_WORKER_VERSION) -f ./conf/product_worker/Dockerfile .

.PHONY: push_product_worker
push_product_worker:
		docker push registry.gitlab.com/fevemania/shopee_side_project/$(PRODUCT_WORKER_REPOPATH):$(PRODUCT_WORKER_VERSION)

#####

.PHONY: build_mysqldb
build_mysqldb:
		docker build -t registry.gitlab.com/fevemania/shopee_side_project/$(MYSQL_DB_WORKER_REPOPATH):$(MYSQL_DB_WORKER_VERSION) -f ./mysqldb/Dockerfile .

.PHONY: push_mysqldb
push_mysqldb:
		docker push registry.gitlab.com/fevemania/shopee_side_project/$(MYSQL_DB_WORKER_REPOPATH):$(MYSQL_DB_WORKER_VERSION)

#####

.PHONY: build_fluentd
build_fluentd:
	    docker build -t registry.gitlab.com/fevemania/shopee_side_project/$(FLUENTD_REPOPATH):$(FLUENTD_VERSION) -f ./conf/fluentd/Dockerfile .

.PHONY: push_fluentd
push_fluentd:
		docker push registry.gitlab.com/fevemania/shopee_side_project/$(FLUENTD_REPOPATH):$(FLUENTD_VERSION)

#####

.PHONY: build_category_crawler
build_category_crawler:
		docker build -t registry.gitlab.com/fevemania/shopee_side_project/$(CATEGORY_CRAWLER_REPOPATH):$(CATEGORY_CRAWLER_VERSION) -f ./category/Dockerfile_category_crawler .

.PHONY: push_category_crawler
push_category_crawler:
		docker push registry.gitlab.com/fevemania/shopee_side_project/$(CATEGORY_CRAWLER_REPOPATH):$(CATEGORY_CRAWLER_VERSION)

#####

.PHONY: build_send_categories
build_send_categories:
		docker build -t registry.gitlab.com/fevemania/shopee_side_project/$(SEND_CATEGORIES_REPOPATH):$(SEND_CATEGORIES_VERSION) -f ./category/Dockerfile_send_categories .

.PHONY: push_send_categories
push_send_categories:
		docker push registry.gitlab.com/fevemania/shopee_side_project/$(SEND_CATEGORIES_REPOPATH):$(SEND_CATEGORIES_VERSION)
