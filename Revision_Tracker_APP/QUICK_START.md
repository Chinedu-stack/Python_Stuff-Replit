# ⚡ Quick Start Guide

Get the Todo App running in minutes!

## 🚀 Fastest Way: Docker (Recommended)

```bash
# Clone/navigate to project
cd Revision_Tracker_APP

# Start everything with one command
docker-compose up --build

# In a new terminal, run migrations
docker-compose exec backend python manage.py migrate

# Create a test user (optional)
# Register through the app UI at http://localhost:3000
```

**Access:**
- 🎨 Frontend: http://localhost:3000
- 🔌 Backend API: http://localhost:8000/api
- 📚 API Docs: http://localhost:8000/api/docs
- 🛠️ Admin: http://localhost:8000/admin

---

## 🛠️ Manual Setup (Without Docker)

### Backend

```bash
# Navigate to backend
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Start server
python manage.py runserver
```

Backend runs on: **http://localhost:8000**

### Frontend

In a new terminal:

```bash
# Navigate to frontend
cd frontend

# Install dependencies
npm install

# Start dev server
npm run dev
```

Frontend runs on: **http://localhost:5173**

---

## 📝 First Steps After Launch

1. **Create Account**
   - Go to http://localhost:5173/register
   - Sign up with email & password
   - Redirect to dashboard

2. **Create a Task**
   - Click "+ New Task" button
   - Fill in task details:
     - Title (required)
     - Description (optional)
     - Start & End dates (required)
     - Due date (optional)
     - Priority: Low, Medium, or High
   - Click "Save Task"

3. **Manage Tasks**
   - ✅ Check box to mark complete
   - ✏️ Click task to edit
   - 🗑️ Delete with trash button
   - 🔍 Search by title

4. **Filter & View**
   - Use sidebar to filter tasks
   - View by: All, Today, Active, Completed
   - Filter by priority: High, Medium, Low
   - View statistics on dashboard

---

## 🧪 Testing the API

### 1. Get Auth Token
```bash
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "your@email.com",
    "password": "your-password"
  }'
```

Response:
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "user": {...}
}
```

### 2. Create a Task
```bash
curl -X POST http://localhost:8000/api/tasks/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Buy groceries",
    "description": "Milk, eggs, bread",
    "start_date": "2026-05-18",
    "end_date": "2026-05-20",
    "priority": "high"
  }'
```

### 3. View All Tasks
```bash
curl http://localhost:8000/api/tasks/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

### 4. Interactive API Docs
Visit: **http://localhost:8000/api/docs/**

Swagger UI lets you test all endpoints without curl!

---

## 📚 API Endpoints Quick Reference

| Method | Endpoint | Purpose |
|--------|----------|---------|
| POST | `/api/auth/register/` | Create new account |
| POST | `/api/auth/login/` | Login & get tokens |
| GET | `/api/tasks/` | List all tasks |
| POST | `/api/tasks/` | Create task |
| PATCH | `/api/tasks/{id}/` | Update task |
| DELETE | `/api/tasks/{id}/` | Delete task |
| GET | `/api/tasks/stats/` | Get statistics |
| GET | `/api/tasks/today/` | Today's tasks |
| GET | `/api/tasks/overdue/` | Overdue tasks |

**Add filters:**
- `?is_completed=true` - Only completed
- `?priority=high` - High priority only
- `?search=word` - Search title/description
- `?ordering=-created_at` - Sort by date

---

## 🐛 Troubleshooting

### "Connection refused" on port 8000
- Backend not running
- Solution: `cd backend && python manage.py runserver`

### "Cannot GET /api/tasks"
- Not authenticated
- Solution: Login first via `/api/auth/login/`

### Frontend shows "Cannot connect to API"
- Check VITE_API_URL in `frontend/.env`
- Backend must be running on 8000
- Solution: `npm run dev`

### WebSocket connection failed
- Redis not running (for real-time updates)
- Can still use app, just no live updates
- Solution: Start Redis server

### Database error
- Migrations not run
- Solution: `python manage.py migrate`

---

## 📖 Learn More

- **Full README**: See `README.md` for complete documentation
- **Deployment**: See `DEPLOYMENT.md` for production setup
- **Architecture**: Check `README.md` for tech stack details

---

## 🎯 What's Included

✅ Full authentication system (JWT tokens)  
✅ Complete CRUD for tasks  
✅ Real-time WebSocket updates  
✅ Modern React UI with Vite  
✅ RESTful API with Swagger docs  
✅ Docker containerization  
✅ Database models & migrations  
✅ API filtering & search  
✅ Task statistics  
✅ Priority management  

---

## 💡 Tips

- Use API Docs (Swagger UI) for testing before building frontend
- Check console (F12) for JavaScript errors
- Check Django logs for backend errors
- WebSocket requires Redis (optional for local dev)
- Refresh token auto-expires in 7 days
- Access token expires in 1 hour (auto-refreshed)

---

## 🚀 Next Steps

1. Customize the UI in `frontend/src/components`
2. Add more fields to tasks in `backend/apps/tasks/models.py`
3. Deploy using Docker or one of the guides in `DEPLOYMENT.md`
4. Setup email notifications
5. Add user profiles and sharing

---

**That's it! Happy tasking! 🎉**
