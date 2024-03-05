#!/bin/bash

# Install ODBC driver for SQL Server
sudo apt-get update
sudo apt-get install -y unixodbc-dev
sudo apt-get install -y tdsodbc