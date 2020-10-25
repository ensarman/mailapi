# mailapi

API for mailserver

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
```
