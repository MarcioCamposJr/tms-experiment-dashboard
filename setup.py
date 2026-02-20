from setuptools import setup, find_packages

setup(
    name="Biomag TMS Experiment Dashboard",
    version="0.1.0",
    description="Web page Graphical User Interface (GUI) for event visualization and control during InVesalius Neuronavigator TMS/EMG experiments.",
    author="Biomag Lab - FFCLRP - USP - Brazil",
    author_email="biomaglab@gmail.com",
    packages=find_packages(),
    install_requires=[
        "nicegui",
        "streamlit",
        "pandas",
        "numpy",
        "matplotlib",
        "python-socketio",
    ],
    python_requires='>=3',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
)
