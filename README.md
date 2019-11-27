running step:

1. run `docker-compose up --scale product_worker=5` to set up all the crawler procedure.

2. open one tmux terminal, and run `docker exec -it  everblue_mysql_1 mysql -u admin -p`, and password is `mypass`, and type `use db;`

3. copy and paste the context of create_table.sql into step2's terminal, then exit the terminal.

4. run `python category_crawler.py` to save category information into mysql

5. open another tmux terminal, and type `docker exec -it  everblue_rabbitmq_1 /bin/sh` and then type `watch rabbitmqctl list_queues name messages_ready messages_unacknowledged` to monitor the number of the messsge in the broker.

6. open another tmux terminal, and run `python send_categories.py` to sent all categories into rabbitmq, and trigger the crawler.


