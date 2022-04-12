# test_rusdn2

Тестовое Задание Backend. Задача 2.
###login to mysql server with your root credentials, ie:<br><br>
mysql -h 127.0.0.1 -uroot -p
execute commands to setup database task2
###create database task2
CREATE DATABASE task2 DEFAULT CHARACTER SET utf8 COLLATE utf8_unicode_ci;
###create user with rights on it
CREATE USER 'task2user'@'%' IDENTIFIED BY 'task2passwd';<br>
GRANT ALL PRIVILEGES ON task2.* TO 'task2user'@'%' WITH GRANT OPTION;
FLUSH PRIVILEGES;
###schema.sql will be executed automatically upon starting the app

###to run you would probably need to set your host of mysql server ie:
python3 task2.py --db-host=192.168.1.204<br>

options are:<br>
  --db-database                    mysql database name (default task2)<br>
  --db-host                        mysql database host (default 192.168.1.204)<br>
  --db-password                    mysql task2user password (default
                                   task2passwd)<br>
  --db-port                        mysql database port (default 3306)<br>
  --db-user                        mysql database user (default task2user)<br>
  --port                           run on the given port (default 8888)<br>
