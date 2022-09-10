from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="xunet",
    version="0.0.1",
    author="Pooya Ashtari",
    author_email="pooya.ash@gmail.com",
    description="xunet - PyTorch",
    license="Apache 2.0",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pashtari/xunet",
    project_urls={
        "Bug Tracker": "https://github.com/pashtari/xunet/issues",
        "Source Code": "https://github.com/pashtari/xunet",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Topic :: Scientific/Engineering",
    ],
    keywords=[
        "machine learning",
        "deep learning",
        "image segmentation",
        "medical image segmentation",
        "xunet",
    ],
    packages=find_packages(),
    python_requires=">=3.8",
    install_requires=[
        "xmltodict",
        "pyyaml",
        "numpy",
        "scipy",
        "pandas",
        "scikit-learn",
        "scikit-image",
        "torch",
        "torchvision",
        "pytorch-lightning",
        "pytorch-lightning-bolts",
        "einops",
        "opt_einsum",
        "itk",
        "nibabel",
        "monai",
    ],
)
