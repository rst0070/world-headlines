FROM python:3.13-slim

ENV TZ=Asia/Seoul
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# install infisical cli
RUN apt-get update && apt-get install -y \
    curl \
    && curl -1sLf 'https://artifacts-cli.infisical.com/setup.deb.sh' | bash \
    && apt-get update && apt-get install -y infisical \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir poetry && \
    poetry config virtualenvs.create false && \
    poetry install --no-cache --no-root && \
    poetry run playwright install chromium --with-deps --only-shell && \
    rm -rf /var/lib/apt/lists/*

CMD infisical run \
    --token="${INFISICAL_TOKEN}" \
    --env="${INFISICAL_ENVIRONMENT}" \
    --projectId="${INFISICAL_PROJECT_ID}" \
    --domain="${INFISICAL_HOST}" \
    -- \
    poetry run python -m src.etl
