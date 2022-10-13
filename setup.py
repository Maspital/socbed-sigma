from setuptools import setup, find_packages

setup(
    name="socbed-sigma",
    version="1.0.0",
    packages=find_packages("src", exclude=["*tests"]),
    package_dir={"": "src"},
    install_requires=[
        "colorama",
        "paramiko",
        "pyvmomi",
        "veryprettytable",
        "selenium",
        "elasticsearch",
        "elasticsearch-dsl",
        "socbed-sigma"
    ],
    entry_points={
        'console_scripts': [
            'socbed_sigma = socbed_sigma_entry:main',
        ]
    }
)
