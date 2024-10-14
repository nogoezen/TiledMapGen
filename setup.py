from setuptools import setup, find_packages

setup(
    name="tiled_map_generator",
    version="0.1",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    install_requires=[
        "PyQt5==5.15.6",
    ],
    entry_points={
        "console_scripts": [
            "tiled_map_generator=tiled_map_generator.gui:run_app",
        ],
    },
)
