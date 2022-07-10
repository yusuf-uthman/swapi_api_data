### Airflow Setup

1. Create a new sub-directory called `airflow` in your `project` dir (such as the one we're currently in)

2. **Set the Airflow user**:

    On Linux, the quick-start needs to know your host user-id and needs to have group id set to 0. 
    Otherwise the files created in `dags`, `logs` and `plugins` will be created with root user. 
    You have to make sure to configure them for the docker-compose:

    ```bash
    mkdir -p ./dags ./logs ./plugins
    echo -e "AIRFLOW_UID=$(id -u)" > .env
    ```

    On Windows you will probably also need it. If you use MINGW/GitBash, execute the same command. 

    To get rid of the warning ("AIRFLOW_UID is not set"), you can create `.env` file with
    this content:

    ```
    AIRFLOW_UID=50000
    ```

3. **Docker Build**:

    When you want to run Airflow locally, you might want to use an extended image, 
    containing some additional dependencies - for example you might add new python packages, 
    or upgrade airflow providers to a later version.
    
    Create a `Dockerfile` pointing to Airflow version you've just downloaded, 
    such as `apache/airflow:2.2.3`, as the base image,
       
    And customize this `Dockerfile` by:
    * Also, integrating `requirements.txt` to install libraries via  `pip install`

   
4. **Import the official docker setup file** from the latest Airflow version:
   ```shell
   curl -LfO 'https://airflow.apache.org/docs/apache-airflow/stable/docker-compose.yaml'
   ```
   

7. **Docker Compose**:

    Back in your `docker-compose.yaml`:
   * In `x-airflow-common`: 
     * Remove the `image` tag, to replace it with your `build` from your Dockerfile, as shown
     * Mount your `pipeline` in `volumes` section 
     * Mount your `swapi_transformation_dbt` in `volumes` section as rean and write
   * Change `AIRFLOW__CORE__LOAD_EXAMPLES` to `false` (optional)

8. Here's how the final versions of your [Dockerfile](./Dockerfile) and [docker-compose.yml](./docker-compose.yaml) should look.

## Problems

### `File or directory not found`

Second, check that docker-compose can correctly map this directory to airflow worker.

Execute `docker ps` to see the list of docker containers running on your host machine and find the ID of the airflow worker.

Then execute `bash` on this container:

```bash
docker exec -it <container-ID> bash
```

Now check if the file with credentials is actually there:

```bash
ls -lh /.google/credentials/
```

If it's empty, docker-compose couldn't map the folder with credentials. 
In this case, try changing it to the absolute path to this folder:

```yaml
  volumes:
    - ./dags:/opt/airflow/dags
    - ./logs:/opt/airflow/logs
    - ./plugins:/opt/airflow/plugins
    # here: ----------------------------
    - /home/yusufuthman57/projects/quasale_class/project_swapi_api/swapi_transformation_dbt:rw
    # -----------------------------------
```
