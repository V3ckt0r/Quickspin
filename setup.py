from distutils.core import setup

setup(
    # Application name:
    name="Quickspin",

    # Version number (initial):
    version="0.1.5",

    # Application author details:
    author="V3ckt0r",
    author_email="",

    # Packages
    packages=["Quickspin"],

    # Include additional files into the package
    include_package_data=True,

    entry_points={
            'console_scripts': [
                'quickspin = Quickspin.quickspin:main',
            ]
    },

    # Details
    url="https://github.com/V3ckt0r/Quickspin",

    #
    license="LICENSE.txt",
    description="Quickspin CLI tool for managing AWS resources",

    long_description=open("DESCRIPTION.rst").read(),

    # Dependent packages (distributions)
    install_requires=[
        "boto3",
    ],
)
