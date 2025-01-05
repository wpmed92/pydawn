# Use an x64 Python image explicitly
FROM --platform=linux/amd64 python:3.9-slim

# Add LLVM repository for Clang 17 and install necessary dependencies
RUN apt-get update && apt-get install -y \
    wget gnupg software-properties-common && \
    wget https://apt.llvm.org/llvm.sh && \
    chmod +x llvm.sh && ./llvm.sh 17 && \
    apt-get install -y \
    clang-17 libclang-17-dev llvm-17-dev && \
    pip install ctypeslib2 clang==17.* && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Set environment variables to use Clang 17
ENV CC=clang-17 CXX=clang++-17

# Set working directory
WORKDIR /app

# Copy the header and shared library into the container
COPY webgpu.h /app/webgpu.h
COPY libwebgpu_dawn.so /app/libwebgpu_dawn.so

# Generate Python bindings using clang2py for the .so library
RUN clang2py -l /app/libwebgpu_dawn.so /app/webgpu.h -o /app/webgpu.py

# Default command (print generated bindings)
CMD ["cat", "/app/webgpu.py"]
