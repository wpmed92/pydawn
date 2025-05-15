from setuptools import setup, find_packages
from pathlib import Path
long_description = Path("README.md").read_text()

setup(
    name="dawn-python",
    version="0.2.0",
    author="Ahmed Harmouche",
    author_email="ahmedharmouche92@gmail.com",
    description="A Python interface for the Dawn WebGPU engine.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/wpmed92/pydawn",
    packages=find_packages(),
    platforms="macOS",
    package_data={"pydawn": [
        "lib/libwebgpu_dawn.so", 
        "lib/libwebgpu_dawn_arm.dylib", 
        "lib/libwebgpu_dawn_x86_64.dylib",
        "lib/libwebgpu_dawn.dll",
    ]},
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: MacOS",
        "Operating System :: POSIX :: Linux",
        "License :: OSI Approved :: BSD License",
    ],
    python_requires=">=3.7",
    install_requires=[],
)
