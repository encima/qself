# qself
An exercise in actually doing stuff with the mass data I collect.

Sadly, Twitter is a real stickler for the order it needs the auth headers in and thus Python 3.6 is required. There are other ways to maintain the order of a dictionary, of course.

## Config 

Each service you want to analyse is an entry in the `ini` file with the following structure:
```
[SERVICE]
CLIENT_ID=
CLIENT_SECRET=
REDIRECT=
REQUEST_URL=https://api.twitter.com/oauth/request_token
AUTH_URL=https://api.twitter.com/oauth/authenticate
TOKEN_URL=https://api.twitter.com/oauth/access_token
API_URL=https://api.twitter.com/1.1
```

## TODO

* Document all options for config file and services
