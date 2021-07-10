#!/bin/bash

new_token=$1
sed -ie "s/KEN='.*'/KEN='${new_token}'/g" .env
