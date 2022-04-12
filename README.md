# test_rusdn2

Тестовое Задание Backend. Задача 2.<br>
###login to mysql server with your root credentials, ie:<br>
mysql -h 127.0.0.1 -uroot -p<br>
execute commands to setup database task2<br>
###create database task2<br>
CREATE DATABASE task2 DEFAULT CHARACTER SET utf8 COLLATE utf8_unicode_ci;<br>
###create user with rights on it<br>
CREATE USER 'task2user'@'%' IDENTIFIED BY 'task2passwd';<br>
GRANT ALL PRIVILEGES ON task2.* TO 'task2user'@'%' WITH GRANT OPTION;<br>
FLUSH PRIVILEGES;<br>
###schema.sql will be executed automatically upon starting the app<br>

###to run you would probably need to set your host of mysql server ie:<br>
python3 task2.py --db-host=192.168.1.204<br>

options are:<br>
  --db-database                    mysql database name (default task2)<br>
  --db-host                        mysql database host (default 192.168.1.204)<br>
  --db-password                    mysql task2user password (default
                                   task2passwd)<br>
  --db-port                        mysql database port (default 3306)<br>
  --db-user                        mysql database user (default task2user)<br>
  --port                           run on the given port (default 8888)<br>
