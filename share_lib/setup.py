from setuptools import setup, find_packages

setup(
    name="share-lib",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "PyJWT==2.10.1",
        "cryptography==45.0.5"
    ]
)
