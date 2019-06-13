#!bin/bash/

docker cp ./ai_server_proto ai_server_proto_1:/opt/services/djangoapp/src

docker restart ai_server_proto_1
