#!/bin/bash

#  Copyright (c) 2024
#  by St3vebrush <steve@d3velopment.fr> with love for D3velopment
# This script checks and installs Python dependencies from requirements.txt
# before starting the Unit server. It ensures all required packages are 
# available before launching the application server, providing a clean startup
# process that fails early if dependencies cannot be satisfied.

echo "Checking dependencies from requirements.txt..."

# Check if requirements.txt exists
if [ ! -f /app/requirements.txt ]; then
    echo "Error: requirements.txt not found in /app directory"
    exit 1
fi

# Check if pip is installed
if ! command -v pip &> /dev/null; then
    echo "Error: pip is not installed"
    exit 1
fi

# Check each dependency and install if missing
missing_deps=0
missing_deps_list=""
while read -r requirement || [ -n "$requirement" ]; do
    # Skip empty lines and comments
    if [[ -z "$requirement" || "$requirement" =~ ^# ]]; then
        continue
    fi
    
    # Extract package name (remove version specifiers)
    package=$(echo "$requirement" | sed 's/[<>=!~].*//')
    package=$(echo "$package" | xargs)  # Trim whitespace
    
    # Check if package is installed
    if ! pip show "$package" &> /dev/null; then
        echo "Missing dependency: $package"
        missing_deps=$((missing_deps+1))
        missing_deps_list="$missing_deps_list $requirement"
    fi
done < /app/requirements.txt

# Install missing dependencies
if [ $missing_deps -eq 0 ]; then
    echo "All dependencies are already installed!"
else
    echo "Found $missing_deps missing dependencies. Installing now..."
    pip install -r /app/requirements.txt
    
    # Verify installation was successful
    if [ $? -eq 0 ]; then
        echo "All dependencies installed successfully!"
    else
        echo "Error: Failed to install some dependencies."
        exit 1
    fi
fi

# If we reach here, all dependencies are installed successfully
echo "Starting NGINX Unit server..."
exec /usr/local/bin/docker-entrypoint.sh unitd --no-daemon --control unix:/var/run/control.unit.sock
