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

CMD #4 - chạy docker:
docker-compose down
docker-compose build
docker-compose up

CMD #5 - check logs:
docker logs -f haipb-bitrix24
docker logs -f haipb-api

API Endpoint:
https://vnztech.com:5000/
https://vnztech.com:3000/