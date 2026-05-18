#!/bin/bash

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}🚀 Starting Todo App (Development Mode)${NC}"
echo ""

# Start backend
echo -e "${BLUE}📦 Starting Backend Server...${NC}"
cd backend
source venv/Scripts/activate 2>/dev/null || source venv/bin/activate
python manage.py migrate
python manage.py runserver &
BACKEND_PID=$!
echo -e "${GREEN}✅ Backend running on http://localhost:8000${NC}"
echo -e "${GREEN}📚 API Docs: http://localhost:8000/api/docs${NC}"
echo ""

# Start frontend
echo -e "${BLUE}🎨 Starting Frontend Server...${NC}"
cd ../frontend
npm run dev &
FRONTEND_PID=$!
echo -e "${GREEN}✅ Frontend running on http://localhost:5173${NC}"
echo ""

echo -e "${GREEN}✅ Todo App is ready!${NC}"
echo -e "${BLUE}Press Ctrl+C to stop all servers${NC}"
echo ""

# Wait for both processes
wait $BACKEND_PID $FRONTEND_PID
