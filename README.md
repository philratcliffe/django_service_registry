# A Service Registry using Django

## Overview
A solution using Django and the Django REST Framework to demo the Service 
Registry API. This Service Registry API provides endpoints for creating,
finding, deleting, and updating services in the registry. 


## Installation
    - Ensure that you are running in a Python3 environment.
    - pip install -r requirements.txt

## Running the Django development server
```bash
$ python manage.py runserver
```

## URL format
All endpoints are prefixed by /services/<api_version_number>. For example to
find information about a service:

```
GET /services/v1/<name>
```

## Testing
Django REST framework allows the API to be browsed. Simply point your browser
at http://127.0.0.1:8000/services/v1 to get started.

You can run all the tests in the tests module using the following command:

```bash
$ python manage.py test
```

In addition, you can test the API from the command line using cURL. This 
allows you to easily investigate and test the service as shown in the examples
below.

### Add a service
```bash
$ curl -i -H "Content-Type: application/json" -X POST -d '{"service":"test1","version":"0.0.1"}' http://localhost:8000/services/v1
```

Returns:

```json
{
  "service": "test1", 
  "version": "0.0.1", 
  "change": "created" 
}
```

### Find a service
```bash
$ curl -i http://localhost:8000/services/v1/test1
```

Returns:  (if we have added test1 twice)
```json
{
  "service":"test1",
  "count":2
}
```

### Delete a service
```bash
$ curl -i -H "Content-Type: application/json" -X DELETE http://localhost:8000/services/v1/test1
```

Returns:
```json
{
  "change":"removed",
  "service":"test1"
}
```


### Update a service
```bash
$ curl -i -H "Content-Type: application/json" -X PUT -d '{"service":"test99","version":"1.1.1"}' http://localhost:8000/services/v1/1  
```

Returns:
```json
{
  "change":"changed"
}
```

### List all registered services (N.B. not in the reqs. for development only)
```bash
$ curl -i http://localhost:8000/services/v1
```

Returns:
```json
[
  {
    "service":"updatetest",
    "version":"9.0.1"
  },
  {
    "service":"test",
    "version":"0.0.1"
  },
  {
    "service":"test",
    "version":"0.0.1"
  }
]
```

## TODO

    - Improve tests
    - Improve input validation and error handling
    - Add logging
    - Add authentication and authorisation 
    - Run over TLS 
    - Improve commenting
    - Add some mechanism for reporting and checking health of services
    - Add additional fields such as the URL of the service
    - Add rate limiting
    - Remove unnecessary modules from requirements.txt
    - Update validators
