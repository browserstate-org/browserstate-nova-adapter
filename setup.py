from setuptools import setup, find_packages

setup(
    name="browserstate-nova-adapter",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "browserstate",
    ],
    extras_require={
        "dev": [
            "pytest>=6.0.0",
            "pytest-cov>=2.10.0",
            "flake8>=3.8.0",
            "black>=20.8b1",
            "isort>=5.0.0",
        ],
        "test": [
            "pytest>=6.0.0",
            "pytest-cov>=2.10.0",
        ],
    },
    author="browserstate-org",
    author_email="info@browserstate.org",
    description="Adapter to use BrowserState with Amazon Nova Act",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/browserstate-org/browserstate-nova-adapter",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
) 