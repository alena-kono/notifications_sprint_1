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
4. Run `notifications` service:
    ``` bash
    # under the poetry virtual env
    python -m src.main
    ```
5. Run `auth` service following [the documentation](../auth/README.md).