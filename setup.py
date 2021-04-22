import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="Jetstream--pkg-CR_Jetstream",  # Replace with your own username
    version="0.0.1",
    author="Jet Jabara",
    author_email="cr.jetstream@gmail.com",
    description="Smash Ultimate thumbnail and graphic generator",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/CR-Jetstream/SSBU_Thumbnails",
    project_urls={
        "Bug Tracker": "https://github.com/CR-Jetstream/SSBU_Thumbnails/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.9",
)