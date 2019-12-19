CATEGORY_WORKER_VERSION_NUMBER ?= check #Remeber to modify version number by each time you modify this part
CATEGORY_WORKER_VERSION ?= v$(CATEGORY_WORKER_VERSION_NUMBER)
CATEGORY_WORKER_REPOPATH := category_worker

PRODUCT_WORKER_VERSION_NUMBER ?= check #Remeber to modify version number by each time you modify this part
PRODUCT_WORKER_VERSION ?= v$(PRODUCT_WORKER_VERSION_NUMBER)
PRODUCT_WORKER_REPOPATH := product_worker

#MYSQL_DB_VERSION_NUMBER ?= 0.0.2 #Remeber to modify version number by each time you modify this part
#MYSQL_DB_WORKER_VERSION ?= v$(MYSQL_DB_VERSION_NUMBER)
#MYSQL_DB_WORKER_REPOPATH := mysqldb

FLUENTD_VERSION_NUMBER ?= 0.0.4 #Remeber to modify version number by each time you modify this part
FLUENTD_VERSION ?= v$(FLUENTD_VERSION_NUMBER)
FLUENTD_REPOPATH := fluentd

CATEGORY_CRAWLER_VERSION_NUMBER ?= 0.0.2 #Remeber to modify version number by each time you modify this part
CATEGORY_CRAWLER_VERSION ?= v$(CATEGORY_CRAWLER_VERSION_NUMBER)
CATEGORY_CRAWLER_REPOPATH := category_crawler

SHOPEE_CRAWLER_ROUTINE_VERSION_NUMBER ?= check #Remeber to modify version number by each time you modify this part
SHOPEE_CRAWLER_ROUTINE_VERSION ?= v$(SHOPEE_CRAWLER_ROUTINE_VERSION_NUMBER)
SHOPEE_CRAWLER_ROUTINE_REPOPATH := shopee_crawler_routine

SHOPEE_RESTFUL_API_SERVICE_VERSION_NUMBER ?= 0.0.1 #Remeber to modify version number by each time you modify this part
SHOPEE_RESTFUL_API_SERVICE_VERSION ?= v$(SHOPEE_RESTFUL_API_SERVICE_VERSION_NUMBER)
SHOPEE_RESTFUL_API_SERVICE_REPOPATH := shopee_restful_api_service

WRITE_S3_JSONFILE_INTO_POSTGRES_ROUTINE_VERSION_NUMBER ?= 0.0.1 #Remeber to modify version number by each time you modify this part
WRITE_S3_JSONFILE_INTO_POSTGRES_ROUTINE_VERSION ?= v$(WRITE_S3_JSONFILE_INTO_POSTGRES_ROUTINE_VERSION_NUMBER)
WRITE_S3_JSONFILE_INTO_POSTGRES_ROUTINE_REPOPATH := write_s3_jsonfile_into_postgres_routine

BUILDTIME = $(shell date --rfc-3339=seconds)
COMMITID = $(shell git rev-parse HEAD)

##########

.PHONY: build_category_worker
build_category_worker:
		docker build -t registry.gitlab.com/fevemania/shopee_side_project/$(CATEGORY_WORKER_REPOPATH):$(CATEGORY_WORKER_VERSION) -f ./side_project/shopee_crawler/category_worker/Dockerfile .

.PHONY: push_category_worker
push_category_worker:
		docker push registry.gitlab.com/fevemania/shopee_side_project/$(CATEGORY_WORKER_REPOPATH):$(CATEGORY_WORKER_VERSION)

##########

.PHONY: build_product_worker
build_product_worker:
		docker build -t registry.gitlab.com/fevemania/shopee_side_project/$(PRODUCT_WORKER_REPOPATH):$(PRODUCT_WORKER_VERSION) -f ./side_project/shopee_crawler/product_worker/Dockerfile .

.PHONY: push_product_worker
push_product_worker:
		docker push registry.gitlab.com/fevemania/shopee_side_project/$(PRODUCT_WORKER_REPOPATH):$(PRODUCT_WORKER_VERSION)

##########

#.PHONY: build_mysqldb
#build_mysqldb:
#		docker build -t registry.gitlab.com/fevemania/shopee_side_project/$(MYSQL_DB_WORKER_REPOPATH):$(MYSQL_DB_WORKER_VERSION) -f ./mysqldb/Dockerfile .

#.PHONY: push_mysqldb
#push_mysqldb:
#		docker push registry.gitlab.com/fevemania/shopee_side_project/$(MYSQL_DB_WORKER_REPOPATH):$(MYSQL_DB_WORKER_VERSION)

##########

.PHONY: build_fluentd
build_fluentd:
	    docker build -t registry.gitlab.com/fevemania/shopee_side_project/$(FLUENTD_REPOPATH):$(FLUENTD_VERSION) -f ./side_project/shopee_crawler/fluentd/Dockerfile .

.PHONY: push_fluentd
push_fluentd:
		docker push registry.gitlab.com/fevemania/shopee_side_project/$(FLUENTD_REPOPATH):$(FLUENTD_VERSION)

##########

.PHONY: build_category_crawler
build_category_crawler:
		docker build -t registry.gitlab.com/fevemania/shopee_side_project/$(CATEGORY_CRAWLER_REPOPATH):$(CATEGORY_CRAWLER_VERSION) -f ./side_project/shopee_crawler/category_crawler/Dockerfile .

.PHONY: push_category_crawler
push_category_crawler:
		docker push registry.gitlab.com/fevemania/shopee_side_project/$(CATEGORY_CRAWLER_REPOPATH):$(CATEGORY_CRAWLER_VERSION)

##########

.PHONY: build_shopee_crawler_routine
build_shopee_crawler_routine:
		docker build -t registry.gitlab.com/fevemania/shopee_side_project/$(SHOPEE_CRAWLER_ROUTINE_REPOPATH):$(SHOPEE_CRAWLER_ROUTINE_VERSION) -f ./side_project/shopee_crawler/crawler_routine/Dockerfile .

.PHONY: push_shopee_crawler_routine
push_shopee_crawler_routine:
		docker push registry.gitlab.com/fevemania/shopee_side_project/$(SHOPEE_CRAWLER_ROUTINE_REPOPATH):$(SHOPEE_CRAWLER_ROUTINE_VERSION)

##########

.PHONY: build_shopee_restful_api_service
build_shopee_restful_api_service:
		docker build -t registry.gitlab.com/fevemania/shopee_side_project/$(SHOPEE_RESTFUL_API_SERVICE_REPOPATH):$(SHOPEE_RESTFUL_API_SERVICE_VERSION) -f ./side_project/restful_api/Dockerfile .

.PHONY: push_shopee_restful_api_service
push_shopee_restful_api_service:
		docker push registry.gitlab.com/fevemania/shopee_side_project/$(SHOPEE_RESTFUL_API_SERVICE_REPOPATH):$(SHOPEE_RESTFUL_API_SERVICE_VERSION)

##########

.PHONY: build_write_s3_jsonfile_into_postgres_routine
build_write_s3_jsonfile_into_postgres_routine:
		docker build -t registry.gitlab.com/fevemania/shopee_side_project/$(WRITE_S3_JSONFILE_INTO_POSTGRES_ROUTINE_REPOPATH):$(WRITE_S3_JSONFILE_INTO_POSTGRES_ROUTINE_VERSION) -f ./side_project/write_s3_jsonfile_into_postgres_routine/Dockerfile .

.PHONY: push_write_s3_jsonfile_into_postgres_routine
push_write_s3_jsonfile_into_postgres_routine:
		docker push registry.gitlab.com/fevemania/shopee_side_project/$(WRITE_S3_JSONFILE_INTO_POSTGRES_ROUTINE_REPOPATH):$(WRITE_S3_JSONFILE_INTO_POSTGRES_ROUTINE_VERSION)
