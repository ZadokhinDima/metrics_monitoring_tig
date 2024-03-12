This repository contains a solution to HW3 Resource monitoring systems. 

Services configured in docker-compose.yml:
- telegraf - agent for monitoring metrics
- influxdb - storage for metrics
- grafana - display metrics on dashboards
- mongodb - first database for demo
- elasticsearch - second database for demo
- pythonapp - python application with endpoints that access data in databases
- nginx - routes requests to pythonapp

Command used for generating load on services:
```
ab -n 100000 -c 200 http://localhost:80/all-johns
```
