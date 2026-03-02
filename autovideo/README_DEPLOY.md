# Deploy AutoVideo to Ubuntu 4090 Server

This guide explains how to package your local Windows project and deploy it to a remote Ubuntu server.

## 1. Package Local Project (Windows)

Run the included packaging script to create a clean zip file (excludes `venv`, `__pycache__`, etc.).

```powershell
python project_packer.py
```

This will generate a file like `autovideo_deploy_20231027_120000.zip`.

## 2. Upload to Server

Use `scp` or any SFTP client (like WinSCP) to upload the zip file to your server.

```bash
# Example using SCP (run on Windows)
scp autovideo_deploy_*.zip username@your_server_ip:~/
```

## 3. Setup on Server (Ubuntu)

Connect to your server and run the following commands:

1. **Unzip the project**:
   ```bash
   unzip autovideo_deploy_*.zip -d autovideo
   cd autovideo
   ```

2. **Run Setup Script**:
   This script installs system dependencies (FFmpeg, Manim, Fonts) and sets up the Python virtual environment.
   ```
   chmod +x setup_linux.sh
   ./setup_linux.sh
   ```

## 4. Verify & Run

Activate the environment and run a test build.

```bash
source venv/bin/activate
python pipeline.py build --project projects/number1 --skip-rvc
```

> **Note on RVC**: The Voice Conversion (RVC) module requires a separate RVC-WebUI server. If you haven't set that up on the server, use `--skip-rvc` to disable it, or set `rvc: enabled: false` in `config.yaml`.
