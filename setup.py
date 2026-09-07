from setuptools import find_packages, setup

setup(
    name="hotel-ai-recommender",
    version="0.1.0",
    description="AI Hotel Recommendation & Price Prediction System",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    include_package_data=True,
    install_requires=[
        "pandas>=2.2.0",
        "numpy>=1.26.0",
        "scikit-learn>=1.4.0",
        "fastapi>=0.110.0",
        "uvicorn[standard]>=0.29.0",
        "streamlit>=1.35.0",
        "pydantic>=2.7.0",
        "kaggle>=1.6.17",
    ],
)
