import setuptools


setuptools.setup(
    name="horse",
    version="0.1.0",
    url="TODO",

    author="Pragmatic Coders",
    author_email="contact@pragmaticcoders.com",

    description="Handy Open Recommendation Service",
    long_description=open('README.rst').read(),

    packages=setuptools.find_packages(),

    install_requires=[
        'flask==0.11.1'
    ],

    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
    ],
)
