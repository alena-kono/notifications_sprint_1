# Email worker 

## How to start 
1. create a .env file based on the .env.example
2. run the main docker-compose dev.yaml file 
``` bash
# in root dir 
./scripts/dev.sh up -d
```
3. enter to the poetry virtual env 
```
# in the email_worker root
poetry shell
poetry install
```
4. run a test smpt server 
``` bash
# under the poetry virtual env
python -m aiosmtpd -n -l localhost:9090
```
5. run the email_worker
``` bash
# under the poetry virtual env
python email_worker/main.py
```
you should see something similar to the log below
``` bash
2023-11-11 13:57:57,230 INFO     - FastStream app starting...
2023-11-11 13:57:57,245 INFO     - default | welcome-event |            - `WelcomeHandler` waiting for messages
...
2023-11-11 13:57:57,251 INFO     - FastStream app started successfully! To exit, press CTRL+C
```
6. login to the rabbit mq web page `localhost:15672`
7. go to the `Queues and Streams` tab
8. choose the topic you want to send a message e.g. `welcome-event`
9. generate an corresponding event payload 
10. press push 
11. check the message in the terminal where you run the test smpt server