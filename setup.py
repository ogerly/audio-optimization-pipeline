from setuptools import setup, find_packages
setup(
name="audio-optimization-pipeline",
version="0.1.0",
packages=find_packages(where="src"),
package_dir={"": "src"},
install_requires=[
"soundfile>=0.10.3",
"noisereduce>=2.0.1",
"scipy>=1.7.3",
"pyloudnorm>=0.1.0",
"numpy>=1.21.5",
"psutil>=5.9.0",
"librosa>=0.9.2",
"pydub>=0.25.1",
"python-acoustics>=0.7",
],
extras_require={
"dev": [
"pytest>=7.1.1",
"pytest-cov>=3.0.0",
"black>=22.3.0",
"flake8>=4.0.1",
]
},
author="Your Name",
author_email="your.email@example.com",
description="Eine Pipeline zur Optimierung von Audioaufnahmen mit Fokus auf Performance-Analyse",
long_description=open("README.md").read(),
long_description_content_type="text/markdown",
keywords="audio, optimization, performance, analysis",
url="https://github.com/yourusername/audio-optimization-pipeline",
classifiers=[
"Development Status :: 3 - Alpha",
"Intended Audience :: Developers",
"License :: OSI Approved :: MIT License",
"Programming Language :: Python :: 3.8",
"Programming Language :: Python :: 3.9",
"Programming Language :: Python :: 3.10",
],
python_requires=">=3.8",
)