# Use Python base image with uv pre-installed
FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim

# Set the working directory
WORKDIR /app

# Install dependencies in a separate layer for better caching
# Copy only the files needed for dependency resolution
COPY pyproject.toml uv.lock ./

# Install dependencies but not the project itself yet
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked --no-install-project

# Copy the app code into the container
COPY server.py .

# Install the project itself
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked

# Expose any ports if needed (MCP typically uses stdio, but keeping for flexibility)
# EXPOSE 8000

# Set the command to run the application
CMD ["uv", "run", "server.py"] 