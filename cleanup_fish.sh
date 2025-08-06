#!/bin/bash

echo "🧹 Cleaning up Session Fixation Lab"
echo "==================================="

# Function to run docker commands via multipass
run_docker() {
    sudo multipass exec k3s -- sudo docker "$@"
}

echo "🛑 Stopping PostgreSQL container..."
run_docker stop bank-postgres 2>/dev/null || echo "Container not running"

echo "🗑️  Removing PostgreSQL container..."
run_docker rm bank-postgres 2>/dev/null || echo "Container not found"

echo "🧹 Removing PostgreSQL image..."
run_docker rmi bank-postgres 2>/dev/null || echo "Image not found"

echo "✅ Cleanup complete!"
echo ""
echo "To restart the lab:"
echo "./setup_fish.sh" 

echo "🧹 Cleaning up Session Fixation Lab"
echo "==================================="

# Function to run docker commands via multipass
run_docker() {
    sudo multipass exec k3s -- sudo docker "$@"
}

echo "🛑 Stopping PostgreSQL container..."
run_docker stop bank-postgres 2>/dev/null || echo "Container not running"

echo "🗑️  Removing PostgreSQL container..."
run_docker rm bank-postgres 2>/dev/null || echo "Container not found"

echo "🧹 Removing PostgreSQL image..."
run_docker rmi bank-postgres 2>/dev/null || echo "Image not found"

echo "✅ Cleanup complete!"
echo ""
echo "To restart the lab:"
echo "./setup_fish.sh" 