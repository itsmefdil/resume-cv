#!/bin/bash

# PM2 Deployment Script for Resume Website
# Usage: ./deploy.sh [development|production|stop|restart|logs]

set -e

PROJECT_NAME="resume-website"
PROJECT_DIR="./"

case "$1" in
    "development" | "dev")
        echo "🚀 Starting development server with PM2..."
        cd $PROJECT_DIR
        pm2 start ecosystem.config.js --env development
        pm2 save
        echo "✅ Development server started on http://localhost:8001"
        ;;
        
    "production" | "prod")
        echo "🚀 Starting production server with PM2..."
        cd $PROJECT_DIR
        pm2 start ecosystem.config.js --env production
        pm2 save
        echo "✅ Production server started on http://localhost:5000"
        ;;
        
    "gunicorn")
        echo "🚀 Starting Gunicorn server with PM2..."
        cd $PROJECT_DIR
        pm2 start resume-website-gunicorn
        pm2 save
        echo "✅ Gunicorn server started on http://localhost:5000"
        ;;
        
    "stop")
        echo "🛑 Stopping all resume website processes..."
        pm2 stop $PROJECT_NAME
        pm2 stop resume-website-gunicorn
        echo "✅ All processes stopped"
        ;;
        
    "restart")
        echo "🔄 Restarting all resume website processes..."
        pm2 restart $PROJECT_NAME
        pm2 restart resume-website-gunicorn
        echo "✅ All processes restarted"
        ;;
        
    "delete")
        echo "🗑️  Deleting all resume website processes..."
        pm2 delete $PROJECT_NAME
        pm2 delete resume-website-gunicorn
        echo "✅ All processes deleted"
        ;;
        
    "logs")
        echo "📋 Showing logs..."
        pm2 logs $PROJECT_NAME
        ;;
        
    "status")
        echo "📊 Showing PM2 status..."
        pm2 status
        ;;
        
    "monitor")
        echo "📈 Opening PM2 monitor..."
        pm2 monit
        ;;
        
    *)
        echo "📖 Usage: $0 {development|production|gunicorn|stop|restart|delete|logs|status|monitor}"
        echo ""
        echo "Commands:"
        echo "  development  - Start Flask dev server (port 8001)"
        echo "  production   - Start Flask production server (port 5000)"
        echo "  gunicorn     - Start Gunicorn server (port 5000)"
        echo "  stop         - Stop all processes"
        echo "  restart      - Restart all processes"
        echo "  delete       - Delete all processes"
        echo "  logs         - Show logs"
        echo "  status       - Show PM2 status"
        echo "  monitor      - Open PM2 monitor"
        exit 1
        ;;
esac
