from setuptools import setup, find_packages

setup(
    name="pymec",
    version="0.2.2",
    auther="jme-rs",
    description="Python client for MECRM API",
    install_requires=["httpx", "attrs>=23.2.0", "result", "pydantic", "aiofiles"],
    tests_require=["pytest", "pytest-asyncio"],
    packages=find_packages(),
)
