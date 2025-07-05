FROM python:3.11-slim

# Install Node.js and nginx
RUN apt-get update && \
    apt-get install -y curl gnupg nginx supervisor && \
    curl -fsSL https://deb.nodesource.com/setup_18.x | bash - && \
    apt-get install -y nodejs && \
    apt-get clean

# Set working directory
WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# # Copy Node source and install dependencies
# COPY frontend/package.json frontend/package-lock.json* ./frontend/
# COPY frontend/package.json ./frontend/
# WORKDIR /app/frontend
# RUN npm install
# WORKDIR /app

# # Copy Django code
# COPY backend ./backend

# Copy Node source and install dependencies
COPY frontend ./frontend
WORKDIR /app/frontend
RUN npm install
WORKDIR /app

# Copy Django code and entry script
COPY backend ./backend
COPY serve.py ./serve.py



# Copy Supervisor and nginx config
COPY supervisord.conf /etc/supervisord.conf
COPY nginx.conf /etc/nginx/nginx.conf

# Expose port 80 for Beanstalk/nginx
EXPOSE 80

# Start Supervisor to run all services
CMD ["/usr/bin/supervisord", "-c", "/etc/supervisord.conf"]