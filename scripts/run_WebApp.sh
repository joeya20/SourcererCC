#!/bin/bash

cd WebApp || exit 1

export FLASK_APP=hello
export FLASK_DEBUG=1
flask run
