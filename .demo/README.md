Demo data
=

This demo data may be set up in one of two ways. Either by using the docker compose file attached and self-hosting databases in a data centre and region of your choice, or by using cloud services.

Docker
-
Using Docker, you will be able to set up all databases provided with all data ready to go virtually instantly.

On a server that you own/operate, run `docker compose up` in the `.demo` directory.

You should then set your environment variables for each of the databases to the correct IP/DNS associated with the server you run. The environment variables in question are found in the `base.envfile.yaml` file.

If it is preferred to use cloud services, then the following may be used.

Clickhouse Cloud
-
Set up an account on [Clickhouse Cloud](https://clickhouse.cloud/), then create a service: ideally on GCP in your closest region.

Once the service is up, click on connect to retrieve connection information and select 'Native'.

```
# Install clickhouse client
brew install clickhouse

# Connect via command line, set up tables, and insert data
clickhouse client --host abcdefg.ap-southeast-2.aws.clickhouse.cloud --secure --password 'abCDefGH1_' --multiquery < data/clickhouse/clickhouse.sql
```

Mongo Atlas
-
Set up an account on [Mongo](https://cloud.mongodb.com/) and create a new deployment ideally on GCP in your closest region.

Once the deployment is complete, navigate to 'Network Access' and add `0.0.0.0/0` to allow all to Atlas.

Navigate to the database that's been deployed and click connect to retrieve connection details.

```
# Install mongo client
brew install mongosh

# Connect to Mongo, set up the collection and validation schema, then insert data
mongosh mongodb+srv://username:password@cluster0.abcdef.mongodb.net < data/mongo/init-mongo.js
```

AWS Aurora / GCP Cloud SQL
-
Set up your instance,

