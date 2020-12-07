# AN-webhooks
Serverless endpoint for Action Network webhooks.

When a new SURJ Bay Area member fills out the Intro Meeting Commitment form and expresses interest in joining one or more committees,
this endpoint sends an email to the committee(s) to notify them about the new member.

## Getting started

Install [Serverless](https://www.serverless.com/framework/docs/providers/aws/guide/installation/):
```
$ npm install -g serverless
```
Install python dependencies:
```
$ virtualenv env
$ source env/bin/activate
$ pip install -r requirements.txt
```

## Deploying

(requires AWS credentials)
```
$ serverless deploy -v
```

## Viewing logs

```
$ serverless logs -f an_webhook
```
