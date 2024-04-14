FROM ubuntu:22.04

# Copied from Joy of Coding project so random stuff might be left

# Set non-interactive timezone to avoid prompts during builds
ARG DEBIAN_FRONTEND=noninteractive
ENV TZ=America/Chicago
ENV LANG en_US.UTF-8
ENV LANGUAGE en_US:en
ENV LC_ALL en_US.UTF-8

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl wget git vim emacs locales build-essential tzdata lsof postgresql-client \
    python3 python3-pip

# Setup locale
RUN locale-gen en_US.UTF-8

# Copy the wait-for-it.sh script into the container and make it executable
COPY wait-for-it.sh /wait-for-it.sh
RUN chmod +x /wait-for-it.sh

# Cleanup
RUN apt-get clean && rm -rf /var/lib/apt/lists/*

# Set the working directory
WORKDIR /space_bar

# Install Python libraries for data manipulation, ETL, and database interaction
RUN pip3 install --no-cache-dir \
    pandas sqlalchemy numpy pyarrow csvkit beautifulsoup4 lxml requests psycopg2-binary python-dotenv Flask flask_caching Cache flask_bcrypt

# Create a non-root user
RUN useradd -M correction_tester

# Keep the container running indefinitely (useful for development and debugging)
CMD ["tail", "-f", "/dev/null"]
