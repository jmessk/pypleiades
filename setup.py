from setuptools import setup

setup(
    name="pymec",
    version="0.0.1",
    description="Python client for MECRM API",
    author="jme-rs",
    install_requires=["httpx", "attrs", "result"],
    packages=["pymec_client"],
)
