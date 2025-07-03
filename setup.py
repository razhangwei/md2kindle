#!/usr/bin/env python3
from setuptools import setup, find_packages

setup(
    name="md2kindle",
    version="0.1.0",
    description="Convert Markdown files to Kindle format and send to device",
    author="Wei",
    author_email="your.email@example.com",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "python-dotenv>=1.0.0",
        "pypandoc>=1.12",
    ],
    entry_points={
        "console_scripts": [
            "md2kindle=md2kindle.cli:main",
        ],
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Console",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Topic :: Text Processing :: Markup",
    ],
)