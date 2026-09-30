# Production deployment

This Compose setup runs the Django API with Gunicorn and connects to an external
PostgreSQL database; it does not start a database container.

1. Copy `production.env.example` to `production.env` and set a unique
   `DJANGO_SECRET_KEY`, the EC2 public DNS name or API domain in
   `DJANGO_ALLOWED_HOSTS`, the frontend origin(s), and the RDS endpoint and
   credentials. Keep `DB_SSLMODE=require` to encrypt the connection to RDS.
2. Allow inbound TCP on `HTTP_PORT` (80 by default) in the EC2 security group.
   In the RDS security group, allow inbound TCP/5432 from the EC2 security
   group. Do not expose PostgreSQL publicly.
3. From the repository root, build and start the service:

   ```sh
   docker compose --env-file docker/production.env -f docker/docker-compose.prod.yml up -d --build
   ```

   Nginx publishes the HTTP port and proxies requests to Gunicorn on the
   internal Compose network; Gunicorn is not published directly to the host.
   The backend container applies Django migrations and collects static files
   before starting Gunicorn. Check startup output with:

   ```sh
   docker compose --env-file docker/production.env -f docker/docker-compose.prod.yml logs -f backend
   ```

`production.env` contains credentials and is excluded from the Docker build
context. Keep it private and do not commit it. This configuration serves plain
HTTP through Nginx. For HTTPS, terminate TLS at an AWS load balancer or add
certificate management and an HTTPS listener to Nginx; do not send production
credentials or other sensitive data over plain HTTP.
