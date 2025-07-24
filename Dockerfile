FROM python:3.12

RUN pip install --upgrade pip \
    && pip install uv

WORKDIR /app

COPY pyproject.toml uv.lock ./
RUN uv pip install --system .

COPY . .

EXPOSE 8000

CMD ["uvicorn", "src.app.main:app", "--host", "0.0.0.0", "--port", "8000"]
