running step:

1. run `docker-compose up`

2. open one tmux terminal, and run `docker exec -it  everblue_mysql_1 mysql -u admin -p`, and password is `mypass`

3. copy and paste the context of create table into step2's terminal

4. run `python category_crawler.py` to save category information into mysql

5. run `python send_categories.py` to second all categories into rabbitmq

6. run `python category_worker.py` to extract all urls in each category and put into rabbitmq

