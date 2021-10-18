#!/bin/bash


#pre-requisites
#SAM CLI - [Install the SAM CLI](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-sam-cli-install.html)
#[Python 3 installed](https://www.python.org/downloads/)
#Docker - [Install Docker community edition](https://hub.docker.com/search/?type=edition&offering=community)

sam build --use-container 

sam deploy --capabilities CAPABILITY_NAMED_IAM