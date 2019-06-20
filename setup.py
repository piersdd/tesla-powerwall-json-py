import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="tesla-powerwall-json-py",
    version="0.0.1",
    author="Piers Dawson-Damer",
    author_email="piersdd@eml.cc",
    description="Python module to access local Tesla Powerwall JSON API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/piersdd/tesla-powerwall-json-py",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Topic :: Home Automation",
    ],
)