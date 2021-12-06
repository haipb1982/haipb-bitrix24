CREATE USER 'haipb'@'localhost' IDENTIFIED BY 'Vietnam@68';
CREATE USER 'haipb'@'%' IDENTIFIED BY 'Vietnam@68';
GRANT ALL ON *.* TO 'haipb'@'localhost';
GRANT ALL ON *.* TO 'haipb'@'%';
FLUSH PRIVILEGES; 