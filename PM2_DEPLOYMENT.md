# PM2 Deployment Guide for Resume Website

## Quick Start Commands

### 1. Install PM2 (if not installed)
```bash
npm install -g pm2
```

### 2. Simple Deployment Commands

```bash
# Start development server (recommended for development)
./deploy.sh development

# Start production server with Flask
./deploy.sh production  

# Start production server with Gunicorn (recommended for production)
./deploy.sh gunicorn

# Stop all servers
./deploy.sh stop

# Restart all servers
./deploy.sh restart

# View logs
./deploy.sh logs

# Check status
./deploy.sh status

# Open monitoring dashboard
./deploy.sh monitor
```

## Alternative Commands (without script)

### Development Mode
```bash
pm2 start ecosystem.config.js --env development
pm2 save
```

### Production Mode (Flask)
```bash
pm2 start ecosystem.config.js --env production
pm2 save
```

### Production Mode (Gunicorn - Recommended)
```bash
pm2 start resume-website-gunicorn
pm2 save
```

### Management Commands
```bash
# View all processes
pm2 list

# Stop specific process
pm2 stop resume-website

# Restart specific process  
pm2 restart resume-website

# Delete process
pm2 delete resume-website

# Show logs
pm2 logs resume-website

# Monitor resources
pm2 monit

# Save current process list
pm2 save

# Resurrect saved processes (after reboot)
pm2 resurrect
```

## Process Details

### Available Processes:
1. **resume-website** - Flask development/production server
2. **resume-website-gunicorn** - Gunicorn WSGI server (recommended for production)

### Ports:
- **Development**: http://localhost:8001
- **Production**: http://localhost:5000

### Log Files:
- Error logs: `./logs/resume-error.log`
- Output logs: `./logs/resume-out.log`
- Combined logs: `./logs/resume-combined.log`

## Auto-restart on System Reboot

```bash
# Generate startup script
pm2 startup

# Save current process list
pm2 save
```

## Environment Variables

The ecosystem config supports different environments:
- `--env development` - Development mode with debug
- `--env production` - Production mode optimized

## Monitoring

### Real-time Monitoring
```bash
pm2 monit
```

### Web-based Monitoring (Optional)
```bash
# Install PM2 Plus for web monitoring
pm2 install pm2-server-monit
```

## Troubleshooting

### Check if processes are running
```bash
pm2 status
```

### View detailed logs
```bash
pm2 logs --lines 100
```

### Restart if issues occur
```bash
pm2 restart all
```

### Clear logs
```bash
pm2 flush
```

## Quick Deployment Workflow

1. **First time setup:**
   ```bash
   npm install -g pm2
   ./deploy.sh gunicorn
   pm2 save
   pm2 startup
   ```

2. **Daily development:**
   ```bash
   ./deploy.sh development  # Start dev server
   ./deploy.sh logs         # Check logs
   ./deploy.sh stop         # Stop when done
   ```

3. **Production deployment:**
   ```bash
   ./deploy.sh gunicorn     # Start production
   ./deploy.sh status       # Verify running
   ```
