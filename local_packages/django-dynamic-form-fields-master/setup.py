# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

with open('README.md', 'r') as f:
    long_description = f.read()

setup(
    name="django-dynamic-form-fields",
    version="0.2.0",
    url="https://gitlab.com/dannosaur/django-dynamic-form-fields",
    description="Dynamically update choice fields based on dependent fields in django",
    long_description=long_description,
    long_description_conent_type='text/markdown',
    author="dannosaur",
    author_email="me@dannosaur.com",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'django>=1.11',
    ],
    python_requires='>=3.5',
)
