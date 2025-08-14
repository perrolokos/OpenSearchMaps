# OpenSearchMaps

Early-stage codebase for the OpenSearchMaps platform. This repository
currently includes a minimal Django backend exposing two API endpoints:

* `POST /api/search/semantic` – placeholder semantic search endpoint.
* `GET /api/map/<id>/tree` – returns a stored knowledge map structure.
* `GET /api/map/<id>/export?fmt=mermaid|gexf` – export a knowledge map as
  a Mermaid diagram or GEXF network file.

The backend defines initial models for articles, citations and related
entities to support future development.

Real-time collaboration is available via a Channels WebSocket endpoint at
`ws://<host>/ws/map/<id>/`, broadcasting messages to all clients connected to
the same map.

## Frontend development

A React/Vite frontend lives in the `frontend/` directory. It provides a
three-panel layout with article search, list and graph visualization and
uses Tailwind CSS, Zustand and React Flow.

### Running the frontend

```bash
cd frontend
npm install
npm run dev
```

### Frontend tests

```bash
npm test
```

## ELK stack for analytics and observability

The repository provides a Docker Compose setup for a local Elastic stack with
Elasticsearch, Logstash, Kibana and the APM server.

### Running the stack

```bash
docker compose up
```

This starts Elasticsearch on `localhost:9200`, Kibana on `localhost:5601`, a
Logstash pipeline that ingests articles from OpenAlex, and an APM server at
`localhost:8200`.

### Dashboards

Sample Kibana dashboards are exported in
`elk/kibana/dashboards/literature.ndjson`. Import them via Kibana's **Saved
Objects** to explore publications over time.
