FROM python:3.12-slim

WORKDIR /app

COPY pyproject.toml README.md ./
COPY src ./src
RUN pip install --no-cache-dir -e ".[dev]"

COPY data ./data
COPY tests ./tests
COPY results ./results

ENTRYPOINT ["python", "-m", "agentic_rag_eval.bench"]
