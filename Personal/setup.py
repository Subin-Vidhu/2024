from setuptools import setup, find_packages

setup(
    name="dicom_utils",
    version="0.1.0",
    packages=find_packages(where="Personal"),
    package_dir={"": "Personal"},
    install_requires=[
        "pydicom>=2.3.0",
        "numpy>=1.20.0",
    ],
    author="Your Name",
    author_email="your.email@example.com",
    description="Utilities for extracting and recombining DICOM files",
    keywords="dicom, medical imaging",
) 