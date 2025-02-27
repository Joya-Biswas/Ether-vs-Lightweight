# Combined Dockerfile for both Ganache and Streamlit
FROM python:3.9.10

# Install Node.js
RUN apt-get update && apt-get install -y \
  curl \
  gnupg \
  && curl -sL https://deb.nodesource.com/setup_16.x | bash - \
  && apt-get install -y nodejs \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/*

# Set up working directory
WORKDIR /app

# Fix for npm global install permission issues
RUN mkdir -p /app/.npm-global \
  && npm config set prefix '/app/.npm-global' \
  && export PATH="/app/.npm-global/bin:$PATH" \
  && echo 'export PATH="/app/.npm-global/bin:$PATH"' >> ~/.bashrc

# Install Ganache and Truffle globally
RUN npm install -g ganache-cli truffle

# Copy application files
COPY . /app

# Install Python dependencies
WORKDIR /app/app
RUN pip install -r requirements.txt

EXPOSE 8501

# Create a startup script
RUN echo '#!/bin/bash\n\
  export PATH="/app/.npm-global/bin:$PATH"\n\
  # Start Ganache in the background\n\
  ganache-cli -h 0.0.0.0 -p 8545 &\n\
  # Wait for Ganache to start\n\
  sleep 5\n\
  # Deploy contracts\n\
  cd /app && truffle migrate\n\
  # Start Streamlit\n\
  cd /app/app && streamlit run Run_Experiment.py\n\
  ' > /app/start.sh

RUN chmod +x /app/start.sh

# Set the entry point
CMD ["/app/start.sh"]