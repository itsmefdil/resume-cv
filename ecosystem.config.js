module.exports = {
    apps: [
        {
            name: 'resume-website',
            script: 'app.py',
            interpreter: 'python3',
            cwd: './',
            instances: 1,
            exec_mode: 'fork',
            watch: false,
            autorestart: true,
            max_restarts: 5,
            min_uptime: '10s',
            max_memory_restart: '500M',
            env: {
                FLASK_APP: 'app.py',
                FLASK_ENV: 'production',
                FLASK_DEBUG: '0',
                HOST: '0.0.0.0',
                PORT: '5000'
            },
            env_development: {
                FLASK_APP: 'app.py',
                FLASK_ENV: 'development',
                FLASK_DEBUG: '1',
                HOST: '127.0.0.1',
                PORT: '8001'
            },
            env_production: {
                FLASK_APP: 'app.py',
                FLASK_ENV: 'production',
                FLASK_DEBUG: '0',
                HOST: '0.0.0.0',
                PORT: '5000'
            },
            log_date_format: 'YYYY-MM-DD HH:mm:ss Z',
            error_file: './logs/resume-error.log',
            out_file: './logs/resume-out.log',
            log_file: './logs/resume-combined.log',
            pid_file: './pids/resume.pid'
        },
        {
            name: 'resume-website-gunicorn',
            script: 'gunicorn',
            args: '--bind 0.0.0.0:5000 --workers 4 --timeout 120 --worker-class sync --worker-connections 1000 --max-requests 1000 --max-requests-jitter 100 --preload app:app',
            cwd: './',
            instances: 1,
            exec_mode: 'fork',
            watch: false,
            autorestart: true,
            max_restarts: 5,
            min_uptime: '10s',
            max_memory_restart: '1G',
            env: {
                FLASK_APP: 'app.py',
                FLASK_ENV: 'production',
                FLASK_DEBUG: '0'
            },
            log_date_format: 'YYYY-MM-DD HH:mm:ss Z',
            error_file: './logs/resume-gunicorn-error.log',
            out_file: './logs/resume-gunicorn-out.log',
            log_file: './logs/resume-gunicorn-combined.log',
            pid_file: './pids/resume-gunicorn.pid'
        }
    ],

    deploy: {
        production: {
            user: 'deploy',
            host: ['your-server.com'],
            ref: 'origin/main',
            repo: 'https://github.com/itsmefdil/resume-cv.git',
            path: '/var/www/resume-website',
            'pre-deploy-local': '',
            'post-deploy': 'pip install -r requirements.txt && pm2 reload ecosystem.config.js --env production',
            'pre-setup': '',
            env: {
                NODE_ENV: 'production'
            }
        },
        development: {
            user: 'dev',
            host: ['dev-server.com'],
            ref: 'origin/develop',
            repo: 'https://github.com/itsmefdil/resume-cv.git',
            path: '/var/www/resume-website-dev',
            'post-deploy': 'pip install -r requirements.txt && pm2 reload ecosystem.config.js --env development',
            env: {
                NODE_ENV: 'development'
            }
        }
    }
};
