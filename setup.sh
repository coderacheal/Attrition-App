# Download Microsoft GPG key and add it to trusted keys
curl https://packages.microsoft.com/keys/microsoft.asc | tee /tmp/microsoft.asc
mv /tmp/microsoft.asc /etc/apt/trusted.gpg.d/microsoft.asc

# Add Microsoft repository to package sources
echo "deb [arch=amd64,arm64,armhf signed-by=/usr/share/keyrings/microsoft-prod.gpg] https://packages.microsoft.com/debian/12/prod bookworm main" | tee /etc/apt/sources.list.d/mssql-release.list

# Update package lists
apt-get update

# Install msodbcsql17 with EULA acceptance
ACCEPT_EULA=Y apt-get install -y msodbcsql17

# Install mssql-tools with EULA acceptance
ACCEPT_EULA=Y apt-get install -y mssql-tools

# Add mssql-tools binaries to PATH
echo 'export PATH="$PATH:/opt/mssql-tools/bin"' >> ~/.bashrc

# Install unixODBC development headers
apt-get install -y unixodbc-dev

# Install kerberos library for Debian distributions
apt-get install -y libgssapi-krb5-2
