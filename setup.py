from setuptools import setup, find_packages
from pathlib import Path
import platform

long_description = Path("README.md").read_text()

if platform.system() == "Darwin":
    package_data = {"pydawn": ["lib/libwebgpu_dawn.dylib"]}
elif platform.system() == "Linux":
    package_data = {"pydawn": ["lib/libwebgpu_dawn.so"]}
else:
    raise RuntimeError("Unsupported platform")

setup(
    name="dawn-python",
    version="0.1.4",
    author="Ahmed Harmouche",
    author_email="ahmedharmouche92@gmail.com",
    description="A Python interface for the Dawn WebGPU engine.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/wpmed92/pydawn",
    packages=find_packages(),
    platforms="macOS",
    package_data=package_data,
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: MacOS",
        "Operating System :: POSIX :: Linux",
        "License :: OSI Approved :: BSD License",
    ],
    python_requires=">=3.7",
    install_requires=[],
)
