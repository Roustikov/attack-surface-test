## ABOUT ##
This is a Django test app for a certain Cloud Security company.
The main goal of this service is to allow you to check for possible attack surfaces in your cloud environment.

## TECH STACK ##
The project consists of two Docker containers linked via `docker-compose.yml`
* `app` - The main service is a vanilla Django api
* `vm_db` - The DB is operated by neo4j graph database
All environment variables and essential settings are located in `docker-compose.env`

## USAGE ##
* Place data files in .json format in `./json_data` directory.
* Set the json file location by altering the `JSON_DATA_PATH` variable in `docker-compose.env`.
* Run the containers by calling `docker-compose up -d`
* Check your VM id for possible attack surface by calling `http://localhost/api/v1/attack?vm_id=vm-a211de`
* Then you can call `http://localhost/api/v1/stats` to view service stats.

## API USAGE EXAMPLES ##
* `curl 'http://localhost/api/v1/stats'` returns service stats in `{"vm_count": 11, "request_count": 7, "average_request_time": 0.07012643046982703}` format.
* `curl 'http://localhost/api/v1/attack?vm_id=vm-a211de'` returns an array of VM ids that comprises the attack surface for `vm_id`.