# 📝 Production-Ready Todo App

A full-stack, production-ready todo application built with **Django REST Framework** backend and **React + Vite** frontend. Features JWT authentication, real-time WebSocket updates, and a clean modern UI.

## Features

✨ **Core Features**
- 🔐 JWT-based authentication with email & password
- 📋 Full CRUD operations for tasks
- 🏷️ Task priorities (Low, Medium, High)
- 📅 Date range and due date tracking
- ✅ Task completion tracking
- 🔍 Search and filter tasks
- 📊 Task statistics dashboard

🚀 **Real-time Features**
- 🔌 WebSocket-based real-time updates
- 👀 Live task synchronization across browsers
- 🔔 Instant notifications on task changes

🎨 **UI/UX**
- Clean, modern, responsive design
- Dark/light theme support ready
- Mobile-first approach
- Smooth animations and transitions
- Professional color scheme

🛠️ **Technical Excellence**
- RESTful API with Swagger/OpenAPI documentation
- Modular backend architecture
- Component-based React frontend
- Comprehensive error handling
- Production-ready Docker setup

## Tech Stack

### Backend
- **Django 6.0** - Web framework
- **Django REST Framework** - REST API
- **Django Channels** - WebSocket support
- **JWT Token Auth** - djangorestframework-simplejwt
- **PostgreSQL/SQLite** - Database
- **Redis** - Caching & WebSocket layer
- **Daphne** - ASGI server

### Frontend
- **React 18** - UI library
- **Vite** - Build tool
- **React Router** - Routing
- **Axios** - HTTP client
- **Zustand** - State management
- **Custom CSS** - Styling (no heavy frameworks)

## Project Structure

```
Revision_Tracker_APP/
├── backend/
│   ├── config/              # Django project settings
│   │   ├── settings.py
│   │   ├── urls.py
│   │   ├── asgi.py
│   │   └── wsgi.py
│   ├── apps/
│   │   ├── accounts/        # User authentication
│   │   │   ├── models.py
│   │   │   ├── serializers.py
│   │   │   ├── views.py
│   │   │   └── urls.py
│   │   └── tasks/           # Task management
│   │       ├── models.py
│   │       ├── serializers.py
│   │       ├── views.py
│   │       ├── permissions.py
│   │       └── urls.py
│   ├── core/
│   │   └── websocket.py     # WebSocket consumers
│   ├── manage.py
│   ├── requirements.txt
│   ├── Dockerfile
│   └── .env
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── Auth/        # Login, Register, ProtectedRoute
│   │   │   ├── Dashboard/   # Main dashboard
│   │   │   ├── Tasks/       # Task list & form
│   │   │   ├── Layout/      # Header, Sidebar
│   │   │   └── Common/      # Reusable UI components
│   │   ├── services/        # API calls
│   │   ├── hooks/           # Custom React hooks
│   │   ├── context/         # Auth context
│   │   ├── styles/          # CSS files
│   │   ├── App.jsx
│   │   └── main.jsx
│   ├── package.json
│   ├── Dockerfile
│   ├── .env
│   └── vite.config.js
├── docker-compose.yml
└── README.md
```

## Setup Instructions

### Prerequisites
- Python 3.11+
- Node.js 18+
- Docker & Docker Compose (optional, for containerized setup)

### Local Development (Without Docker)

#### Backend Setup

1. **Navigate to backend directory:**
   ```bash
   cd backend
   ```

2. **Create virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Create .env file:**
   ```bash
   cp .env.example .env
   ```

5. **Run migrations:**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

6. **Create superuser (optional):**
   ```bash
   python manage.py createsuperuser
   ```

7. **Run development server:**
   ```bash
   python manage.py runserver
   ```
   Server runs on: http://localhost:8000

#### Frontend Setup

1. **Navigate to frontend directory:**
   ```bash
   cd frontend
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```

3. **Create .env file:**
   ```bash
   cp .env.example .env
   ```

4. **Run development server:**
   ```bash
   npm run dev
   ```
   App runs on: http://localhost:5173

### Docker Setup (Recommended for Production)

1. **Build and run all services:**
   ```bash
   docker-compose up --build
   ```

2. **Run migrations (in new terminal):**
   ```bash
   docker-compose exec backend python manage.py migrate
   ```

3. **Create superuser (optional):**
   ```bash
   docker-compose exec backend python manage.py createsuperuser
   ```

4. **Access the application:**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000/api
   - API Docs: http://localhost:8000/api/docs
   - Admin: http://localhost:8000/admin

## API Endpoints

### Authentication
- `POST /api/auth/register/` - Register new user
- `POST /api/auth/login/` - Login (get JWT tokens)
- `POST /api/auth/token/refresh/` - Refresh access token
- `GET /api/auth/users/me/` - Get current user profile
- `POST /api/auth/logout/` - Logout

### Tasks
- `GET /api/tasks/` - List all tasks (with filtering)
- `POST /api/tasks/` - Create new task
- `GET /api/tasks/{id}/` - Get task details
- `PUT /api/tasks/{id}/` - Update task
- `PATCH /api/tasks/{id}/` - Partial update task
- `DELETE /api/tasks/{id}/` - Delete task
- `GET /api/tasks/today/` - Get today's tasks
- `GET /api/tasks/overdue/` - Get overdue tasks
- `GET /api/tasks/stats/` - Get task statistics

### Query Parameters
- `?is_completed=true|false` - Filter by completion status
- `?priority=low|medium|high` - Filter by priority
- `?search=query` - Search in title & description
- `?ordering=-created_at|due_date` - Sort results

### API Documentation
Visit `http://localhost:8000/api/docs/` for interactive Swagger UI

## Default Test Credentials

For local testing, create an account through the registration page.

## Development Commands

### Backend
```bash
cd backend

# Run migrations
python manage.py migrate

# Create migrations
python manage.py makemigrations

# Run tests
python manage.py test

# Access Django shell
python manage.py shell

# Run development server
python manage.py runserver

# Collect static files
python manage.py collectstatic
```

### Frontend
```bash
cd frontend

# Install dependencies
npm install

# Run development server
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview

# Run tests
npm run test

# Lint code
npm run lint
```

## Environment Variables

### Backend (.env)
```
SECRET_KEY=your-secret-key
DEBUG=True/False
ALLOWED_HOSTS=localhost,127.0.0.1
CORS_ALLOWED_ORIGINS=http://localhost:5173
DATABASE_URL=sqlite:///db.sqlite3 or postgresql://...
REDIS_URL=redis://localhost:6379
```

### Frontend (.env)
```
VITE_API_URL=http://localhost:8000/api
VITE_WS_URL=ws://localhost:8000/ws/tasks/
```

## Features in Detail

### Authentication Flow
1. User registers with email & password
2. JWT tokens (access & refresh) are issued
3. Access token stored in localStorage
4. Token automatically refreshed on expiry
5. Logout clears tokens & redirects to login

### Real-time Updates
- WebSocket connection established on login
- Task changes broadcast to all connected clients
- Automatic reconnection on disconnect
- User-specific task streams

### Task Management
- Create tasks with title, description, dates, priority
- Edit existing tasks
- Mark tasks as complete
- Delete tasks permanently
- Filter by status, priority, date range
- Search by title/description
- View task statistics

## Production Deployment

### Security Checklist
- [ ] Change `SECRET_KEY` in production
- [ ] Set `DEBUG=False`
- [ ] Configure `ALLOWED_HOSTS`
- [ ] Setup HTTPS/SSL
- [ ] Use PostgreSQL instead of SQLite
- [ ] Configure email backend for password resets
- [ ] Setup Redis for production
- [ ] Use environment variables for secrets
- [ ] Enable CORS only for trusted origins
- [ ] Setup automated backups

### Recommended Deployment
- **Backend**: Heroku, AWS, Google Cloud, DigitalOcean
- **Frontend**: Vercel, Netlify, AWS S3 + CloudFront
- **Database**: AWS RDS, Google Cloud SQL
- **Cache**: AWS ElastiCache, Heroku Redis

## Troubleshooting

### Backend Issues
- **Port already in use**: Change port in command `python manage.py runserver 8001`
- **Database error**: Ensure migrations are run: `python manage.py migrate`
- **Redis connection error**: Install and run Redis or update `REDIS_URL`

### Frontend Issues
- **API connection error**: Check `VITE_API_URL` in `.env`
- **WebSocket connection error**: Check `VITE_WS_URL` in `.env`
- **Port already in use**: Run on different port: `npm run dev -- --port 5174`

### Docker Issues
- **Port conflicts**: Change ports in docker-compose.yml
- **Container won't start**: Check logs: `docker-compose logs backend`
- **Database connection error**: Ensure postgres container is healthy

## Testing

### Backend Testing
```bash
python manage.py test apps.accounts apps.tasks
```

### Frontend Testing
```bash
npm run test
```

## Performance Optimization

- **Frontend**: Code splitting, lazy loading, image optimization
- **Backend**: Database indexing, query optimization, caching
- **WebSocket**: Connection pooling, message batching
- **Deployment**: CDN, compression, minification

## License

MIT License - feel free to use this project for personal or commercial purposes

## Support

For issues and feature requests, please open an issue on GitHub.

---

**Built with ❤️ using Django & React**
