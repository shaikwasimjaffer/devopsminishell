#!/usr/bin/env bash
# ==============================================================================
# Quick Launch Script for DevOps Mini Shell (Linux / WSL)
# ==============================================================================

echo "Compiling DevOps Mini Shell..."
gcc -Wall -Wextra devops_shell.c -o devops-shell

if [ $? -eq 0 ]; then
    echo "Starting DevOps Mini Shell..."
    ./devops-shell
else
    echo "Compilation failed! Please ensure gcc is installed."
    exit 1
fi
