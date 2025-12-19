FROM astrocrpublic.azurecr.io/runtime:3.1-8

# Instalar dbt e adaptar o conector para o Postgres
RUN pip install dbt-core==1.9.0 dbt-postgres==1.9.0

# Instalar faker
RUN pip install faker

# Garantir que o diretório .dbt esteja dentro do container
RUN mkdir -p /home/astro/.dbt
COPY include/.dbt/profiles.yml /home/astro/.dbt/profiles.yml

USER astro