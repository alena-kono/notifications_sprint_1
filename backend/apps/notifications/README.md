# Notifications service

## How to start 
1. Create `.env` file based on the `.env.example`.
2. Run the main docker-compose dev.yaml file: 
    ``` bash
    # in the root dir 
    ./scripts/dev.sh up -d
    ```
3. Activate `poetry` virtual env:
    ```
    cd backend/apps/notifications
    poetry shell
    poetry install
    ```
4. Run Notifications service:
    ``` bash
    # under the poetry virtual env
    faststream run src.main:app
    ```