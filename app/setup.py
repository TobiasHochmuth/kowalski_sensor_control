#!/usr/bin/env python3

import os
import ssl

from setuptools import setup

# Ignore ssl if it fails
if not os.environ.get("PYTHONHTTPSVERIFY", "") and getattr(ssl, "_create_unverified_context", None):
    ssl._create_default_https_context = ssl._create_unverified_context

setup(
    name="sensor-reading",
    version="0.0.1",
    description="Extension for reading various sensors necessary for kowalski",
    license="MIT",
    install_requires=[
        "loguru == 0.5.3",
    ],
)