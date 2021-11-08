# haipb-bitrix24

heroku buildpacks:set heroku/python --app haipb-bitrix24

heroku logs --app haipb-bitrix24 -t

outbound webhook
https://haipb-bitrix24.herokuapp.com/api/v1/bitrix24/webhooks/deal


# link to subcribe

https://accounts.haravan.com/connect/authorize/callback?response_mode=form_post&response_type=code id_token&scope=openid profile email org userinfo&client_id=f7dfbb2bd41e37b59a279208ec7ef783&redirect_uri=https://haipb-api.herokuapp.com/install/login&nonce=haipb1982