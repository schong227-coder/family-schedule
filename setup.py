from setuptools import setup, find_packages

setup(
    name="family-schedule",
    version="0.1.0",
    description="A Streamlit app for managing family shift schedules with Google Sheets integration.",
    author="Steve Hong",
    author_email="schong227@gmail.com",
    packages=find_packages(),
    install_requires=[
        "streamlit",
        "streamlit_gsheets",
        "pandas"
    ],
    entry_points={
        "console_scripts": [
            "family-schedule=family_schedule.app:main"
        ]
    },
    include_package_data=True,
    python_requires=">=3.7",
)