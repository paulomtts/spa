# Multi-stage build for Python SPA application

# * Stage 1: Node.js stage for frontend build
FROM node:20-slim AS node-builder

WORKDIR /app

# Copy package files for better caching
COPY package*.json ./

# Install Node.js dependencies
RUN npm ci

# Copy source files needed for build
COPY tsconfig.json ./
COPY src/ ./src/
COPY templates/ ./templates/

# Create static directory and build frontend assets
RUN mkdir -p static && npm run build

# * Stage 2: Final stage with Python runtime
FROM python:3.13-slim

WORKDIR /app

# Install uv
RUN pip install uv

# Copy Python project files first for better caching
COPY pyproject.toml ./
COPY uv.lock ./

# Install Python dependencies
RUN uv pip install --system .

# Copy the rest of the application
COPY ./templates ./templates
COPY ./main.py ./main.py
COPY --from=node-builder /app/static/ ./static/