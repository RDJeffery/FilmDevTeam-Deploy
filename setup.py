from setuptools import setup, find_packages

setup(
    name="FilmDevAgency",
    version="0.1",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "agency-swarm",
        "python-dotenv",
        "twilio",
    ],
) 