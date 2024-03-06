#!/bin/bash

# Install ODBC driver for SQL Server
apt-get update
apt-get install -y unixodbc-dev
apt-get install -y tdsodbc