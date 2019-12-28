running step:

1. run `docker-compose up --scale product_worker=5` to set up all the crawler procedure.

2. open one tmux terminal, and run `docker exec -it  everblue_mysql_1 mysql -u admin -p`, and password is `mypass`, and type `use db;`

3. copy and paste the context of create_table.sql into step2's terminal, then exit the terminal.

4. run `python category_crawler.py` to save category information into mysql

5. open another tmux terminal, and type `docker exec -it  everblue_rabbitmq_1 /bin/sh` and then type `watch rabbitmqctl list_queues name messages_ready messages_unacknowledged` to monitor the number of the messsge in the broker.

6. open another tmux terminal, and run `python send_categories.py` to sent all categories into rabbitmq, and trigger the crawler.

# ----- For Kubernetes Production -----

## Prepare your authorization for pull image

```
cat ~/.docker/config.json | base64 -w0
```

There will be base64 code, copy that and into and replace Form <your-bas364-code> in gitlab.yaml and save it. type

```
kubectl create -f gitlab-yaml
```

to create, after creating, you can check by:

```
kubectl get secrets
```

## Prepare StorageClass For EBS

```
kubectl apply -f deploy/storageclass/postgres-gp2-class.yaml
```

## Prepare Infrastructure

```
kubectl apply -f deploy/
```

And wait for all containers are running, you can check by:

```
kubectl get pods -o wide
```

## Start crawler

```
kubectl apply -f deploy/job/category-crawler-job.yaml
```

# NOTE:

##正式版本 image 對應為:

- product_worker:v0.0.3 (建議先使用vcheck)
- category_worker:v0.0.3 (建議先使用vcheck)
- write_s3_jsonfile_into_postgres_routine:v0.0.2
- shopee_crawler_routine:v0.0.2 (每天晚上六點)
- shopee_restful_api_service:v0.0.3
- category_crawler:v0.0.2
- fluentd:v0.0.4 (寫入 Ching-Yi Hung 的 s3)

##目前測試用 image 對應為:

- product_worker:vcheck (尚在除錯用, 會不定時重新建立)
- category_worker:vcheck (尚在除錯用, 會不定時重新建立)
- write_s3_jsonfile_into_postgres_routine:v0.0.2
- shopee_crawler_routine:vcheck (每天中午12點)
- shopee_restful_api_service:v0.0.3
- category_crawler:v0.0.2
- fluentd:v0.0.3 (寫入 ashspencil 的 s3)
