import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

    setuptools.setup(
        name="nirtools", # Replace with your own username
        version="0.0.1",
        author="Crystina",
        author_email="xzhangbx@gmail.com",
        description="Some small tool functions for nir",
        long_description=long_description,
        long_description_content_type="text/markdown",
        url="https://github.com/crystina-z/nirtools.git",
        packages=setuptools.find_packages(),
        classifiers=[
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent",
        ],
        python_requires='>=3.6',
    )
