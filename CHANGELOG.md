# CHANGELOG for DevOps

## 2019/12/27
- Merge code Commit 90ec2fd1

## 2019/12/19
- Fix Bugs of crawler_routine
- Add category_worker 'check' version image for debug
- Add product_worker 'check' version image for debug
## 2019/12/18
- Merge code Commit 8e357259
- Merge code Commit 03e7f349
- Merge code Commit f1fe248d
- Update all deployment and service file
- Update Makefile
- Convert Deployment category_crawler to Job

## 2019/12/17
- Merge code until Commit 7510966e

## 2019/12/13
- Merge code until Commit 784431fd
- Add gitlab-auth.yaml
- Update README.md for Kubernetes

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
