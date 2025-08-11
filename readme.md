# Netzwerkanalyse tool software

## Introduction

### Goal
The primary goal of this project is to develop a modular network analysis tool that initially enables passive analysis of network traffic and also stores and outputs the collected data in a structured manner based on the MAC address.
The focus here is on expandability through custom protocols defined by JSON files, easy implementation in existing systems, and, as a result, a clearly structured software architecture.

### The Software
<img width="1241" height="911" alt="Screenshot from 2025-08-11 09-21-38" src="https://github.com/user-attachments/assets/1170f3d7-408a-4589-9980-9d15f11f9f41" />
<img width="1241" height="911" alt="Screenshot from 2025-08-11 09-22-10" src="https://github.com/user-attachments/assets/ed28a7f7-5e3f-4a67-a55e-87a715e3fbbe" />
<img width="1241" height="911" alt="Screenshot from 2025-08-11 09-23-01" src="https://github.com/user-attachments/assets/9d92953c-a988-4651-8834-80b0aa55443b" />

## Install

### Clone the repository

```bash
git@github.com:franktronics/netzwerkanalyse-Tool-software.git
```

### Set the environment
You need to have Python 3 installed on your system.

- Set the virtual environment
    ```bash
    python3 -m venv venv
    ```
- Activate the virtual environment
    ```bash
    source venv/bin/activate # Linux
    venv\Scripts\activate # Windows
    ```
- Install the requirements
    ```bash
    pip install -r requirements.txt
    ```
  
### Run the software
Administrator privileges are required to run the software.

```bash
sudo python main.py
```

## Functions
- Start
- Stop
- DataExport (raw data)
- DataImport (raw data)
