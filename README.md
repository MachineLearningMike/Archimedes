# Fast API
## How to run
### Requirements
- Install virtual environment
```
py -m venv .venv
```
- Activate virtual environment
```
.venv\scripts\activate
```
- Install dependencies
```
pip install -r requirements.txt
```
### Run locally
- Run app
```
uvicorn app:app --host 0.0.0.0 --port 8000 --reload
```
- Test app
```
curl -X 'GET' \
  'http://127.0.0.1:8000/?id=1&name=2' \
  -H 'accept: application/json'
```
```
curl -X 'POST' \
  'http://127.0.0.1:8000/' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "id": 0,
  "name": "string"
}'
```

### Run by Using Docker
- Build docker image
```
docker build -t <docker_hub_username>/<image_name> .
```
- Run
```
docker run -d -p 8000:8000 --name <container_name> <docker_hub_username>/<image_name>
```
- Start
```
docker start <container_name>
```
- Stop
```
docker stop <contanier_name>
```
- Push
```
docker login
```
```
docker push <docker_humb_username>/<image_name>
```

## Check docs
- After running app, navigate http://localhost:8080/docs

## Docker image url
`docker.io/<docker_hub_username>/<image_name>`
