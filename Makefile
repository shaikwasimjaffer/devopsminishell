# ==============================================================================
# Makefile for DevOps Mini Shell
# Course: Operating Systems and System Programming Project
# Team:   Gokul Arnav, Wasim, Binamra, Yogith
# ==============================================================================

CC = gcc
CFLAGS = -Wall -Wextra -O2
TARGET = devops-shell
SRC = devops_shell.c

all: $(TARGET)

$(TARGET): $(SRC)
	$(CC) $(CFLAGS) $(SRC) -o $(TARGET)
	@echo "Build complete: $(TARGET)"

run: $(TARGET)
	./$(TARGET)

test: $(TARGET)
	@echo "Running automated smoke test suite..."
	@printf "help\npwd\nuptime\nfree\ndf\nhistory\nlog 5\nexit\n" | ./$(TARGET)
	@echo "All smoke tests executed successfully!"

clean:
	rm -f $(TARGET) devops_shell.log .devops_shell_history
	@echo "Cleaned build artifacts, logs, and history."

help:
	@echo "DevOps Mini Shell - Build Targets:"
	@echo "  make         - Compile the shell binary"
	@echo "  make run     - Compile and launch interactive shell"
	@echo "  make test    - Run automated test suite"
	@echo "  make clean   - Remove compiled binary, logs, and history"
