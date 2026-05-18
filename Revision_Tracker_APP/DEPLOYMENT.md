# Deployment Guide

## Pre-deployment Checklist

### Security
- [ ] Change SECRET_KEY in production settings
- [ ] Set DEBUG = False
- [ ] Configure ALLOWED_HOSTS properly
- [ ] Setup HTTPS/SSL certificates
- [ ] Configure CORS for production domains
- [ ] Remove debug-only middleware
- [ ] Setup secure cookies and session handling
- [ ] Enable CSRF protection
- [ ] Setup rate limiting

### Database
- [ ] Use PostgreSQL in production (not SQLite)
- [ ] Setup automated backups
- [ ] Configure connection pooling
- [ ] Run migrations on deployment
- [ ] Create production database user
- [ ] Setup database monitoring

### Backend (Django)
- [ ] Collect static files: `python manage.py collectstatic`
- [ ] Run all migrations: `python manage.py migrate`
- [ ] Test with production settings
- [ ] Setup logging and monitoring
- [ ] Configure email backend
- [ ] Setup error tracking (Sentry)
- [ ] Configure Redis for production

### Frontend (React)
- [ ] Build production bundle: `npm run build`
- [ ] Test production build locally
- [ ] Optimize images
- [ ] Setup environment variables for production
- [ ] Configure CDN for static assets
- [ ] Setup error tracking (Sentry)

## Deployment Options

### Option 1: Heroku + Vercel (Easy)

#### Backend Deployment (Heroku)
```bash
# Install Heroku CLI
# Login to Heroku
heroku login

# Create new app
heroku create your-app-name

# Add buildpacks
heroku buildpacks:add heroku/python
heroku buildpacks:add heroku/nodejs

# Set environment variables
heroku config:set SECRET_KEY=your-secret-key
heroku config:set ALLOWED_HOSTS=your-app-name.herokuapp.com
heroku config:set DEBUG=False

# Add PostgreSQL
heroku addons:create heroku-postgresql:hobby-dev

# Add Redis
heroku addons:create heroku-redis:premium-0

# Deploy
git push heroku main

# Run migrations
heroku run python manage.py migrate

# Create superuser
heroku run python manage.py createsuperuser
```

#### Frontend Deployment (Vercel)
```bash
# Install Vercel CLI
npm i -g vercel

# Deploy from frontend directory
cd frontend
vercel

# Set environment variables in Vercel dashboard
VITE_API_URL=https://your-app-name.herokuapp.com/api
VITE_WS_URL=wss://your-app-name.herokuapp.com/ws/tasks/
```

### Option 2: AWS (Scalable)

#### Backend (EC2 or Elastic Beanstalk)
```bash
# Install AWS CLI
# Create EC2 instance or EB environment
# Connect via SSH

# Clone repository
git clone your-repo

# Setup environment
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Setup Gunicorn
pip install gunicorn

# Run with Gunicorn
gunicorn config.wsgi:application --bind 0.0.0.0:8000

# Setup supervisor for automatic restarts
sudo apt-get install supervisor
# ... configure supervisor file
```

#### Frontend (S3 + CloudFront)
```bash
# Build frontend
cd frontend
npm run build

# Upload to S3
aws s3 sync dist/ s3://your-bucket-name

# Create CloudFront distribution for CDN
# Set Origin to S3 bucket
# Configure SSL certificate
```

### Option 3: DigitalOcean App Platform

```bash
# Push to GitHub
git push origin main

# In DigitalOcean App Platform:
# 1. Connect GitHub account
# 2. Select repository
# 3. Auto-detect Django and React apps
# 4. Configure environment variables
# 5. Deploy
```

### Option 4: Docker Swarm / Kubernetes

#### Push Docker Images to Registry
```bash
# Build images
docker-compose build

# Tag images
docker tag todo-app-backend:latest your-registry/todo-backend:latest
docker tag todo-app-frontend:latest your-registry/todo-frontend:latest

# Push to Docker Hub or ECR
docker push your-registry/todo-backend:latest
docker push your-registry/todo-frontend:latest
```

#### Kubernetes Deployment
```bash
# Create secrets for environment variables
kubectl create secret generic todo-secrets \
  --from-literal=SECRET_KEY=your-secret-key \
  --from-literal=DATABASE_URL=postgresql://...

# Deploy using kubectl
kubectl apply -f k8s/
```

## Production Environment Variables

### Backend (.env)
```
SECRET_KEY=generate-strong-random-key
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
CORS_ALLOWED_ORIGINS=https://yourdomain.com,https://www.yourdomain.com
DATABASE_URL=postgresql://user:password@host:5432/dbname
REDIS_URL=redis://host:6379
ENVIRONMENT=production
```

### Frontend (.env.production)
```
VITE_API_URL=https://api.yourdomain.com/api
VITE_WS_URL=wss://api.yourdomain.com/ws/tasks/
```

## Performance Optimization for Production

### Backend
- Setup caching with Redis
- Use database query optimization
- Enable GZIP compression
- Setup CDN for static files
- Use connection pooling
- Enable database indexes

### Frontend
- Code splitting with React.lazy()
- Image optimization
- CSS minification
- JavaScript minification
- Service worker for offline support
- HTTP/2 push for critical resources

## Monitoring & Logging

### Backend Monitoring
- **Application**: Sentry for error tracking
- **Performance**: New Relic or Datadog
- **Logs**: ELK Stack or CloudWatch
- **Database**: pgAdmin or RDS monitoring
- **Health Checks**: Set up endpoint monitoring

### Frontend Monitoring
- **Error Tracking**: Sentry
- **Performance**: Vercel Analytics or Datadog
- **User Analytics**: Google Analytics or Mixpanel
- **Real User Monitoring**: SpeedCurve or Synthetics

## Backup & Recovery

### Database Backups
```bash
# PostgreSQL automated backup
pg_dump dbname > backup.sql

# Restore from backup
psql dbname < backup.sql

# Setup automated backups (AWS RDS)
# - Enable automated backups
# - Set retention period to 30 days
# - Enable multi-AZ deployment
```

### File Uploads & Media
- Store in S3 or similar cloud storage
- Setup versioning
- Enable lifecycle policies for old files
- Configure CloudFront CDN

## SSL/TLS Certificate

### Using Let's Encrypt (Free)
```bash
# Install certbot
sudo apt-get install certbot python3-certbot-nginx

# Get certificate
sudo certbot certonly --standalone -d yourdomain.com -d www.yourdomain.com

# Auto-renewal (auto-installed)
sudo systemctl enable certbot.timer
```

### Using AWS Certificate Manager
- Request certificate in ACM
- Validate domain ownership
- Attach to CloudFront or ALB

## Rollback Strategy

```bash
# Tag production releases
git tag -a v1.0.0 -m "Production release"
git push origin v1.0.0

# Quick rollback to previous version
git checkout v0.9.9
git push -f origin main

# For containers
docker pull your-registry/todo-backend:previous-tag
docker-compose up -d
```

## Scaling

### Horizontal Scaling
- Add more application servers
- Use load balancer (HAProxy, nginx, AWS ALB)
- Implement session sharing with Redis
- Scale database with read replicas

### Vertical Scaling
- Increase server resources (CPU, RAM)
- Optimize database queries
- Implement caching layer
- Use connection pooling

## Production Checklist

- [ ] Domain registered and configured
- [ ] SSL certificate installed
- [ ] Database backup strategy implemented
- [ ] Monitoring and alerts configured
- [ ] Error tracking (Sentry) setup
- [ ] Logging aggregation configured
- [ ] CDN configured for static assets
- [ ] Rate limiting implemented
- [ ] API documentation accessible
- [ ] Admin panel secured
- [ ] Health check endpoint working
- [ ] Load testing completed
- [ ] Security audit completed
- [ ] Performance benchmarks established
- [ ] Incident response plan documented

## Support & Maintenance

### Regular Tasks
- Monitor application logs
- Review performance metrics
- Update dependencies monthly
- Run security patches immediately
- Backup databases daily
- Review user feedback and issues

### Scheduled Maintenance
- Weekly: Database optimization
- Monthly: Security updates and dependency upgrades
- Quarterly: Performance review and optimization
- Annually: Security audit and comprehensive review
