from setuptools import setup

setup(
    name="pymec_client",
    version="0.0.1",
    description="Python client for MECRM API",
    author="jme-rs",
    install_requires=["httpx", "attrs"],
    packages=["pymec_client"],
)
