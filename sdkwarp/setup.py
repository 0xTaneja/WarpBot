from setuptools import setup, find_namespace_packages

# Get all modules and subpackages
packages = find_namespace_packages(include=["*"])

setup(
    name="sdkwarp",
    version="0.1.0",
    description="Python SDK for MultiversX Warps - Refactored Version",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Your Name",
    author_email="your.email@example.com",
    url="https://github.com/yourusername/sdkwarp",
    packages=packages,
    py_modules=["__init__", "__main__", "cli", "client"],
    install_requires=[
        "pydantic>=2.5.0",
        "httpx>=0.25.0",
        "aiohttp>=3.8.0",
        "multiversx-sdk-core>=0.3.0",
        "multiversx-sdk-wallet>=0.6.0",
        "typer>=0.9.0",
        "rich>=13.6.0",
    ],
    extras_require={
        "web": [
            "flask>=2.0.0",
            "fastapi>=0.95.0",
            "uvicorn>=0.22.0",
        ],
        "flask": [
            "flask>=2.0.0",
        ],
        "fastapi": [
            "fastapi>=0.95.0",
            "uvicorn>=0.22.0",
        ],
        "dev": [
            "pytest>=7.4.0",
            "black>=23.7.0",
            "isort>=5.12.0",
            "mypy>=1.5.0",
            "ruff>=0.0.286",
            "pytest-cov>=4.1.0",
        ],
    },
    python_requires=">=3.9",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Internet :: WWW/HTTP",
    ],
    keywords="multiversx, blockchain, warp, sdk",
    project_urls={
        "Documentation": "https://github.com/yourusername/sdkwarp",
        "Source": "https://github.com/yourusername/sdkwarp",
        "Tracker": "https://github.com/yourusername/sdkwarp/issues",
    },
) 