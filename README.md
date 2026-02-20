# Biomag TMS Experiment Dashboard 

<p align="center">
  <img src="https://github.com/biomaglab.png" width="100px" alt="Logo Biomag">
</p>

> Web-based graphical interface for visualization, control and documenting events during TMS experiments coupled with EMG using neuronavigation with InVesalius.

## 🚀 Quick Installation

### Option 1: With uv (Recommended)

```bash
# Clone source repository
git clone git@github.com:biomaglab/tms-experiment-dashboard.git
cd tms-experiment-dashboard

# Install NiceGUI
uv sync --extra nicegui
```

### Option 2: With pip/venv (Traditional)

```bash
# Clone source repository
git clone git@github.com:biomaglab/tms-experiment-dashboard.git
cd tms-experiment-dashboard

# Create a virtual environment
python -m venv .venv

# Activate the virtual environment
# Windows:
.venv\Scripts\activate
# Linux/Mac:
source .venv/bin/activate

# Install dependencies
pip install -e .

# Install NiceGUI
pip install -e .[nicegui]
```

## ✨ How to Use

### 1. Start the relay server.

**With uv:**
```bash
uv run python scripts/relay_server.py 127.0.0.1 5000
```

**With pip/venv:**
```bash
# Make sure the virtual environment is activated
python scripts/relay_server.py 127.0.0.1 5000
```

### 2. (Optional) Start InVesalius

```bash
python /path/to/invesalius3/app.py --remote-host http://localhost:5000
```

### 3. Start the Dashboard

**With uv:**
```bash
# Automatic detection (NiceGUI)
uv run python main.py
```

**With pip/venv:**
```bash
# Make sure the virtual environment is activated
python main.py
```

### **Acess:**
- NiceGUI: http://localhost:8084

##  Licency

This project is licensed. Check the file. [LICENÇA](LICENSE.md) for further details.

## Supported by NeuroMat

This work is supported by NeuroMat - Centro de Pesquisa, Inovação e Difusão em Neuromatemática (CEPID NeuroMat) established in 2013 at the University of São Paulo (USP). Homepage: http://neuromat.numec.prp.usp.br