import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()


setuptools.setup(
    # we don't intend to upload this to PyPi, so don't worry too much about
    # name, version etc
    name="surf_data",
    version="0.0.1",
    description="Log surf sessions and get local wave and tide conditions",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/andrew-candela/surf_scraper",
    packages=setuptools.find_packages(),
    python_requires='>=3.9',
    # package_dir={"": "src/surf_data"}
)
