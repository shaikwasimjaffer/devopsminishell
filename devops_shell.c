/*
 * ============================================================================
 * PROJECT:        DevOps Mini Shell (devops-shell)
 * COURSE:         Operating Systems and System Programming (OSSP)
 * TEAM MEMBERS:   01 Gokul Arnav
 *                 02 Wasim
 *                 03 Binamra
 *                 04 Yogith
 *
 * DESCRIPTION:
 *   A unified command-line toolkit combining common DevOps operations:
 *   - Git & Version Control Operations
 *   - Docker & Container Management
 *   - Build & Deployment Automation (Make, Build, Deploy scripts)
 *   - Process & System Monitoring (ps, free, df, uptime, sysinfo)
 *   - Command Chaining (';' and '&&')
 *   - Automated Workflow Execution (.workflow pipelines)
 *   - Command Execution Logging & History
 *   - Remote Server Operations (SSH)
 *
 * COMPILATION:
 *   Linux / WSL:   gcc devops_shell.c -o devops-shell
 *   Or with Make:  make
 *
 * EXECUTION:
 *   ./devops-shell
 * ============================================================================
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <ctype.h>
#include <errno.h>

/* Platform-specific headers for Operating Systems process management */
#ifdef _WIN32
    #include <windows.h>
    #include <direct.h>
    #include <process.h>
    #include <io.h>
    #define getcwd _getcwd
    #define chdir _chdir
    #define PATH_MAX 260
#else
    #include <unistd.h>
    #include <sys/types.h>
    #include <sys/wait.h>
    #include <sys/stat.h>
    #include <signal.h>
    #include <limits.h>
#endif

/* Buffer size limits */
#define SHELL_MAX_INPUT 1024
#define MAX_ARGS        64
#define MAX_COMMANDS    32
#define MAX_PATH_LEN    1024

/* Log and History files */
#define HISTORY_FILE    ".devops_shell_history"
#define LOG_FILE        "devops_shell.log"

/* ANSI Terminal Color Codes for clear, modern visual presentation */
#define COLOR_RESET     "\033[0m"
#define COLOR_BOLD      "\033[1m"
#define COLOR_CYAN      "\033[36m"
#define COLOR_GREEN     "\033[32m"
#define COLOR_YELLOW    "\033[33m"
#define COLOR_BLUE      "\033[34m"
#define COLOR_MAGENTA   "\033[35m"
#define COLOR_RED       "\033[31m"

/* Structure to store chained commands (e.g., cmd1 && cmd2 ; cmd3) */
typedef struct {
    char command[SHELL_MAX_INPUT];
    int condition; /* 0 = EXECUTE_ALWAYS (;), 1 = EXECUTE_ON_SUCCESS (&&) */
} ChainedCommand;

/* Function Declarations */
void print_banner(void);
void show_help(void);
void trim(char *str);
int parse_arguments(char *input, char *args[]);
void log_command(const char *cmd_line, int exit_code);
void save_history(const char *cmd_line);
void show_history(void);
void show_log(int lines_to_show);
void show_sysinfo(void);
void show_memory(void);
void show_disk(void);
void show_uptime(void);
int execute_external(char *args[]);
int execute_single_command(char *command);
int execute_command_line(char *input);
int run_workflow(const char *filename);
int run_deploy(const char *script_path);
void git_summary(void);
void docker_status(void);
void run_smart_build(void);

#ifndef _WIN32
/* Signal handler for graceful Ctrl+C handling */
void handle_sigint(int sig)
{
    (void)sig;
    printf("\n" COLOR_YELLOW "devops-shell" COLOR_RESET "> ");
    fflush(stdout);
}
#endif

/* ============================================================================
 * STRING UTILITIES
 * ============================================================================ */

/* Remove leading and trailing whitespace from a string */
void trim(char *str)
{
    if (str == NULL) return;

    /* Skip leading whitespace */
    char *start = str;
    while (isspace((unsigned char)*start)) {
        start++;
    }

    if (start != str) {
        memmove(str, start, strlen(start) + 1);
    }

    /* Remove trailing whitespace */
    int len = (int)strlen(str);
    while (len > 0 && isspace((unsigned char)str[len - 1])) {
        str[len - 1] = '\0';
        len--;
    }
}

/*
 * Parse a command string into arguments (argv-style array).
 * Correctly preserves quoted strings: git commit -m "my commit message"
 */
int parse_arguments(char *input, char *args[])
{
    int count = 0;
    char *p = input;

    while (*p && count < MAX_ARGS - 1) {
        /* Skip whitespace */
        while (*p && isspace((unsigned char)*p)) {
            p++;
        }

        if (*p == '\0') {
            break;
        }

        /* Check for quotes (single or double) */
        if (*p == '"' || *p == '\'') {
            char quote = *p++;
            args[count++] = p;
            while (*p && *p != quote) {
                p++;
            }
            if (*p == quote) {
                *p = '\0';
                p++;
            }
        } else {
            args[count++] = p;
            while (*p && !isspace((unsigned char)*p)) {
                p++;
            }
            if (*p) {
                *p = '\0';
                p++;
            }
        }
    }

    args[count] = NULL;
    return count;
}

/* ============================================================================
 * LOGGING & HISTORY MANAGEMENT
 * ============================================================================ */

/* Log every executed command with ISO timestamp and exit status */
void log_command(const char *cmd_line, int exit_code)
{
    FILE *file = fopen(LOG_FILE, "a");
    if (file == NULL) return;

    time_t now = time(NULL);
    struct tm *t = localtime(&now);

    if (t != NULL) {
        fprintf(file, "[%04d-%02d-%02d %02d:%02d:%02d] [EXIT:%3d] %s\n",
                t->tm_year + 1900, t->tm_mon + 1, t->tm_mday,
                t->tm_hour, t->tm_min, t->tm_sec,
                exit_code, cmd_line);
    }
    fclose(file);
}

/* Append command to persistent command history */
void save_history(const char *cmd_line)
{
    if (cmd_line == NULL || strlen(cmd_line) == 0) return;

    FILE *file = fopen(HISTORY_FILE, "a");
    if (file == NULL) return;

    fprintf(file, "%s\n", cmd_line);
    fclose(file);
}

/* Display persistent command history */
void show_history(void)
{
    FILE *file = fopen(HISTORY_FILE, "r");
    if (file == NULL) {
        printf(COLOR_YELLOW "No command history found.\n" COLOR_RESET);
        return;
    }

    printf("\n" COLOR_BOLD COLOR_CYAN "=== Command History ===" COLOR_RESET "\n");
    char line[SHELL_MAX_INPUT];
    int index = 1;

    while (fgets(line, sizeof(line), file)) {
        trim(line);
        if (strlen(line) > 0) {
            printf(" %3d  %s\n", index++, line);
        }
    }
    printf("=======================\n\n");
    fclose(file);
}

/* Display the last N entries of the DevOps execution log */
void show_log(int lines_to_show)
{
    FILE *file = fopen(LOG_FILE, "r");
    if (file == NULL) {
        printf(COLOR_YELLOW "No log file found (" LOG_FILE ").\n" COLOR_RESET);
        return;
    }

    printf("\n" COLOR_BOLD COLOR_CYAN "=== Recent DevOps Shell Logs ===" COLOR_RESET "\n");
    char lines[100][SHELL_MAX_INPUT];
    int total_lines = 0;

    while (fgets(lines[total_lines % 100], sizeof(lines[0]), file)) {
        total_lines++;
    }
    fclose(file);

    int start = 0;
    int count = total_lines;
    if (count > 100) count = 100;
    if (lines_to_show > 0 && lines_to_show < count) {
        start = count - lines_to_show;
    }

    for (int i = start; i < count; i++) {
        printf("%s", lines[i % 100]);
    }
    printf("================================\n\n");
}

/* ============================================================================
 * SYSTEM & PROCESS MONITORING
 * ============================================================================ */

/* Display uptime in a clean, human-readable format */
void show_uptime(void)
{
#ifndef _WIN32
    FILE *file = fopen("/proc/uptime", "r");
    if (file != NULL) {
        double uptime_seconds;
        if (fscanf(file, "%lf", &uptime_seconds) == 1) {
            long total = (long)uptime_seconds;
            long hours = total / 3600;
            long minutes = (total % 3600) / 60;
            long seconds = total % 60;
            printf(COLOR_GREEN "System Uptime: " COLOR_RESET "%ld hours, %ld mins, %ld secs (%.0f seconds total)\n",
                   hours, minutes, seconds, uptime_seconds);
            fclose(file);
            return;
        }
        fclose(file);
    }
    /* Fallback to standard uptime command */
    char *args[] = {"uptime", NULL};
    execute_external(args);
#else
    ULONGLONG ms = GetTickCount64();
    long total = (long)(ms / 1000);
    long hours = total / 3600;
    long minutes = (total % 3600) / 60;
    long seconds = total % 60;
    printf(COLOR_GREEN "System Uptime: " COLOR_RESET "%ld hours, %ld mins, %ld secs\n", hours, minutes, seconds);
#endif
}

/* Display memory utilization */
void show_memory(void)
{
#ifndef _WIN32
    FILE *file = fopen("/proc/meminfo", "r");
    if (file != NULL) {
        char line[256];
        long total_kb = 0, free_kb = 0, avail_kb = 0;

        while (fgets(line, sizeof(line), file)) {
            if (sscanf(line, "MemTotal: %ld kB", &total_kb) == 1) continue;
            if (sscanf(line, "MemFree: %ld kB", &free_kb) == 1) continue;
            if (sscanf(line, "MemAvailable: %ld kB", &avail_kb) == 1) continue;
        }
        fclose(file);

        if (total_kb > 0) {
            long used_kb = total_kb - avail_kb;
            double pct = (double)used_kb / total_kb * 100.0;
            printf(COLOR_BOLD COLOR_CYAN "=== Memory Monitoring (/proc/meminfo) ===" COLOR_RESET "\n");
            printf("  Total Memory:     %8ld MB\n", total_kb / 1024);
            printf("  Used Memory:      %8ld MB (%.1f%%)\n", used_kb / 1024, pct);
            printf("  Available Memory: %8ld MB\n", avail_kb / 1024);
            printf("  Free Memory:      %8ld MB\n", free_kb / 1024);
            printf("=========================================\n");
            return;
        }
    }
    /* Fallback */
    char *args[] = {"free", "-h", NULL};
    execute_external(args);
#else
    MEMORYSTATUSEX statex;
    statex.dwLength = sizeof(statex);
    if (GlobalMemoryStatusEx(&statex)) {
        printf(COLOR_BOLD COLOR_CYAN "=== Memory Monitoring (Windows) ===" COLOR_RESET "\n");
        printf("  Total Physical: %8llu MB\n", statex.ullTotalPhys / (1024 * 1024));
        printf("  Avail Physical: %8llu MB\n", statex.ullAvailPhys / (1024 * 1024));
        printf("  Memory in Use:  %8u%%\n", statex.dwMemoryLoad);
        printf("===================================\n");
    }
#endif
}

/* Display disk filesystem status */
void show_disk(void)
{
#ifndef _WIN32
    char *args[] = {"df", "-h", NULL};
    execute_external(args);
#else
    ULARGE_INTEGER free_bytes_avail, total_bytes, total_free_bytes;
    if (GetDiskFreeSpaceEx(NULL, &free_bytes_avail, &total_bytes, &total_free_bytes)) {
        double total_gb = (double)total_bytes.QuadPart / (1024 * 1024 * 1024);
        double free_gb = (double)free_bytes_avail.QuadPart / (1024 * 1024 * 1024);
        double used_gb = total_gb - free_gb;
        printf(COLOR_BOLD COLOR_CYAN "=== Disk Space Monitoring (Current Drive) ===" COLOR_RESET "\n");
        printf("  Total Size: %.2f GB\n", total_gb);
        printf("  Used Space: %.2f GB (%.1f%%)\n", used_gb, (used_gb / total_gb) * 100.0);
        printf("  Free Space: %.2f GB\n", free_gb);
        printf("=============================================\n");
    }
#endif
}

/* Unified DevOps Dashboard */
void show_sysinfo(void)
{
    printf("\n" COLOR_BOLD COLOR_CYAN "╔══════════════════════════════════════════════════════════════╗" COLOR_RESET "\n");
    printf(COLOR_BOLD COLOR_CYAN "║                 DEVOPS SYSTEM STATUS DASHBOARD               ║" COLOR_RESET "\n");
    printf(COLOR_BOLD COLOR_CYAN "╚══════════════════════════════════════════════════════════════╝" COLOR_RESET "\n");

    /* Current working directory */
    char cwd[MAX_PATH_LEN];
    if (getcwd(cwd, sizeof(cwd)) != NULL) {
        printf(COLOR_YELLOW " Working Directory: " COLOR_RESET "%s\n", cwd);
    }

    /* Uptime */
    printf(" ");
    show_uptime();

    /* Memory summary */
    printf("\n" COLOR_BOLD "[MEMORY STATUS]" COLOR_RESET "\n");
    show_memory();

    /* Git Status quick check */
    printf("\n" COLOR_BOLD "[GIT REPOSITORY STATUS]" COLOR_RESET "\n");
    git_summary();

    /* Docker Daemon quick check */
    printf("\n" COLOR_BOLD "[DOCKER CONTAINER STATUS]" COLOR_RESET "\n");
    docker_status();

    printf("\n");
}

/* ============================================================================
 * DEVOPS OPERATIONS (GIT, DOCKER, BUILD, DEPLOY)
 * ============================================================================ */

/* Quick Git repository summary */
void git_summary(void)
{
    /* Check if .git directory exists */
    struct stat st;
    if (stat(".git", &st) != 0) {
        printf(" Current directory is not a Git repository (.git not found).\n");
        return;
    }

    printf(COLOR_GREEN "--> Git Branch & Status:" COLOR_RESET "\n");
    char *args[] = {"git", "status", "-s", "-b", NULL};
    execute_external(args);

    printf(COLOR_GREEN "--> Recent Commits (Last 3):" COLOR_RESET "\n");
    char *log_args[] = {"git", "log", "--oneline", "-n", "3", NULL};
    execute_external(log_args);
}

/* Quick Docker daemon & container status */
void docker_status(void)
{
    printf(COLOR_GREEN "--> Docker Running Containers:" COLOR_RESET "\n");
    char *args[] = {"docker", "ps", "--format", "table {{.ID}}\t{{.Image}}\t{{.Status}}\t{{.Names}}", NULL};
    int res = execute_external(args);
    if (res != 0) {
        printf(COLOR_YELLOW " Note: Docker daemon is currently not running or not accessible.\n" COLOR_RESET);
    }
}

/* Smart build automation: automatically detects project type and builds */
void run_smart_build(void)
{
    struct stat st;

    printf(COLOR_BOLD COLOR_CYAN "[BUILD AUTOMATION] Detecting build system..." COLOR_RESET "\n");

    /* Check for Makefile */
    if (stat("Makefile", &st) == 0 || stat("makefile", &st) == 0) {
        printf(COLOR_GREEN "Found Makefile. Running 'make'..." COLOR_RESET "\n");
        char *args[] = {"make", NULL};
        execute_external(args);
        return;
    }

    /* Check for CMakeLists.txt */
    if (stat("CMakeLists.txt", &st) == 0) {
        printf(COLOR_GREEN "Found CMakeLists.txt. Running 'cmake --build .'..." COLOR_RESET "\n");
        char *args[] = {"cmake", "--build", ".", NULL};
        execute_external(args);
        return;
    }

    /* Check for package.json (Node.js) */
    if (stat("package.json", &st) == 0) {
        printf(COLOR_GREEN "Found package.json. Running 'npm run build'..." COLOR_RESET "\n");
        char *args[] = {"npm", "run", "build", NULL};
        execute_external(args);
        return;
    }

    /* Check for devops_shell.c (self-compile) */
    if (stat("devops_shell.c", &st) == 0) {
        printf(COLOR_GREEN "Found devops_shell.c. Compiling with gcc..." COLOR_RESET "\n");
        char *args[] = {"gcc", "devops_shell.c", "-o", "devops-shell", NULL};
        int res = execute_external(args);
        if (res == 0) {
            printf(COLOR_GREEN "Successfully built 'devops-shell' binary!\n" COLOR_RESET);
        }
        return;
    }

    printf(COLOR_YELLOW "No recognized build file found (Makefile, CMakeLists.txt, package.json).\n" COLOR_RESET);
    printf("Tip: Run 'make <target>' or specify your compiler command directly.\n");
}

/* Deploy script execution with validation and logging */
int run_deploy(const char *script_path)
{
    if (script_path == NULL || strlen(script_path) == 0) {
        printf(COLOR_RED "Error: No deployment script provided.\n" COLOR_RESET);
        printf("Usage: deploy <script_file>  (e.g., deploy deploy_sample.sh)\n");
        return 1;
    }

    struct stat st;
    if (stat(script_path, &st) != 0) {
        printf(COLOR_RED "Error: Deployment script '%s' does not exist.\n" COLOR_RESET, script_path);
        return 1;
    }

    printf(COLOR_BOLD COLOR_GREEN "\n🚀 [DEPLOY] Starting automated deployment script: %s" COLOR_RESET "\n", script_path);
    printf("─────────────────────────────────────────────────────────────\n");

    int exit_code;
    /* Determine interpreter based on script extension or run directly */
    if (strstr(script_path, ".sh") != NULL) {
        char *args[] = {"bash", (char *)script_path, NULL};
        exit_code = execute_external(args);
    } else if (strstr(script_path, ".py") != NULL) {
        char *args[] = {"python3", (char *)script_path, NULL};
        exit_code = execute_external(args);
    } else {
        char *args[] = {(char *)script_path, NULL};
        exit_code = execute_external(args);
    }

    printf("─────────────────────────────────────────────────────────────\n");
    if (exit_code == 0) {
        printf(COLOR_BOLD COLOR_GREEN "✅ [DEPLOY SUCCESS] Deployment completed successfully (Exit Code: 0)!\n" COLOR_RESET "\n");
    } else {
        printf(COLOR_BOLD COLOR_RED "❌ [DEPLOY FAILED] Deployment exited with error code: %d\n" COLOR_RESET "\n", exit_code);
    }

    return exit_code;
}

/* Workflow automation: runs a multi-step pipeline from a .workflow file */
int run_workflow(const char *filename)
{
    if (filename == NULL || strlen(filename) == 0) {
        printf(COLOR_RED "Error: Workflow file not specified.\n" COLOR_RESET);
        printf("Usage: workflow <pipeline_file> (e.g., workflow ci_pipeline.workflow)\n");
        return 1;
    }

    FILE *file = fopen(filename, "r");
    if (file == NULL) {
        printf(COLOR_RED "Error: Cannot open workflow file '%s': %s\n" COLOR_RESET, filename, strerror(errno));
        return 1;
    }

    printf(COLOR_BOLD COLOR_CYAN "\n══════════════════════════════════════════════════════════════\n");
    printf(" ⚡ EXECUTING DEVOPS WORKFLOW PIPELINE: %s\n", filename);
    printf("══════════════════════════════════════════════════════════════" COLOR_RESET "\n");

    char line[SHELL_MAX_INPUT];
    int step_number = 0;
    int overall_status = 0;

    while (fgets(line, sizeof(line), file)) {
        trim(line);

        /* Skip empty lines and comment lines */
        if (strlen(line) == 0 || line[0] == '#') {
            continue;
        }

        step_number++;
        printf(COLOR_BOLD COLOR_BLUE "\n--> [Step %d] Executing: " COLOR_YELLOW "%s" COLOR_RESET "\n", step_number, line);

        int status = execute_command_line(line);

        if (status == 9999) {
            printf(COLOR_YELLOW "[workflow] Exit command ignored inside pipeline execution.\n" COLOR_RESET);
            continue;
        }

        if (status != 0) {
            printf(COLOR_BOLD COLOR_RED "\n❌ [WORKFLOW ABORTED] Pipeline failed at step %d: '%s' (Status: %d)\n" COLOR_RESET,
                   step_number, line, status);
            overall_status = status;
            break;
        } else {
            printf(COLOR_GREEN "✓ [Step %d Completed Successfully]\n" COLOR_RESET, step_number);
        }
    }

    fclose(file);

    if (overall_status == 0) {
        printf(COLOR_BOLD COLOR_GREEN "\n🎉 ═════════════════════════════════════════════════════════\n");
        printf("   ALL WORKFLOW STEPS (%d) COMPLETED SUCCESSFULLY!\n", step_number);
        printf("═════════════════════════════════════════════════════════" COLOR_RESET "\n\n");
    }

    return overall_status;
}

/* ============================================================================
 * PROCESS EXECUTION ENGINE (OPERATING SYSTEMS CONCEPTS)
 * ============================================================================ */

/*
 * Fork and execute an external process with waitpid.
 * Demonstrates core OS concepts: Process creation (fork), image overlay (execvp),
 * parent process synchronization (waitpid), and termination status evaluation.
 */
int execute_external(char *args[])
{
    if (args[0] == NULL) return 0;

    fflush(stdout);
    fflush(stderr);

#ifndef _WIN32
    pid_t pid = fork();

    if (pid < 0) {
        perror("fork error");
        return 1;
    }

    if (pid == 0) {
        /* Child Process: Replace memory image with target executable */
        execvp(args[0], args);

        /* If execvp returns, the command failed or does not exist */
        fprintf(stderr, COLOR_RED "devops-shell: command not found: %s" COLOR_RESET "\n", args[0]);
        exit(127);
    }

    /* Parent Process: Wait for child process to terminate */
    int status;
    if (waitpid(pid, &status, 0) < 0) {
        perror("waitpid error");
        return 1;
    }

    if (WIFEXITED(status)) {
        return WEXITSTATUS(status);
    }

    if (WIFSIGNALED(status)) {
        printf(COLOR_YELLOW "Process terminated by signal %d" COLOR_RESET "\n", WTERMSIG(status));
        return 128 + WTERMSIG(status);
    }

    return 1;
#else
    /* Windows native compatibility */
    intptr_t ret = _spawnvp(_P_WAIT, args[0], (const char * const *)args);
    if (ret == -1) {
        fprintf(stderr, COLOR_RED "devops-shell: command not found or failed: %s" COLOR_RESET "\n", args[0]);
        return 127;
    }
    return (int)ret;
#endif
}

/*
 * Check if command belongs to supported DevOps toolset
 */
int is_devops_command(const char *cmd)
{
    const char *devops_tools[] = {
        "git", "docker", "make", "deploy", "build", "workflow", "test",
        "ps", "free", "df", "uptime", "sysinfo", "remote",
        /* Standard helpful system & developer utilities */
        "ls", "dir", "cat", "echo", "grep", "curl", "wget", "mkdir",
        "rm", "python", "python3", "node", "npm", "gcc", "clang",
        "ssh", "ping", "top", "kill", "status", "./devops-shell",
        "bash", "sh", "whoami", "which", "head", "tail", "nano", "vim", NULL
    };

    for (int i = 0; devops_tools[i] != NULL; i++) {
        if (strcmp(cmd, devops_tools[i]) == 0) {
            return 1;
        }
    }
    return 0;
}

/*
 * Execute a single command string after separating tokens
 */
int execute_single_command(char *command)
{
    trim(command);
    if (strlen(command) == 0) return 0;

    char buffer[SHELL_MAX_INPUT];
    strncpy(buffer, command, sizeof(buffer) - 1);
    buffer[sizeof(buffer) - 1] = '\0';

    char *args[MAX_ARGS];
    int argc = parse_arguments(buffer, args);
    if (argc == 0) return 0;

    /* --- BUILT-IN COMMANDS --- */

    /* 1. EXIT / QUIT */
    if (strcmp(args[0], "exit") == 0 || strcmp(args[0], "quit") == 0) {
        return 9999;
    }

    /* 2. HELP */
    if (strcmp(args[0], "help") == 0) {
        show_help();
        return 0;
    }

    /* 3. HISTORY */
    if (strcmp(args[0], "history") == 0) {
        show_history();
        return 0;
    }

    /* 4. LOG / SHOWLOG */
    if (strcmp(args[0], "log") == 0 || strcmp(args[0], "showlog") == 0) {
        int lines = (argc > 1) ? atoi(args[1]) : 20;
        show_log(lines);
        return 0;
    }

    /* 5. CLEAR / CLS */
    if (strcmp(args[0], "clear") == 0 || strcmp(args[0], "cls") == 0) {
        printf("\033[2J\033[H");
        return 0;
    }

    /* 6. PWD */
    if (strcmp(args[0], "pwd") == 0) {
        char cwd[MAX_PATH_LEN];
        if (getcwd(cwd, sizeof(cwd)) != NULL) {
            printf("%s\n", cwd);
            return 0;
        }
        perror("pwd error");
        return 1;
    }

    /* 7. CD */
    if (strcmp(args[0], "cd") == 0) {
        const char *dir = args[1];
        if (dir == NULL || strcmp(dir, "~") == 0) {
            dir = getenv("HOME");
            if (dir == NULL) dir = "/";
        }
        if (chdir(dir) != 0) {
            printf(COLOR_RED "cd: %s: %s\n" COLOR_RESET, dir, strerror(errno));
            return 1;
        }
        return 0;
    }

    /* 8. SYSINFO / STATUS */
    if (strcmp(args[0], "sysinfo") == 0 || strcmp(args[0], "status") == 0) {
        show_sysinfo();
        return 0;
    }

    /* 9. BUILTIN MONITORING COMMANDS */
    if (strcmp(args[0], "uptime") == 0) {
        show_uptime();
        return 0;
    }

    if (strcmp(args[0], "free") == 0 || strcmp(args[0], "memory") == 0) {
        show_memory();
        return 0;
    }

    if (strcmp(args[0], "df") == 0 || strcmp(args[0], "disk") == 0) {
        show_disk();
        return 0;
    }

    /* 10. BUILD AUTOMATION */
    if (strcmp(args[0], "build") == 0) {
        run_smart_build();
        return 0;
    }

    /* 11. DEPLOY */
    if (strcmp(args[0], "deploy") == 0) {
        return run_deploy(args[1]);
    }

    /* 12. WORKFLOW */
    if (strcmp(args[0], "workflow") == 0) {
        return run_workflow(args[1]);
    }

    /* 13. REMOTE (SSH Command Execution) */
    if (strcmp(args[0], "remote") == 0) {
        if (args[1] == NULL || args[2] == NULL) {
            printf("Usage: remote <user@host> <command>\n");
            printf("Example: remote user@server.com uptime\n");
            return 1;
        }
        char *ssh_args[MAX_ARGS];
        int idx = 0;
        ssh_args[idx++] = "ssh";
        ssh_args[idx++] = args[1];
        for (int i = 2; args[i] != NULL && idx < MAX_ARGS - 1; i++) {
            ssh_args[idx++] = args[i];
        }
        ssh_args[idx] = NULL;
        return execute_external(ssh_args);
    }

    /* 14. GIT SUMMARY SHORTCUT */
    if (strcmp(args[0], "git") == 0 && args[1] != NULL && strcmp(args[1], "summary") == 0) {
        git_summary();
        return 0;
    }

    /* 15. DOCKER STATUS SHORTCUT */
    if (strcmp(args[0], "docker") == 0 && args[1] != NULL && strcmp(args[1], "status") == 0) {
        docker_status();
        return 0;
    }

    /* Command validation against DevOps whitelist */
    if (!is_devops_command(args[0])) {
        printf(COLOR_YELLOW "Notice: '%s' is not in standard DevOps toolset.\n" COLOR_RESET, args[0]);
        printf("Type " COLOR_BOLD "'help'" COLOR_RESET " to view supported DevOps commands.\n");
    }

    /* Dispatch to external process */
    return execute_external(args);
}

/*
 * Command chaining engine:
 * Supports ';' (unconditional sequence) and '&&' (conditional execution on success)
 * Example: git status ; make
 * Example: git pull && make && deploy deploy_sample.sh
 */
int execute_command_line(char *input)
{
    trim(input);
    if (strlen(input) == 0) return 0;

    ChainedCommand commands[MAX_COMMANDS];
    int cmd_count = 0;

    int len = (int)strlen(input);
    int start = 0;
    int next_condition = 0; /* 0 = always, 1 = on previous success */

    for (int i = 0; i <= len && cmd_count < MAX_COMMANDS; i++) {
        int is_semi = (input[i] == ';');
        int is_and  = (input[i] == '&' && i + 1 < len && input[i + 1] == '&');
        int is_end  = (input[i] == '\0');

        if (is_semi || is_and || is_end) {
            int cmd_len = i - start;
            if (cmd_len > 0 && cmd_len < SHELL_MAX_INPUT) {
                strncpy(commands[cmd_count].command, input + start, cmd_len);
                commands[cmd_count].command[cmd_len] = '\0';
                trim(commands[cmd_count].command);
                commands[cmd_count].condition = next_condition;
                cmd_count++;
            }

            if (is_semi) {
                next_condition = 0; /* ';' = execute next always */
                start = i + 1;
            } else if (is_and) {
                next_condition = 1; /* '&&' = execute next only if current succeeds */
                start = i + 2;
                i++; /* Skip second '&' */
            }
        }
    }

    int last_status = 0;

    for (int i = 0; i < cmd_count; i++) {
        /* Check condition for && */
        if (commands[i].condition == 1 && last_status != 0) {
            printf(COLOR_YELLOW "[chain] Skipping '%s' because previous command failed (status: %d)\n" COLOR_RESET,
                   commands[i].command, last_status);
            continue;
        }

        last_status = execute_single_command(commands[i].command);

        /* Check if user requested shell exit */
        if (last_status == 9999) {
            return 9999;
        }
    }

    return last_status;
}

/* ============================================================================
 * USER INTERFACE & HELP DISPLAY
 * ============================================================================ */

/* Display interactive shell banner */
void print_banner(void)
{
    printf("\n");
    printf(COLOR_BOLD COLOR_CYAN "╔══════════════════════════════════════════════════════════════════════╗\n");
    printf("║                         DEVOPS MINI SHELL                            ║\n");
    printf("║             Operating Systems and System Programming                 ║\n");
    printf("╠══════════════════════════════════════════════════════════════════════╣\n");
    printf("║  Team Members:                                                       ║\n");
    printf("║    01 Gokul Arnav   02 Wasim   03 Binamra   04 Yogith                ║\n");
    printf("╚══════════════════════════════════════════════════════════════════════╝" COLOR_RESET "\n");
    printf(COLOR_GREEN "✓ Unified DevOps Environment Initialized." COLOR_RESET "\n");
    printf("Type " COLOR_BOLD COLOR_YELLOW "help" COLOR_RESET " for all commands, or " COLOR_BOLD COLOR_YELLOW "exit" COLOR_RESET " to quit.\n\n");
}

/* Display comprehensive help manual */
void show_help(void)
{
    printf("\n" COLOR_BOLD COLOR_CYAN "======================================================================\n");
    printf("                       DEVOPS MINI SHELL REFERENCE                    \n");
    printf("======================================================================" COLOR_RESET "\n");

    printf("\n" COLOR_BOLD COLOR_GREEN "1. CORE SHELL COMMANDS" COLOR_RESET "\n");
    printf("   help                         Show this command reference\n");
    printf("   sysinfo / status             Show unified DevOps & System dashboard\n");
    printf("   history                      Display command history\n");
    printf("   log [N]                      Show last N execution log entries\n");
    printf("   pwd                          Print current working directory\n");
    printf("   cd <dir>                     Change directory (supports cd ~, cd ..)\n");
    printf("   clear / cls                  Clear the terminal screen\n");
    printf("   exit / quit                  Exit the DevOps Mini Shell\n");

    printf("\n" COLOR_BOLD COLOR_GREEN "2. GIT & VERSION CONTROL OPERATIONS" COLOR_RESET "\n");
    printf("   git status                   Show repository working tree status\n");
    printf("   git summary                  Quick overview of branch and last commits\n");
    printf("   git log                      Show commit history\n");
    printf("   git diff                     Show tracked file modifications\n");
    printf("   git add <files>              Stage files for commit\n");
    printf("   git commit -m \"<msg>\"        Commit staged changes with message\n");
    printf("   git push / git pull          Synchronize with remote repository\n");

    printf("\n" COLOR_BOLD COLOR_GREEN "3. DOCKER & CONTAINER OPERATIONS" COLOR_RESET "\n");
    printf("   docker ps                    List active running containers\n");
    printf("   docker ps -a                 List all containers (running & stopped)\n");
    printf("   docker images                List local container images\n");
    printf("   docker status                Quick Docker daemon & container check\n");
    printf("   docker build -t <tag> .      Build a container image\n");
    printf("   docker run <image>           Run a container\n");

    printf("\n" COLOR_BOLD COLOR_GREEN "4. BUILD & DEPLOYMENT AUTOMATION" COLOR_RESET "\n");
    printf("   build                        Smart build: auto-detects Makefile/CMake/npm\n");
    printf("   make [target]                Execute Makefile build targets\n");
    printf("   deploy <script>              Execute deployment script (e.g. deploy.sh)\n");

    printf("\n" COLOR_BOLD COLOR_GREEN "5. PROCESS & SYSTEM MONITORING" COLOR_RESET "\n");
    printf("   uptime                       Show system uptime and running duration\n");
    printf("   free / memory                Show memory usage and availability\n");
    printf("   df / disk                    Show filesystem disk storage\n");
    printf("   ps [options]                 Monitor processes (e.g. ps aux)\n");

    printf("\n" COLOR_BOLD COLOR_GREEN "6. WORKFLOW & REMOTE AUTOMATION" COLOR_RESET "\n");
    printf("   workflow <file.workflow>     Run multi-step CI/CD pipeline from file\n");
    printf("   remote <user@host> <cmd>     Execute command on remote server via SSH\n");

    printf("\n" COLOR_BOLD COLOR_GREEN "7. COMMAND CHAINING" COLOR_RESET "\n");
    printf("   cmd1 ; cmd2                  Run cmd1, then run cmd2\n");
    printf("   cmd1 && cmd2                 Run cmd2 ONLY IF cmd1 succeeds\n");
    printf("   Example:                     git status && make && deploy deploy_sample.sh\n");

    printf("\n" COLOR_BOLD COLOR_CYAN "======================================================================\n\n" COLOR_RESET);
}

/* ============================================================================
 * MAIN REPL LOOP
 * ============================================================================ */

int main(void)
{
#ifndef _WIN32
    /* Install signal handler for graceful Ctrl+C */
    signal(SIGINT, handle_sigint);
#endif

    print_banner();

    char input[SHELL_MAX_INPUT];
    char cwd[MAX_PATH_LEN];

    while (1) {
        /* Retrieve current working directory */
        if (getcwd(cwd, sizeof(cwd)) == NULL) {
            strcpy(cwd, "?");
        }

        /* Interactive prompt */
        printf(COLOR_BOLD COLOR_CYAN "devops:" COLOR_YELLOW "%s" COLOR_CYAN "$ " COLOR_RESET, cwd);
        fflush(stdout);

        /* Read user input */
        if (fgets(input, sizeof(input), stdin) == NULL) {
            printf("\n");
            break; /* End of File (Ctrl+D) */
        }

        /* Remove trailing newline character */
        input[strcspn(input, "\r\n")] = '\0';
        trim(input);

        /* Skip empty lines */
        if (strlen(input) == 0) {
            continue;
        }

        /* Record command into persistent history and log */
        save_history(input);

        /* Execute command line (handles chaining and built-ins) */
        int result = execute_command_line(input);

        /* Log execution result */
        log_command(input, result);

        /* Check for shell termination */
        if (result == 9999) {
            break;
        }
    }

    printf(COLOR_BOLD COLOR_GREEN "\nExiting DevOps Mini Shell. Goodbye!\n" COLOR_RESET);
    return 0;
}
