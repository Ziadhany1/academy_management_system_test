# pull official Postgres image
FROM postgres:15

# switch to bash shell
SHELL ["/bin/bash", "-c"]

# Optional: add an odoo user inside the container (not strictly needed)
RUN useradd -m -s /bin/bash odoo
