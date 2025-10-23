# utils/hide_output.py
import subprocess
import os

def run_hidden_command(cmd, cwd=None):
    """
    Jalankan command tanpa menampilkan output asli ke terminal.
    Mengembalikan (stdout, stderr, returncode)
    """
    try:
        result = subprocess.run(
            cmd,
            shell=True,
            cwd=cwd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=60  # timeout 60 detik
        )
        return result.stdout, result.stderr, result.returncode
    except subprocess.TimeoutExpired:
        return "", "Command timeout", -1
    except Exception as e:
        return "", str(e), -1
