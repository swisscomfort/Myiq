# Crypto Recovery Toolkit - Portable Scanner Container
# Build: docker build -t crypto-scanner .
# Run:   docker run -v /evidence:/evidence crypto-scanner --root /evidence --outdir /evidence/reports

FROM python:3.11-slim

# Install dependencies
RUN apt-get update && apt-get install -y \
    bash \
    coreutils \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy scanner files
COPY tools/modules/search.py /app/
COPY yara_rules/ /app/yara_rules/

# Make scanner executable
RUN chmod +x /app/search.py

# Set entry point
ENTRYPOINT ["python3", "/app/search.py"]
CMD ["--help"]

# Volume for evidence mounting
VOLUME ["/evidence"]

# Metadata
LABEL maintainer="Crypto Recovery Toolkit Team"
LABEL description="Portable crypto wallet scanner for forensic analysis"
LABEL version="1.0.0"
