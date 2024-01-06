FROM python:3.10-alpine as builder

WORKDIR /app

RUN python3 -m venv /venv
ENV PATH="/venv/bin:$PATH"

RUN pip install --upgrade pip
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY ./src ./src


FROM python:3.10-alpine as test_runner
WORKDIR /app
COPY --from=builder /venv /venv
COPY --from=builder /app .
ENV PATH="/venv/bin:$PATH"

COPY requirements.txt ./
RUN pip install -r requirements.txt
COPY . .

ENTRYPOINT pytest tests/main -v -x