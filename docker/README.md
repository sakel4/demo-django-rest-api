# Production deployment

This Compose setup runs the Django API with Gunicorn and connects to an external
PostgreSQL database; it does not start a database container.

1. Copy `production.env.example` to `production.env` and set a unique
   `DJANGO_SECRET_KEY`, the EC2 public DNS name or API domain in
   `DJANGO_ALLOWED_HOSTS`, the frontend origin(s), and the RDS endpoint and
   credentials. Keep `DB_SSLMODE=require` to encrypt the connection to RDS.
2. Allow inbound TCP on `APP_PORT` (8000 by default) in the EC2 security group.
   In the RDS security group, allow inbound TCP/5432 from the EC2 security
   group. Do not expose PostgreSQL publicly.
3. From the repository root, build and start the service:

   ```sh
   docker compose --env-file docker/production.env -f docker/docker-compose.prod.yml up -d --build
   ```

   The container applies Django migrations and collects static files before
   starting Gunicorn. Check startup output with:

   ```sh
   docker compose --env-file docker/production.env -f docker/docker-compose.prod.yml logs -f backend
   ```

`production.env` contains credentials and is excluded from the Docker build
context. Keep it private and do not commit it. The EC2 instance's open port
allows HTTP traffic directly to Gunicorn; use a TLS-terminating proxy or load
balancer before serving production traffic over HTTPS.
