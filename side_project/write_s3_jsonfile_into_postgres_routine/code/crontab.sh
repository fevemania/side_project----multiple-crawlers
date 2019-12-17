#!/bin/bash

cd /mnt
source /mnt/.env ## source env變數
/usr/local/bin/python /mnt/write_s3_jsonfile_into_postgres.py
