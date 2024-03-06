#!/bin/bash

# Check if the user is root (or has equivalent privileges)
if [ "$(id -u)" != "0" ]; then
    echo "This script must be run as root or with equivalent privileges" 1>&2
    exit 1
fi

# Install ODBC driver for SQL Server
apt-get update
apt-get install -y unixodbc-dev
apt-get install -y tdsodbc
