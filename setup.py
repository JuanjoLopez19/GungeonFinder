#!/usr/bin/python3
# Copyright 2023 AIR Institute
# See LICENSE for details.
# Author: AIR Institute (@AIRInstitute on GitHub)


import io

from setuptools import find_packages, setup


def readme():
    with io.open("README.md", encoding="utf-8") as f:
        return f.read()


def requirements(filename):
    reqs = list()
    with io.open(filename, encoding="utf-8") as f:
        for line in f.readlines():
            reqs.append(line.strip())
    return reqs


setup(
    name="gungeon",
    version="1.0",
    packages=find_packages(),
    license="LICENSE.md",
    author="JuanjoLopez19",
    author_email="juanjoselopez@usal.es",
    description="",
    long_description=readme(),
    long_description_content_type="text/markdown",
    install_requires=requirements(filename="src/requirements.txt"),
    data_files=[],
    entry_points={
        "console_scripts": ["gungeon=src.main:main"],
    },
    include_package_data=True,
    classifiers=[
        "Development Status :: 4 - Beta",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Intended Audience :: Developers",
    ],
    python_requires=">=3",
)
