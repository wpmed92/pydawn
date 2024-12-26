# Use the latest Ubuntu LTS as the base image
FROM ubuntu:22.04

# Set the working directory
WORKDIR /usr/src

# Install essential dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    git \
    cmake \
    python3 \
    python3-pip \
    curl \
    libx11-dev \
    libx11-xcb-dev \
    libgl1-mesa-dev \
    libxrandr-dev \
    libxinerama-dev \
    libxcursor-dev \
    libxi-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Vulkan SDK with error handling
RUN curl -LO https://sdk.lunarg.com/sdk/download/1.3.261.1/linux/vulkan-sdk.tar.gz
RUN tar -xf vulkan-sdk.tar.gz
RUN mv 1.3.261.1 /usr/local/vulkan-sdk
RUN rm vulkan-sdk.tar.gz

# Set Vulkan environment variables
ENV VULKAN_SDK=/usr/local/vulkan-sdk/x86_64
ENV PATH=$VULKAN_SDK/bin:$PATH
ENV LD_LIBRARY_PATH=$VULKAN_SDK/lib
ENV VK_ICD_FILENAMES=$VULKAN_SDK/etc/vulkan/icd.d
ENV VK_LAYER_PATH=$VULKAN_SDK/etc/vulkan/explicit_layer.d

# Clone the Dawn repository
RUN git clone https://dawn.googlesource.com/dawn

# Set working directory to Dawn
WORKDIR /usr/src/dawn

# Configure and build Dawn with Vulkan backend
RUN cmake -S . -B out/Release \
    -DDAWN_FETCH_DEPENDENCIES=ON \
    -DDAWN_ENABLE_INSTALL=ON \
    -DCMAKE_BUILD_TYPE=Release \
    -DAWN_ENABLE_BACKEND_VULKAN=ON && \
    cmake --build out/Release --target install

# Install the build artifacts
RUN cmake --install out/Release --prefix /usr/src/dawn/install/Release

# Clean up unnecessary files to reduce image size
RUN rm -rf /var/lib/apt/lists/* /usr/src/dawn/out
