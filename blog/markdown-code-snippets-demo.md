---
title: "Markdown and Code Snippets Demo"
date: "2025-07-19"
category: "Development"
summary: "A comprehensive demo showcasing markdown formatting and syntax highlighting for various programming languages."
tags: ["markdown", "syntax-highlighting", "demo", "programming"]
read_time: "5 min read"
---

# Markdown and Code Snippets Demo

This post demonstrates the enhanced markdown support with syntax highlighting for code snippets across various programming languages.

## Python Code Example

Here's a Python function for handling API requests:

```python
import requests
import json
from typing import Dict, Optional

def fetch_user_data(user_id: int, api_key: str) -> Optional[Dict]:
    """
    Fetch user data from the API with error handling.
    
    Args:
        user_id: The ID of the user to fetch
        api_key: API authentication key
    
    Returns:
        User data dictionary or None if error occurs
    """
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json'
    }
    
    try:
        response = requests.get(f'https://api.example.com/users/{user_id}', headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching user data: {e}")
        return None

# Usage example
user = fetch_user_data(123, "your-api-key-here")
if user:
    print(f"Welcome, {user['name']}!")
```

## JavaScript/Node.js Example

Here's an Express.js route handler:

```javascript
const express = require('express');
const bcrypt = require('bcrypt');
const jwt = require('jsonwebtoken');

const app = express();

// User authentication endpoint
app.post('/api/auth/login', async (req, res) => {
    try {
        const { email, password } = req.body;
        
        // Validate input
        if (!email || !password) {
            return res.status(400).json({ 
                error: 'Email and password are required' 
            });
        }
        
        // Find user in database
        const user = await User.findOne({ email });
        if (!user) {
            return res.status(401).json({ error: 'Invalid credentials' });
        }
        
        // Verify password
        const isValid = await bcrypt.compare(password, user.password);
        if (!isValid) {
            return res.status(401).json({ error: 'Invalid credentials' });
        }
        
        // Generate JWT token
        const token = jwt.sign(
            { userId: user._id, email: user.email },
            process.env.JWT_SECRET,
            { expiresIn: '24h' }
        );
        
        res.json({
            message: 'Login successful',
            token,
            user: {
                id: user._id,
                email: user.email,
                name: user.name
            }
        });
        
    } catch (error) {
        console.error('Login error:', error);
        res.status(500).json({ error: 'Internal server error' });
    }
});
```

## Bash/Shell Script

DevOps automation script:

```bash
#!/bin/bash

# Deployment script for containerized applications
set -e

# Configuration
APP_NAME="myapp"
DOCKER_REGISTRY="registry.example.com"
ENVIRONMENT=${1:-staging}
VERSION=${2:-latest}

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Build and push Docker image
build_and_push() {
    log_info "Building Docker image for $APP_NAME:$VERSION"
    
    docker build -t $APP_NAME:$VERSION .
    docker tag $APP_NAME:$VERSION $DOCKER_REGISTRY/$APP_NAME:$VERSION
    
    log_info "Pushing image to registry..."
    docker push $DOCKER_REGISTRY/$APP_NAME:$VERSION
}

# Deploy to Kubernetes
deploy_to_k8s() {
    log_info "Deploying to Kubernetes environment: $ENVIRONMENT"
    
    # Update deployment with new image
    kubectl set image deployment/$APP_NAME \
        $APP_NAME=$DOCKER_REGISTRY/$APP_NAME:$VERSION \
        -n $ENVIRONMENT
    
    # Wait for rollout to complete
    kubectl rollout status deployment/$APP_NAME -n $ENVIRONMENT
    
    log_info "Deployment completed successfully!"
}

# Main execution
main() {
    log_info "Starting deployment process..."
    
    if [[ $# -lt 1 ]]; then
        log_warn "Usage: $0 <environment> [version]"
        log_warn "Example: $0 staging v1.2.3"
        exit 1
    fi
    
    build_and_push
    deploy_to_k8s
    
    log_info "All done! Application is now running."
}

main "$@"
```

## YAML Configuration

Kubernetes deployment manifest:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: web-app
  namespace: production
  labels:
    app: web-app
    version: v1.0.0
spec:
  replicas: 3
  selector:
    matchLabels:
      app: web-app
  template:
    metadata:
      labels:
        app: web-app
    spec:
      containers:
      - name: web-app
        image: registry.example.com/web-app:v1.0.0
        ports:
        - containerPort: 8080
          name: http
        env:
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: app-secrets
              key: database-url
        - name: REDIS_URL
          value: "redis://redis-service:6379"
        resources:
          requests:
            memory: "256Mi"
            cpu: "250m"
          limits:
            memory: "512Mi"
            cpu: "500m"
        livenessProbe:
          httpGet:
            path: /health
            port: 8080
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /ready
            port: 8080
          initialDelaySeconds: 5
          periodSeconds: 5
---
apiVersion: v1
kind: Service
metadata:
  name: web-app-service
  namespace: production
spec:
  selector:
    app: web-app
  ports:
  - port: 80
    targetPort: 8080
  type: LoadBalancer
```

## SQL Database Query

Complex PostgreSQL query example:

```sql
-- Advanced analytics query for user engagement metrics
WITH user_activity AS (
    SELECT 
        u.user_id,
        u.email,
        u.created_at,
        COUNT(DISTINCT s.session_id) as total_sessions,
        COUNT(DISTINCT DATE(s.created_at)) as active_days,
        AVG(s.duration_minutes) as avg_session_duration,
        MAX(s.created_at) as last_activity
    FROM users u
    LEFT JOIN sessions s ON u.user_id = s.user_id
    WHERE u.created_at >= NOW() - INTERVAL '30 days'
    GROUP BY u.user_id, u.email, u.created_at
),
engagement_scores AS (
    SELECT 
        *,
        CASE 
            WHEN total_sessions >= 20 AND active_days >= 15 THEN 'High'
            WHEN total_sessions >= 10 AND active_days >= 7 THEN 'Medium'
            WHEN total_sessions >= 3 AND active_days >= 3 THEN 'Low'
            ELSE 'Inactive'
        END as engagement_level,
        ROW_NUMBER() OVER (ORDER BY total_sessions DESC, active_days DESC) as engagement_rank
    FROM user_activity
)
SELECT 
    user_id,
    email,
    total_sessions,
    active_days,
    ROUND(avg_session_duration, 2) as avg_session_duration,
    engagement_level,
    engagement_rank,
    EXTRACT(DAYS FROM NOW() - last_activity) as days_since_last_activity
FROM engagement_scores
WHERE engagement_level != 'Inactive'
ORDER BY engagement_rank
LIMIT 100;
```

## JSON Configuration

Package.json for a Node.js project:

```json
{
  "name": "awesome-web-app",
  "version": "1.0.0",
  "description": "A modern web application with React and Express",
  "main": "server.js",
  "scripts": {
    "start": "node server.js",
    "dev": "concurrently \"npm run server\" \"npm run client\"",
    "server": "nodemon server.js",
    "client": "cd client && npm start",
    "build": "cd client && npm run build",
    "test": "jest",
    "test:watch": "jest --watch",
    "lint": "eslint .",
    "lint:fix": "eslint . --fix"
  },
  "dependencies": {
    "express": "^4.18.2",
    "cors": "^2.8.5",
    "helmet": "^7.0.0",
    "morgan": "^1.10.0",
    "mongoose": "^7.5.0",
    "bcryptjs": "^2.4.3",
    "jsonwebtoken": "^9.0.1",
    "dotenv": "^16.3.1",
    "joi": "^17.9.2"
  },
  "devDependencies": {
    "nodemon": "^3.0.1",
    "concurrently": "^8.2.0",
    "jest": "^29.6.2",
    "supertest": "^6.3.3",
    "eslint": "^8.47.0",
    "@types/node": "^20.5.0"
  },
  "engines": {
    "node": ">=18.0.0",
    "npm": ">=9.0.0"
  },
  "keywords": [
    "nodejs",
    "express",
    "react",
    "mongodb",
    "jwt",
    "api"
  ],
  "author": "Your Name <your.email@example.com>",
  "license": "MIT"
}
```

## Markdown Features

### Lists and Formatting

**Unordered List:**
- Infrastructure as Code with Terraform
- Container orchestration with Kubernetes
- CI/CD pipelines with Jenkins/GitLab
- Monitoring with Prometheus and Grafana

**Ordered List:**
1. Plan your infrastructure requirements
2. Design modular and reusable components
3. Implement proper state management
4. Set up comprehensive monitoring
5. Document everything thoroughly

### Blockquotes

> "Infrastructure as Code is not just about automation; it's about creating a reliable, repeatable, and auditable way to manage your cloud resources."
> 
> — DevOps Engineer

### Tables

| Language | Use Case | Difficulty | Performance |
|----------|----------|------------|-------------|
| Python | Data Science, Automation | Easy | Medium |
| JavaScript | Web Development | Easy | Medium |
| Go | Microservices, CLI Tools | Medium | High |
| Rust | Systems Programming | Hard | Very High |
| TypeScript | Large Applications | Medium | Medium |

### Inline Code

Use `kubectl get pods` to list all pods in the current namespace, or `terraform plan` to preview infrastructure changes before applying them.

## Conclusion

This enhanced markdown support provides:

- ✅ **Syntax highlighting** for multiple programming languages
- ✅ **Copy button functionality** for easy code copying
- ✅ **Proper typography** for better readability
- ✅ **Responsive design** that works on all devices
- ✅ **Modern styling** with consistent theming

The blog now supports rich content formatting that makes technical articles more engaging and easier to follow!
