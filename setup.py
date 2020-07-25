import setuptools

setuptools.setup(
    name="automl",
    version="0.0.1",
    author="Joe Kim",
    author_email="joekim987@gmail.com",
    description="Automated model selection via scikit-learn",
    long_description='',
    long_description_content_type="text/markdown",
    url="https://github.com/viriditycapital/automl.git",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)