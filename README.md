# DevOps Mini Shell (`devops-shell`)

**Course:** Operating Systems and System Programming (OSSP)  
**Project Title:** DevOps Mini Shell  
**Team Members:**
1. Gokul Arnav (01)
2. Wasim (02)
3. Binamra (03)
4. Yogith (04)

---

## 📌 Project Overview & Abstract

The **DevOps Mini Shell** is a unified command-line toolkit and specialized UNIX/POSIX shell environment designed to simplify and combine routine DevOps operations into a single interface. 

Instead of juggling disparate tools with varying syntaxes, developers and system administrators can execute Git commands, Docker containers, automated builds, deployments, workflow pipelines, and live system monitoring directly from one coherent shell.

---

## 🎯 Problem Statement & Motivation

DevOps engineers and students often need to manage multiple disconnected utilities:
- **Version Control:** `git status`, `git commit`, `git pull`, `git push`
- **Containers:** `docker ps`, `docker images`, `docker run`, `docker build`
- **Builds:** `make`, `gcc`, build scripts
- **Deployment:** Custom shell scripts, release steps
- **System Monitoring:** `ps`, `free`, `df`, `uptime`

Managing these through different tools can slow down common workflows and increase cognitive load. The **DevOps Mini Shell** addresses this problem by providing:
1. A **single unified command line** for common DevOps tasks.
2. Built-in **command chaining** (`cmd1 ; cmd2` and `cmd1 && cmd2`).
3. **Automated CI/CD Workflow pipelines** via `.workflow` execution.
4. **Command history and audit logging** with timestamps and exit statuses.
5. High-level DevOps status overview with the `sysinfo` / `status` dashboard.

---

## 🏗️ Architecture & Operating Systems Concepts

The DevOps Mini Shell is implemented in pure **C** and illustrates fundamental OS and System Programming concepts:

```
                      +-----------------------------+
                      |   User Input (Terminal)     |
                      +--------------+--------------+
                                     |
                                     v
                      +-----------------------------+
                      | Command Chaining & Parsing  |
                      |  - ';' (unconditional)      |
                      |  - '&&' (conditional)       |
                      |  - Argument & Quote Parser  |
                      +--------------+--------------+
                                     |
                 +-------------------+-------------------+
                 |                                       |
                 v                                       v
      [ Built-In Shell Engine ]              [ External Process Engine ]
      - help, sysinfo, status                - Process Creation: fork()
      - cd, pwd, clear, history              - Execution: execvp()
      - log, workflow, deploy                - Synchronization: waitpid()
      - free, uptime, df                     - Exit status: WIFEXITED, etc.
                 |                                       |
                 +-------------------+-------------------+
                                     |
                                     v
                      +-----------------------------+
                      | Audit Log & History Engine  |
                      |  - .devops_shell_history    |
                      |  - devops_shell.log         |
                      +-----------------------------+
```

### Key OS Principles Implemented:
1. **Process Management & Creation (`fork`)**:
   - The shell creates child processes using the `fork()` system call to execute external DevOps commands safely without terminating the shell.
2. **Process Image Replacement (`execvp`)**:
   - The child process replaces its address space with the target binary using `execvp()`, preserving environment variables and arguments.
3. **Parent Process Synchronization (`waitpid`)**:
   - The parent shell waits for child processes to finish using `waitpid()`, evaluating return codes (`WIFEXITED`, `WEXITSTATUS`, `WTERMSIG`) to support conditional chaining (`&&`).
4. **Signal Handling (`signal`)**:
   - Catches `SIGINT` (Ctrl+C) gracefully so the shell does not abort accidentally during user interaction.
5. **File I/O & Audit Logging**:
   - Uses persistent file streams to maintain `.devops_shell_history` and timestamped execution logs in `devops_shell.log`.
6. **Quote-Aware Tokenization**:
   - Parses arguments while preserving quoted parameters (e.g., `git commit -m "initial commit"`).

---

## 🚀 Features & Commands Reference

| Category | Command | Description |
|---|---|---|
| **Core Shell** | `help` | Displays the interactive reference manual |
| | `sysinfo` / `status` | Unified system, memory, git, and docker dashboard |
| | `history` | Displays numbered history of executed commands |
| | `log [N]` | Displays recent entries from `devops_shell.log` |
| | `pwd` | Prints current working directory |
| | `cd <directory>` | Changes working directory (supports `cd ~`, `cd ..`) |
| | `clear` / `cls` | Clears terminal screen |
| | `exit` / `quit` | Exits the shell cleanly |
| **Git Operations** | `git status` | Displays working tree status |
| | `git summary` | Built-in summary: active branch and latest 3 commits |
| | `git log` | Displays repository commit history |
| | `git add <files>` | Stages modified files |
| | `git commit -m "<msg>"` | Creates a commit with the provided message |
| | `git push` / `git pull` | Synchronizes with remote repositories |
| **Docker Operations** | `docker ps` | Lists active running containers |
| | `docker ps -a` | Lists all containers (active and stopped) |
| | `docker images` | Lists local container images |
| | `docker status` | Built-in status check for Docker daemon and containers |
| | `docker build / run` | Builds container images and launches containers |
| **Build & Deploy** | `build` | Smart builder: auto-detects Makefile, CMake, or npm |
| | `make [target]` | Executes build targets from Makefile |
| | `deploy <script>` | Runs deployment script with logging and status check |
| **System Monitoring** | `uptime` | Human-readable system uptime |
| | `free` / `memory` | Memory utilization from `/proc/meminfo` |
| | `df` / `disk` | Filesystem storage and disk space utilization |
| | `ps [args]` | Process monitoring (e.g., `ps aux`) |
| **Automation** | `workflow <file>` | Runs sequential CI/CD pipeline from `.workflow` file |
| | `remote <user@host> <cmd>` | Executes remote commands via SSH |
| **Chaining** | `cmd1 ; cmd2` | Runs `cmd1`, then unconditionally runs `cmd2` |
| | `cmd1 && cmd2` | Runs `cmd2` only if `cmd1` succeeds (exit status 0) |

---

## 🛠️ Compilation & Execution

### Option 1: Linux / WSL (Recommended)
Compile directly with GCC:
```bash
gcc -Wall -Wextra devops_shell.c -o devops-shell
./devops-shell
```

Or run via the provided launch script:
```bash
chmod +x run.sh
./run.sh
```

### Option 2: Using Makefile
```bash
# Compile binary
make

# Run interactive shell
make run

# Run automated smoke test suite
make test

# Clean artifacts
make clean
```

### Option 3: Windows (Command Prompt / PowerShell)
Double-click `run.bat` or run:
```cmd
run.bat
```
*(Automatically detects WSL Ubuntu or native Windows GCC).*

---

## 🧪 Demonstration & Examples

### 1. Unified System Status (`sysinfo`):
```text
devops:/workspace$ sysinfo

╔══════════════════════════════════════════════════════════════╗
║                 DEVOPS SYSTEM STATUS DASHBOARD               ║
╚══════════════════════════════════════════════════════════════╝
 Working Directory: /workspace
 System Uptime: 2 hours, 14 mins, 10 secs

[MEMORY STATUS]
=== Memory Monitoring (/proc/meminfo) ===
  Total Memory:         7748 MB
  Used Memory:           650 MB (8.4%)
  Available Memory:     7097 MB
  Free Memory:          6482 MB
=========================================

[GIT REPOSITORY STATUS]
--> Git Branch & Status:
## master...origin/master
--> Recent Commits (Last 3):
a1b2c3d feat: add workflow automation

[DOCKER CONTAINER STATUS]
--> Docker Running Containers:
CONTAINER ID   IMAGE     STATUS    NAMES
```

### 2. Command Chaining:
```bash
# Unconditional sequential execution
devops:$ uptime ; pwd

# Conditional execution: runs make only if git succeeds
devops:$ git status && make && deploy deploy_sample.sh
```

### 3. Automated Workflow Pipeline:
Create a `.workflow` file (e.g. `ci_pipeline.workflow`):
```bash
# CI/CD Pipeline
uptime
free
pwd
history
```
Execute inside the shell:
```bash
devops:$ workflow ci_pipeline.workflow
```

### 4. Automated Deployment Script Execution:
```bash
devops:$ deploy deploy_sample.sh
```

---

## 📁 Project File Structure

```
ossp project/
│
├── devops_shell.c             # Core shell source code in C (POSIX & Win32 compatible)
├── Makefile                   # Build automation configuration
├── ci_pipeline.workflow       # Sample CI/CD pipeline definition
├── deploy_sample.sh           # Sample deployment script
├── run.sh                     # Linux / WSL one-click execution script
├── run.bat                    # Windows one-click execution script
├── DevOps-Mini-Shell.pptx     # Project presentation slides
└── README.md                  # Comprehensive documentation and manual
```

---

## 👥 Credits
Developed for **Operating Systems and System Programming (OSSP)** course project by:
- **Gokul Arnav** (01)
- **Wasim** (02)
- **Binamra** (03)
- **Yogith** (04)
