# uptime-kuma-ssl-check

This is a tiny python project that can be used to check the SSL certificate expiry on a given `HOST`:`PORT` combination.
The result will be pushed to the provided `UPTIME_KUMA_PUSH_URL`.

If the remaining validity is less than `MINIMUM_VALIDITY_DAYS` the published status will be `down`, `up` otherwise.
The message will always be `SSL Expiry for {host}:{port} is in {days_left} days`.

## Create Docker image
```bash
docker build -t uptime-kuma-ssl-check .
```

## Run Docker image
```bash
docker run --rm \
    -e HOST=smtp.example.com \
    -e PORT=465 \
    -e MINIMUM_VALIDITY_DAYS=30 \
    -e UPTIME_KUMA_PUSH_URL=https://uptime-kuma.example.com/api/push/{PUSH_TOKEN} \
    uptime-kuma-ssl-check
```