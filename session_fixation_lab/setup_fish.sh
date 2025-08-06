#!/bin/bash

echo "🏦 Setting up Session Fixation Lab with Database"
echo "================================================"

# Function to run docker commands via multipass
run_docker() {
    sudo multipass exec k3s -- sudo docker "$@"
}

echo "📦 Building PostgreSQL Docker image..."
run_docker build -t bank-postgres .

echo "🐳 Starting PostgreSQL container..."
run_docker run -d \
    --name bank-postgres \
    -p 5432:5432 \
    -e POSTGRES_DB=bank_db \
    -e POSTGRES_USER=bank_user \
    -e POSTGRES_PASSWORD=bank_password \
    bank-postgres

echo "⏳ Waiting for database to be ready..."
sleep 10

echo "🐍 Creating virtual environment..."
python3 -m venv venv

echo "📦 Installing Python dependencies..."
source venv/bin/activate
pip install -r requirements.txt

echo "✅ Setup complete!"
echo ""
echo "🚀 To start the lab:"
echo "1. Start the bank app: python bank_app.py"
echo "2. Start the hacker app: python vulnerable_app.py"
echo "3. Visit: http://localhost:5001/bank/register (to create account)"
echo "4. Visit: http://localhost:5001/bank/login (to login)"
echo "5. Visit: http://localhost:5000/login (hacker's fake site)"
echo ""
echo "📚 For session fixation demo:"
echo "python simple_session_fixation_demo.py"
echo ""
echo "🗑️  To clean up:"
echo "./cleanup_fish.sh" 

echo "🏦 Setting up Session Fixation Lab with Database"
echo "================================================"

# Function to run docker commands via multipass
run_docker() {
    sudo multipass exec k3s -- sudo docker "$@"
}

echo "📦 Building PostgreSQL Docker image..."
run_docker build -t bank-postgres .

echo "🐳 Starting PostgreSQL container..."
run_docker run -d \
    --name bank-postgres \
    -p 5432:5432 \
    -e POSTGRES_DB=bank_db \
    -e POSTGRES_USER=bank_user \
    -e POSTGRES_PASSWORD=bank_password \
    bank-postgres

echo "⏳ Waiting for database to be ready..."
sleep 10

echo "🐍 Creating virtual environment..."
python3 -m venv venv

echo "📦 Installing Python dependencies..."
source venv/bin/activate
pip install -r requirements.txt

echo "✅ Setup complete!"
echo ""
echo "🚀 To start the lab:"
echo "1. Start the bank app: python bank_app.py"
echo "2. Start the hacker app: python vulnerable_app.py"
echo "3. Visit: http://localhost:5001/bank/register (to create account)"
echo "4. Visit: http://localhost:5001/bank/login (to login)"
echo "5. Visit: http://localhost:5000/login (hacker's fake site)"
echo ""
echo "📚 For session fixation demo:"
echo "python simple_session_fixation_demo.py"
echo ""
echo "🗑️  To clean up:"
echo "./cleanup_fish.sh" 