# Diagnosis Hub
## RESTful API for Internationally Recognized Set of Diagnosis Codes

[![N|Solid](https://cldup.com/dTxpPi9lDf.thumb.png)](https://nodesource.com/products/nsolid)

[![Build Status](https://travis-ci.org/joemccann/dillinger.svg?branch=master)](https://travis-ci.org/joemccann/dillinger)

Diagnosis Hub is a set of RESTful APIs that can allow us to utilize an internationally recognized set of diagnosis codes.

DRF-YASG-powered API Documentation.
- Visit `localhost:8001`
- See Documentation in Browser
- ✨Magic ✨

## Features
- Create a new diagnosis code record
- Edit an existing diagnosis code record
- List diagnosis codes in batches of 20 (and paginate through the rest of the record)
- Retrieve diagnosis codes by ID
- Delete a diagnosis code by ID
- Upload diagnosis ICD CSV containing diagnosis record and receive an email after processing is done

## Project Setup
Diagnosis Hub require the docker and docker-compose to run

### Unix system or unix like terminal
```sh
git clone https://github.com/horlali/diagnosis-api.git
cd diagnosis-api
touch .env
# Copy the content of the environment variable file attached to the submission email and paste into into the .env file
docker-compose up --build
```
Voilà  - The app is up and running

## Documentation
With the app running visti `localhost:8001` and interact with it.


## 
