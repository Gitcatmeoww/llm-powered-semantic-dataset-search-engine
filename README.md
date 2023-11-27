### System Overview

We use [`pagila`](https://github.com/devrimgunduz/pagila) as the sample database for the system.

### Running This System

```
docker compose up
source venv/bin/activate
pip install -r requirements.txt
python run.py
```

### Weaviate Server

Meta information about the Weaviate instance: `http://localhost:8080/v1/meta`
Check the specified classes and vectorizers: `http://localhost:8080/v1/schema`
