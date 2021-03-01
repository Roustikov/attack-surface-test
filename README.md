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
* You can browse DB structure by opening `http://127.0.0.1:7474/browser/` and logging in with `NEO4J_USERNAME` and `NEO4J_PASSWORD` from the `docker-compose.env`.
* To view DB connection graph - open `http://127.0.0.1:7474/browser/` in your web browser and enter `MATCH (n) RETURN n LIMIT 25` in the "query bar" at the top.

<details>
  <summary>View DB Structure Example</summary>
  ![DB Structure Example](../../blob/master/readme_images/db_structure.PNG)
</details>

## UNIT TESTING ##
* Since neo4j isn't a Django-coupled DB engine - we must rely on a separate DB instance running in docker container.
* Container address is located in `NEO4J_TEST_URL` inside of `docker-compose.env`.
* Tests are run as following: `python manage.py test api.tests --settings attack_surface.settings_test`

## API USAGE EXAMPLES ##
* `curl 'http://localhost/api/v1/stats'` returns service stats in `{"vm_count": 11, "request_count": 7, "average_request_time": 0.07012643046982703}` format.
* `curl 'http://localhost/api/v1/attack?vm_id=vm-a211de'` returns an array of VM ids that comprises the attack surface for `vm_id`.
