from setuptools import setup, find_packages

setup(
    name="pymec",
    version="0.2.2",
    auther="jme-rs",
    description="Python client for MECRM API",
    install_requires=["httpx", "pydantic"],
    tests_require=["pytest", "pytest-asyncio"],
    packages=find_packages(),
)
