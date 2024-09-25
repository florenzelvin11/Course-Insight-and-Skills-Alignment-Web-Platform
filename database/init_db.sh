#!/bin/bash 
docker rm -f -v testDatabase1;
docker run -d --name testDatabase1 -v $PWD/schema:/docker-entrypoint-initdb.d -e MYSQL_ROOT_PASSWORD=password -p 3306:3306 mysql

# python3 ../backend/app/init_course.py