import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

requirements = [
    'pydantic',
    'pymongo'
]

setuptools.setup(
    name="mogger",
    version="0.0.1",
    author="Nouzan@AshWorkshop",
    author_email="clobraindie@outlook.com",
    description="A data model for logging(in MongoDB)",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/AshWorkshop",
    packages=setuptools.find_packages(),
    install_requires=requirements,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    # entry_points={
    #     'console_scripts': [
    #         'pyrmq = pyrmq.__main__:main'
    #     ]
    # }
)