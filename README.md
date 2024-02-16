## Detection of Ideal Behaviors with Low Impact in Github Repositories


Sometimes in order to ensure that all team members are contributing effectively, managers will place goals or expectations on Git participation on a sprint by sprint basis. However, 
bad actors will search for ways to meet these objectives without actually performing any work. These people will have ideal metrics, but little or no actual impact on the contents
of the repository. Such behavior is difficult for a manager to detect, and can take a lot of time to investigate. This project aims to create a prototype of a system
which can automatically scan a repository for such behavior and raise an alert for the manager to investigate.

## How to install Librararies:
```
pip install -r requirements.txt
```

## How to run
``` 
make run 
```
OR
```
python -m uvicorn main:app --reload
```

## How to use API
```
curl -X 'POST' \
  'http://127.0.0.1:8000/gitbehaviors' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "repository_owner": "string",
  "repository_name": "string",
  "git_access_token": "string"
}'
```