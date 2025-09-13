from setuptools import setup, find_packages

setup(
    name="mimodulo",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "sympy",  # agregá las librerías que tu módulo necesita
        "types"
    ],
    python_requires=">=3.1",
)
