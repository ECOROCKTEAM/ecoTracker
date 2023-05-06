FROM python:3.10 as builder

WORKDIR /app

RUN python3 -m venv /venv
ENV PATH="/venv/bin:$PATH"

RUN pip install --upgrade pip

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY . .


FROM python:3.10 as test_runner
WORKDIR /app
COPY --from=builder /venv /venv
COPY --from=builder /app .
ENV PATH="/venv/bin:$PATH"

COPY requirements-test.txt ./
RUN pip install -r requirements-test.txt

CMD ["python", "-m", "pytest", "tests/", "-v", "-s"]