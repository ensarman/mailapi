# mailapi

API for mailserver

## Prepare dovecot to accept http requests

create a file in /etc/dovecot/conf.d/10-doveadm.conf

```dovecot
doveadm_password = [some_password]
doveadm_api_key = [some_api_key]
service doveadm {
   inet_listener http {
      port = 8191
      #ssl = yes # uncomment to enable https
   }
}
```

## Preparing sensible data

create a file _secret.py_ in the projet directory _/ispmailadmin_ and put the sensible variables

```python
SECRET_KEY = 'some generated secret key'
DATABASES = {
    'default': {
         'ENGINE': 'django.db.backends.mysql',
         'HOST: "some_host",
         'NAME': 'some_database',
         'USER': 'some_username',
         'PASSWORD': 'some_password',
    }
}
DOVECOT_HTTP = {
    'url': 'http://localhost:8191/doveadm/v1',
    'user': 'doveadm',
    'password': 'some_password or None',
    'apiKey': 'some_api_key or None'
}
```

## if your tables from ispmail already exists

you must fake some migrations then migrate all next migrations

```bash
$python manage.py migrate virtual 0001 --fake
$python manage.py migrate
```
