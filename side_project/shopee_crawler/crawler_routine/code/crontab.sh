#!/bin/bash

cd /mnt
source /mnt/.env ## source env變數
/usr/local/bin/python /mnt/send_categories.py
<<<<<<< HEAD

#echo "1"
#echo $RABBITMQ_USER ##因為在crontab的 shell, 為空
#echo "============="
#
#echo "2"
#source /mnt/.env ## source env變數
#echo $RABBITMQ_USER ## 所以輸出test
#echo "============="
#
#echo "3"
#export TEST="test2" ## 在crontab裡重新export
#echo $RABBITMQ_USER ##輸出test2
=======
>>>>>>> dev_devops_test
