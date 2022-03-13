#!/bin/bash

if curl -s 'localhost:1234/time' > /dev/null
then echo "Request was successful. Station is working"
else echo "CURL Failed. Station could not be reached."
fi

