#!/bin/bash

path="/home/cny/c-drive/Users/TERMINAL/Desktop/python/instagram/to_post/stories"
cd ${path}

python -m http.server 8000 &
$HOME/Applications/ngrok http 8000 &
