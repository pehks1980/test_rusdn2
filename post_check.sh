#!/bin/bash
curl 127.0.0.1:8888/values -X POST -H "Content-Type: application/json" -d '{"test": "data"}'
curl 127.0.0.1:8888/values/2 -X GET