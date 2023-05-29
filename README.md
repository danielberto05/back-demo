# Back Demo

Testar localemente

```bash
docker build -t back-demo:latest && \
docker run -t -p 8080:8000 \
	--env PUB_SUB_TOPIC=notify-client-topic \
	--env GOOGLE_APPLICATION_CREDENTIALS=./credentials/credentials.json \
	back-demo:latest

```
