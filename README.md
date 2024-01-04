# **Glass Governments**
[https://glassgovernments.com/](https://glassgovernments.com/)

# Description
[https://youtu.be/PBwAxmrE194?si=3F_z09-oXVCaNJum](https://youtu.be/PBwAxmrE194?si=3F_z09-oXVCaNJum)

# Installation
## Setting up environment
### 1. Clone repository
```bash
git clone https://github.com/mikezangus/GlassGovernments.git
cd GlassGovernments
```
### 2. Create virtual environment
#### For conda
```bash
conda create --glassgovernments_env python=3.9.8
conda activate glassgovernments_env
```
#### For venv
##### If on Unix
```bash
python3 -m venv glassgovernments_env
source glassgovernments_env/bin/activate
```
##### If on Windows
```bash
python3 -m venv glassgovernments_env
glassgovernments_env\Scripts\activate
```
### 3. Install dependencies
```bash
pip install -r requirements.txt
```