CLI commands:

CMD #1 - connect SSH:
ssh vnztech@103.159.51.249
password: Vietnam@68


CMD #2 - pull code mới về: haipb-bitrix24
cd ./haipb/app
git fetch
git pull

CMD #3: haipb-api
cd ./haipb/api
git fetch
git pull

CMD #4 - chạy docker: --> ko open port 
docker-compose down
docker-compose build
docker-compose up

CMD #4 - chạy docker:
docker-compose build
docker run -d -p 5000:5000 haipb-bitrix24 #  in background
docker run -p 5000:5000 haipb-bitrix24

CMD #5 - check logs:
docker logs -f haipb-bitrix24
docker logs -f haipb-api

API Endpoint:
https://vnztech.com:5000/
https://vnztech.com:3000/

----------------------
cmd hay dung

firewall-cmd --list-all --permanent
firewall-cmd --zone=public --add-port=80/tcp --permanent
firewall-cmd --reload
firewall-cmd --complete-reload 
firewall-cmd --zone=public --remove-interface=eth0 --permanent
firewall-cmd --zone=public --add-service=http
firewall-cmd --zone=public --add-service=https
firewall-cmd --zone=public --remove-port=80/tcp --permanent
firewall-cmd --add-masquerade
firewall-cmd --remove-masquerade

