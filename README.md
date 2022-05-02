# Diagnosis Hub
## RESTful API for Internationally Recognized Set of Diagnosis Codes

### Welcome to my little spacetime continium

[![Build Status](https://travis-ci.org/joemccann/dillinger.svg?branch=master)](https://linkedin.com/in/gideon-ahiadzi)

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
# Copy the content of the environment variable file attached to the 
# submission email and paste into into the .env file
docker-compose up --build
```
Alternatively you can request access to the environment variables [here](https://docs.google.com/document/d/1Fr33uDpNXEdXYVFOWYxVLImdyDc7lRlDUlBry1FiDhc/edit)

Voilà ✨✨ - The app is up and running

### Windows system
```sh
git clone https://github.com/horlali/diagnosis-api.git
cd diagnosis-api
# Create a .env file in the diagnosis-api folder
# Copy the content of the environment variable file attached to the 
# submission email and paste into into the .env file
docker-compose up --build
```
Alternatively you can request access to the environment variables [here](https://docs.google.com/document/d/1Fr33uDpNXEdXYVFOWYxVLImdyDc7lRlDUlBry1FiDhc/edit)

Voilà ✨✨ - The app is up and running

## Documentation
With the app running visit `localhost:8001` in your browser to view documentation and interact with it.


## Inspect Database
Inspecting the database require the pgadmin installed.
- Open pgadmin
- Register a new server
- Choose a name for the server
- Click the `Connection` Tab
    - Host = `localhost`
    - Port = `5432`
    - Maintenance database = `postgres`
    - Username = `postgres`
    - Password = `postgres`
- Click `Save`

Voilà ✨✨ - You can now inspect the database