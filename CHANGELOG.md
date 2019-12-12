# CHANGELOG for DevOps

## 2019/12/12

- Create Dockerfile for category_crawler and send_categories as Kubernetes Job
- Update Makefile
- Modify category_crawler env for connect mysql
- Modify send_categories env for connect mysql and rabbitmq
- Modify command ang args
- Update gitlab-auth in deployment
- Update depend_on in deployment
- Modify mysql Dockerfile
- Update category file and rebuild image

## 2019/12/10

- Add deploy file for Kubernetes
- Update Makefile
- Update fluentd Dockerfile
- Add Image fluentd:v0.0.1 for S3 ashspencil



## 2019/12/7

- Update Dockerfile and Add Makefile
- Add Image mysqldb:v0.0.1 for Initial Transfer
- Add Image product_worker:v0.0.1 for Initial Transfer
- Add Image category_worker:v0.0.1 for Initial Transfer
