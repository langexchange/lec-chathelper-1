# lec-chathelper
Apache lec chathelper for lang-exchange app.

## 1. Host domain
+ Root: /app
+ Auth: /app/auth
+ Upload: /app/upload/
+ Upload: /xmpp

## Local running for coding frontend
```console
foo@bar:~$ make front
```

Then you can start to code on `src` folder inside `lec_chathelper/static` directory. The server `localhost:3003` will reload whenever your codebase changes.

## How to deploy
1. Run following command
```console
foo@bar:~$ docker run --rm --name=lec-chathelper -d --env-file=/home/ec2-user/apache.prod.env -p 80:80 -v /home/ec2-user/apache_log:/usr/local/apache2/logs -v /home/ec2-user/apache.conf:/usr/local/apache2/conf/httpd.conf:ro narutosimaha/lec-chathelper
```

Where:
+ apache.conf: is your apache configuration
2. Then generate /.well-known/host-meta for xmpp service:
```console
foo@bar:~$ docker exec lec-web /etc/nginx/script.sh
```

## Check list
- [ ] Webpack for frontend building.
- [ ] Correction message.e
- [ ] Friend integrating with webapp.
- [ ] Audio message.
- [ ] Friend arrangement.
