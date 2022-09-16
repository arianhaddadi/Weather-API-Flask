# Weather API

## Introduction
This Project is a back-end implementation of a website in which users can signup and get the weather information of the place they live in.
The Framework used in this project is [Flask](https://github.com/pallets/flask/).

## Documentation

### Signing Up
* Method: `POST`
* Endpoint: `/user`
* Body: 
    * username
    * password
    * country
    * province
    * city

### Logging In
* Method: `POST`
* Endpoint: `/login`
* Body: 
    * username
    * password
* Response contains token used for authorization of further requests


### Updating The Location
* Method: `PUT`
* Endpoint: `/user?username=<username>`
* Header must include Authorization Bearer with the generated token during login.
* Body[Optional]: 
    * country
    * province
    * country

### Getting Weather Info
* Method: `GET`
* Endpoint: `/weather?username=<username>`
* Header must include Authorization Bearer with the generated token during login.

### Deleting The User
* Method: `DELETE`
* Endpoint: `/user?username=<username>`
* Header must include Authorization Bearer with the generated token during login.