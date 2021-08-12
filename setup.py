import os

from setuptools import find_packages, setup

here = os.path.abspath(os.path.dirname(__file__))

os.chdir(here)

version_contents = {}
with open(os.path.join(here, "shipengine", "version.py"), encoding="utf-8") as f:
    exec(f.read(), version_contents)

setup(
    name="shipengine",
    version=version_contents["__version__"],
    description="The official Python library for ShipEngine API.",
    author="ShipEngine",
    author_email="support@shipengine.com",
    url="https://www.shipengine.com/",
    packages=find_packages(exclude=["tests", "tests.*"]),
    include_package_data=True,
    license="Apache 2",
    install_requires=[
        "requests >= 2.21.0, <= 2.26.0",
    ],
    project_urls={
        "Bug Tracker": "https://github.com/ShipEngine/shipengine-python/issues",
        "Documentation": "https://github.com/ShipEngine/shipengine-python/tree/main/docs",
        "Source Code": "https://github.com/ShipEngine/shipengine-python",
    },
    test_suite="./tests",
    tests_require=["pytest", "responses"],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    zip_safe=False,
)
