from setuptools import setup, find_packages

setup(
    name="behavior_generation",
    version="0.1.0",
    description="A package for synthetic user and behavior generation",
    packages=find_packages(),
    install_requires=[
        "pandas",
        "faker",
    ],
)
