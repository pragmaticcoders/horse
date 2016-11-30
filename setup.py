import os

import setuptools


def read_requirements(filename):
    path = os.path.join(os.path.dirname(__file__), filename)
    with open(path) as f:
        content = f.read()
        return content.split('\n') if content else []


setuptools.setup(
    name="horse",
    version="0.1.0",
    url="TODO",

    author="Pragmatic Coders",
    author_email="contact@pragmaticcoders.com",

    description="Handy Open Recommendation Service",
    long_description=open('README.rst').read(),

    packages=setuptools.find_packages(),

    install_requires=read_requirements('requirements.txt'),

    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
    ],
)
