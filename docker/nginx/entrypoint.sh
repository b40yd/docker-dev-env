#!/bin/bash

echo "Starting Nginx and Vector..."
nginx &
vector --config /etc/vector/vector.toml 