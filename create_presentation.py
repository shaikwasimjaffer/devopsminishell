import sys
import os
import pptx
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE

def build_presentation(output_path):
    prs = pptx.Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    # Theme Colors
    C_NAVY_DARK   = RGBColor(15, 23, 42)     # #0F172A (Deep Slate/Navy)
    C_NAVY_LIGHT  = RGBColor(30, 41, 59)     # #1E293B
    C_CYAN_ACCENT = RGBColor(14, 165, 233)   # #0EA5E9 (Cyan / Sky)
    C_CYAN_LIGHT  = RGBColor(224, 242, 254)  # #E0F2FE (Light Cyan)
    C_EMERALD     = RGBColor(16, 185, 129)   # #10B981 (Success Green)
    C_AMBER       = RGBColor(245, 158, 11)   # #F59E0B (Warning Amber)
    C_ROSE        = RGBColor(244, 63, 94)    # #F43F5E (Alert Rose)
    C_BG_LIGHT    = RGBColor(248, 250, 252)  # #F8FAFC (Clean Light Grey)
    C_CARD_BG     = RGBColor(255, 255, 255)  # White Card
    C_CARD_BORDER = RGBColor(226, 232, 240)  # #E2E8F0 (Card Border)
    C_TEXT_DARK   = RGBColor(15, 23, 42)     # #0F172A
    C_TEXT_MUTED  = RGBColor(100, 116, 139)  # #64748B
    C_TEXT_LIGHT  = RGBColor(255, 255, 255)  # Pure White
    C_CODE_BG     = RGBColor(30, 41, 59)     # #1E293B Terminal Dark
    C_CODE_GREEN  = RGBColor(52, 211, 153)   # #34D399 Bright Terminal Green

    def set_slide_background(slide, color):
        background = slide.background
        fill = background.fill
        fill.solid()
        fill.fore_color.rgb = color

    def add_header(slide, title_text, category_badge="OSSP PROJECT", subtitle_text=None):
        # Category Badge
        badge = slide.shapes.add_shape(
            MSO_SHAPE.ROUNDED_RECTANGLE,
            Inches(0.8), Inches(0.4), Inches(2.2), Inches(0.35)
        )
        badge.fill.solid()
        badge.fill.fore_color.rgb = C_CYAN_LIGHT
        badge.line.color.rgb = C_CYAN_ACCENT
        badge.line.width = Pt(1)
        tf = badge.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = category_badge.upper()
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = C_CYAN_ACCENT
        p.alignment = PP_ALIGN.CENTER

        # Title
        title_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.8), Inches(11.7), Inches(0.8))
        tf = title_box.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = title_text
        p.font.size = Pt(26)
        p.font.bold = True
        p.font.color.rgb = C_TEXT_DARK
        p.font.name = "Arial"

        if subtitle_text:
            p2 = tf.add_paragraph()
            p2.text = subtitle_text
            p2.font.size = Pt(13)
            p2.font.color.rgb = C_TEXT_MUTED
            p2.font.name = "Arial"

    def add_card(slide, left, top, width, height, title="", title_color=C_CYAN_ACCENT, bg_color=C_CARD_BG, border_color=C_CARD_BORDER):
        card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
        card.fill.solid()
        card.fill.fore_color.rgb = bg_color
        card.line.color.rgb = border_color
        card.line.width = Pt(1.5)
        
        if title:
            tb = slide.shapes.add_textbox(left + Inches(0.2), top + Inches(0.15), width - Inches(0.4), Inches(0.45))
            tf = tb.text_frame
            tf.word_wrap = True
            p = tf.paragraphs[0]
            p.text = title
            p.font.size = Pt(15)
            p.font.bold = True
            p.font.color.rgb = title_color
            p.font.name = "Arial"
        return card

    # =========================================================================
    # SLIDE 1: TITLE SLIDE (DARK THEME)
    # =========================================================================
    slide1 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide1, C_NAVY_DARK)

    # Accent decorative banner
    accent_bar = slide1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(0.4), Inches(7.5))
    accent_bar.fill.solid()
    accent_bar.fill.fore_color.rgb = C_CYAN_ACCENT
    accent_bar.line.fill.background()

    # Course Tag
    tag_box = slide1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.2), Inches(1.0), Inches(4.5), Inches(0.4))
    tag_box.fill.solid()
    tag_box.fill.fore_color.rgb = C_NAVY_LIGHT
    tag_box.line.color.rgb = C_CYAN_ACCENT
    tf = tag_box.text_frame
    p = tf.paragraphs[0]
    p.text = "OPERATING SYSTEMS & SYSTEM PROGRAMMING (OSSP)"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = C_CYAN_ACCENT
    p.alignment = PP_ALIGN.CENTER

    # Main Title
    t_box = slide1.shapes.add_textbox(Inches(1.2), Inches(1.6), Inches(11.0), Inches(1.8))
    tf = t_box.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "DevOps Mini Shell"
    p.font.size = Pt(44)
    p.font.bold = True
    p.font.color.rgb = C_TEXT_LIGHT
    p.font.name = "Arial"

    p2 = tf.add_paragraph()
    p2.text = "A Unified Command-Line Environment for Automated DevOps Workflows & System Observability"
    p2.font.size = Pt(18)
    p2.font.color.rgb = C_CYAN_ACCENT
    p2.font.name = "Arial"

    # Divider line
    div = slide1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(1.2), Inches(3.6), Inches(10.8), Inches(0.04))
    div.fill.solid()
    div.fill.fore_color.rgb = C_CYAN_ACCENT
    div.line.fill.background()

    # Team Card & Project Features
    team_card = slide1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.2), Inches(3.9), Inches(5.2), Inches(2.9))
    team_card.fill.solid()
    team_card.fill.fore_color.rgb = C_NAVY_LIGHT
    team_card.line.color.rgb = RGBColor(51, 65, 85)
    tf = team_card.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "PROJECT TEAM MEMBERS"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = C_CYAN_ACCENT
    members = [
        "01. Gokul Arnav",
        "02. Wasim",
        "03. Binamra",
        "04. Yogith"
    ]
    for m in members:
        pm = tf.add_paragraph()
        pm.text = f"  •  {m}"
        pm.font.size = Pt(13)
        pm.font.color.rgb = C_TEXT_LIGHT

    # Highlights Card
    high_card = slide1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.8), Inches(3.9), Inches(5.2), Inches(2.9))
    high_card.fill.solid()
    high_card.fill.fore_color.rgb = C_NAVY_LIGHT
    high_card.line.color.rgb = RGBColor(51, 65, 85)
    tf = high_card.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "CORE IMPLEMENTATION HIGHLIGHTS"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = C_EMERALD
    highlights = [
        "• Written in pure C utilizing native POSIX system calls",
        "• Process Management via fork(), execvp(), and waitpid()",
        "• Command chaining with ';' and conditional '&&'",
        "• Automated CI/CD execution of .workflow pipelines",
        "• Real-time /proc telemetry & audit execution logging"
    ]
    for h in highlights:
        ph = tf.add_paragraph()
        ph.text = h
        ph.font.size = Pt(12)
        ph.font.color.rgb = RGBColor(226, 232, 240)

    # =========================================================================
    # SLIDE 2: PROJECT OVERVIEW & ABSTRACT
    # =========================================================================
    slide2 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide2, C_BG_LIGHT)
    add_header(slide2, "Project Overview & Abstract", "Introduction", "Unified developer cockpit for version control, containers, builds, and monitoring")

    # Left Card: Abstract Summary
    add_card(slide2, Inches(0.8), Inches(1.8), Inches(5.7), Inches(5.1), "Executive Abstract", C_NAVY_DARK)
    tb = slide2.shapes.add_textbox(Inches(1.0), Inches(2.4), Inches(5.3), Inches(4.3))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.text = "The DevOps Mini Shell (devops-shell) is a specialized UNIX/POSIX command-line toolkit and interactive shell designed to unify routine development and operations tasks into a single, cohesive interface."
    tf.paragraphs[0].font.size = Pt(13)
    tf.paragraphs[0].font.color.rgb = C_TEXT_DARK

    abstract_points = [
        ("Unified Environment: ", "Combines Git version control, Docker container operations, build automation, deployment scripts, and workflow pipelines under one prompt."),
        ("Low-Level OS Mastery: ", "Built from scratch in C to demonstrate core system programming principles: process creation, memory overlay, signals, and virtual filesystem inspection."),
        ("Lightweight & Fast: ", "Operates with zero heavy dependencies or daemons, providing instantaneous startup and near-zero memory footprint (<1MB)."),
        ("Dual Platform Support: ", "Native Linux / WSL execution with compatibility fallbacks for Windows environments.")
    ]
    for title, desc in abstract_points:
        p = tf.add_paragraph()
        p.text = f"• {title}"
        p.font.bold = True
        p.font.size = Pt(12)
        p.font.color.rgb = C_NAVY_DARK
        p_desc = tf.add_paragraph()
        p_desc.text = f"   {desc}"
        p_desc.font.size = Pt(11.5)
        p_desc.font.color.rgb = C_TEXT_MUTED

    # Right Card: Motivation & Impact
    add_card(slide2, Inches(6.8), Inches(1.8), Inches(5.7), Inches(5.1), "Why DevOps Mini Shell?", C_CYAN_ACCENT)
    tb2 = slide2.shapes.add_textbox(Inches(7.0), Inches(2.4), Inches(5.3), Inches(4.3))
    tf2 = tb2.text_frame
    tf2.word_wrap = True
    tf2.text = "Key Motivating Drivers:"
    tf2.paragraphs[0].font.bold = True
    tf2.paragraphs[0].font.size = Pt(13)
    tf2.paragraphs[0].font.color.rgb = C_CYAN_ACCENT

    mot_points = [
        ("Eliminating Tool Fatigue: ", "Engineers frequently switch between terminal tabs, Git GUIs, Docker desktops, and system monitors. A unified shell streamlines daily operations."),
        ("Pedagogical Value for OS Students: ", "Provides a concrete, real-world application of Operating System abstractions that students typically only study theoretically."),
        ("Built-in Workflow Orchestration: ", "Run complete CI/CD routines locally without configuring enterprise-level server daemons like Jenkins or GitLab CI runners."),
        ("Auditability & Governance: ", "Automatically tracks every executed command and its exit status with high-precision ISO timestamps for complete reproducibility.")
    ]
    for title, desc in mot_points:
        p = tf2.add_paragraph()
        p.text = f"• {title}"
        p.font.bold = True
        p.font.size = Pt(12)
        p.font.color.rgb = C_NAVY_DARK
        p_desc = tf2.add_paragraph()
        p_desc.text = f"   {desc}"
        p_desc.font.size = Pt(11.5)
        p_desc.font.color.rgb = C_TEXT_MUTED

    # =========================================================================
    # SLIDE 3: PROBLEM STATEMENT
    # =========================================================================
    slide3 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide3, C_BG_LIGHT)
    add_header(slide3, "Problem Statement & Operational Challenges", "Problem Formulation", "Addressing the friction of fragmented DevOps workflows and disparate tooling")

    cards_data = [
        (Inches(0.8), "1. Tool Fragmentation & Inconsistency", C_ROSE, [
            ("Disjointed Interfaces", "Engineers must interact with distinct syntax and CLI structures across Git, Docker, Make, and system tools."),
            ("High Cognitive Load", "Context-switching between commands increases errors and cognitive overhead for students and developers."),
            ("Lack of Cohesion", "No single standard shell natively correlates Git repository states with active container and memory health.")
        ]),
        (Inches(4.8), "2. Inefficient Workflow Execution", C_AMBER, [
            ("Manual Step Repetition", "Standard build-test-deploy cycles require typing 5-10 separate commands in strict sequence."),
            ("Silent Failure Vulnerability", "In standard shells, executing 'cmd1 ; cmd2' does not verify whether cmd1 succeeded before running cmd2."),
            ("Complex Scripting Overhead", "Creating robust Bash scripts with error-trapping requires advanced shell scripting knowledge.")
        ]),
        (Inches(8.8), "3. Absence of Built-in Telemetry", C_CYAN_ACCENT, [
            ("Blind Operations", "Developers deploy code without immediate visibility into available host RAM, CPU uptime, or disk space."),
            ("No Unified Audit Log", "Terminal histories lack timestamping and process exit codes, complicating debugging of failed builds."),
            ("Heavyweight Alternatives", "Enterprise observability stacks (Prometheus, Grafana) are far too heavy for lightweight local workflows.")
        ])
    ]

    for left, title, color, points in cards_data:
        add_card(slide3, left, Inches(1.8), Inches(3.7), Inches(5.1), title, color)
        tb = slide3.shapes.add_textbox(left + Inches(0.2), Inches(2.5), Inches(3.3), Inches(4.2))
        tf = tb.text_frame
        tf.word_wrap = True
        first = True
        for p_title, p_desc in points:
            p = tf.paragraphs[0] if first else tf.add_paragraph()
            first = False
            p.text = f"• {p_title}"
            p.font.bold = True
            p.font.size = Pt(12)
            p.font.color.rgb = C_NAVY_DARK
            pd = tf.add_paragraph()
            pd.text = f"   {p_desc}"
            pd.font.size = Pt(11)
            pd.font.color.rgb = C_TEXT_MUTED

    # =========================================================================
    # SLIDE 4: LITERATURE REVIEW: EXISTING SYSTEMS
    # =========================================================================
    slide4 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide4, C_BG_LIGHT)
    add_header(slide4, "Literature Review: Analysis of Existing Systems", "Literature Review", "Survey of traditional command-line shells, CI/CD runners, and build tools")

    lit_cards = [
        (Inches(0.8), "Traditional UNIX Shells (Bash, Zsh, Sh)", C_NAVY_DARK, [
            ("Focus & Strengths: ", "Universal adoption, general-purpose command execution, POSIX compliance, extensive piping and scripting capabilities."),
            ("DevOps Limitations: ", "Completely generic. No native knowledge of Git repositories or Docker daemon health."),
            ("Telemetry Gaps: ", "No single dashboard view; developers must memorize 'ps', 'free -h', 'df -h', 'uptime' and combine them manually."),
            ("Logging: ", "Standard '.bash_history' records commands but drops critical metadata like exact timestamps and return exit codes.")
        ]),
        (Inches(4.8), "Enterprise CI/CD Systems (Jenkins, GitLab CI)", C_CYAN_ACCENT, [
            ("Focus & Strengths: ", "Robust distributed pipeline automation, web dashboards, multi-node cloud deployments, secret management."),
            ("DevOps Limitations: ", "Extreme resource overhead; requires server daemons, Java Runtime (JVM), web listeners, and heavy background processes."),
            ("Workflow Complexity: ", "Requires complex YAML or Groovy pipeline DSLs; overkill for local microservices or student projects."),
            ("Execution Model: ", "Designed for remote servers, not interactive, real-time command-line terminal exploration.")
        ]),
        (Inches(8.8), "Build Wrappers & Task Runners (Make, npm)", C_EMERALD, [
            ("Focus & Strengths: ", "Target-based dependency resolution, incremental compilation, script alias standardization."),
            ("DevOps Limitations: ", "Restricted to compilation or project tasks; not an interactive shell or REPL environment."),
            ("Workflow Gaps: ", "Cannot monitor live system memory, process trees, or manage interactive Git branch checkouts."),
            ("Scope Limitation: ", "Operates as a one-off utility rather than a continuous operational workspace.")
        ])
    ]

    for left, title, color, points in lit_cards:
        add_card(slide4, left, Inches(1.8), Inches(3.7), Inches(5.1), title, color)
        tb = slide4.shapes.add_textbox(left + Inches(0.2), Inches(2.5), Inches(3.3), Inches(4.2))
        tf = tb.text_frame
        tf.word_wrap = True
        first = True
        for p_title, p_desc in points:
            p = tf.paragraphs[0] if first else tf.add_paragraph()
            first = False
            p.text = p_title
            p.font.bold = True
            p.font.size = Pt(11.5)
            p.font.color.rgb = color
            pd = tf.add_paragraph()
            pd.text = p_desc
            pd.font.size = Pt(11)
            pd.font.color.rgb = C_TEXT_MUTED

    # =========================================================================
    # SLIDE 5: DRAWBACKS & GAPS OF EXISTING SYSTEMS (TABLE)
    # =========================================================================
    slide5 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide5, C_BG_LIGHT)
    add_header(slide5, "Gaps & Drawbacks in Existing Approaches", "Comparative Analysis", "Systematic evaluation demonstrating the need for a specialized DevOps shell")

    # Add Comparative Table
    rows = 6
    cols = 5
    table_shape = slide5.shapes.add_table(rows, cols, Inches(0.8), Inches(1.8), Inches(11.7), Inches(4.5))
    table = table_shape.table

    # Set column widths
    table.columns[0].width = Inches(2.7)
    table.columns[1].width = Inches(2.2)
    table.columns[2].width = Inches(2.3)
    table.columns[3].width = Inches(2.2)
    table.columns[4].width = Inches(2.3)

    table_data = [
        ["Evaluation Dimension", "Traditional Shells (Bash/Zsh)", "Enterprise CI/CD (Jenkins)", "Task Runners (Make)", "DevOps Mini Shell (Ours)"],
        ["Interactive DevOps REPL", "No (General purpose)", "No (Web GUI / Agent)", "No (Batch task only)", "YES (Built-in DevOps focus)"],
        ["Local Pipeline Execution", "Requires custom scripts", "Complex daemon required", "Target-only compilation", "YES (Native .workflow runner)"],
        ["System & Resource Telemetry", "Disparate commands only", "Requires plugin stack", "None", "YES (Instant 'sysinfo' dashboard)"],
        ["Memory & Resource Overhead", "Low (~5-10 MB)", "Very High (>500 MB RAM)", "Very Low (~2 MB)", "Extremely Low (<1 MB, 0 daemons)"],
        ["Auditability & Exit Logging", "Basic history (no status)", "Detailed but heavy", "None", "YES (Timestamped log with exit code)"]
    ]

    for r_idx, row in enumerate(table_data):
        for c_idx, cell_value in enumerate(row):
            cell = table.cell(r_idx, c_idx)
            cell.text = cell_value
            p = cell.text_frame.paragraphs[0]
            p.alignment = PP_ALIGN.CENTER if c_idx > 0 else PP_ALIGN.LEFT
            
            if r_idx == 0:
                cell.fill.solid()
                cell.fill.fore_color.rgb = C_NAVY_DARK
                p.font.bold = True
                p.font.color.rgb = C_TEXT_LIGHT
                p.font.size = Pt(11)
            else:
                cell.fill.solid()
                if c_idx == 4:
                    cell.fill.fore_color.rgb = RGBColor(236, 253, 245) # light green highlight
                    p.font.bold = True
                    p.font.color.rgb = C_EMERALD
                    p.font.size = Pt(10.5)
                else:
                    cell.fill.fore_color.rgb = RGBColor(255, 255, 255) if r_idx % 2 == 1 else RGBColor(241, 245, 249)
                    p.font.color.rgb = C_TEXT_DARK
                    p.font.size = Pt(10.5)

    # Bottom summary callout
    bot_box = slide5.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(6.5), Inches(11.7), Inches(0.6))
    bot_box.fill.solid()
    bot_box.fill.fore_color.rgb = C_CYAN_LIGHT
    bot_box.line.color.rgb = C_CYAN_ACCENT
    tf = bot_box.text_frame
    p = tf.paragraphs[0]
    p.text = "Key Insight: The DevOps Mini Shell bridges the gap between lightweight terminal efficiency and automated DevOps orchestration without server overhead."
    p.font.size = Pt(11.5)
    p.font.bold = True
    p.font.color.rgb = C_NAVY_DARK
    p.alignment = PP_ALIGN.CENTER

    # =========================================================================
    # SLIDE 6: PROPOSED SYSTEM
    # =========================================================================
    slide6 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide6, C_BG_LIGHT)
    add_header(slide6, "Proposed System: DevOps Mini Shell Architecture", "Our Solution", "A specialized C-based shell designed for streamlined development and operations")

    # Left Card: Core Philosophy
    add_card(slide6, Inches(0.8), Inches(1.8), Inches(5.7), Inches(5.1), "Core Architecture & Design Goals", C_NAVY_DARK)
    tb = slide6.shapes.add_textbox(Inches(1.0), Inches(2.4), Inches(5.3), Inches(4.3))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.text = "The Proposed DevOps Mini Shell is designed around four pillars:"
    tf.paragraphs[0].font.bold = True
    tf.paragraphs[0].font.size = Pt(13)
    tf.paragraphs[0].font.color.rgb = C_NAVY_DARK

    pillars = [
        ("1. Unified Command Execution: ", "Integrates Git, Docker, Make, Build, Deploy, and Workflow utilities under a single prompt with intelligent syntax dispatching."),
        ("2. Conditional Command Chaining: ", "Implements sequential ';' and conditional '&&' operators, automatically evaluating child process exit codes before running next commands."),
        ("3. Zero-Dependency CI/CD Engine: ", "Executes .workflow pipeline scripts locally with step-by-step validation, failure halting, and console reporting."),
        ("4. Low-Level OS Integration: ", "Interacts directly with Linux kernel data structures (/proc/uptime, /proc/meminfo) and handles signals (SIGINT) gracefully.")
    ]
    for title, desc in pillars:
        p = tf.add_paragraph()
        p.text = title
        p.font.bold = True
        p.font.size = Pt(12)
        p.font.color.rgb = C_CYAN_ACCENT
        pd = tf.add_paragraph()
        pd.text = desc
        pd.font.size = Pt(11)
        pd.font.color.rgb = C_TEXT_MUTED

    # Right Card: Concrete Features Implemented
    add_card(slide6, Inches(6.8), Inches(1.8), Inches(5.7), Inches(5.1), "Key Capabilities Implemented", C_EMERALD)
    tb2 = slide6.shapes.add_textbox(Inches(7.0), Inches(2.4), Inches(5.3), Inches(4.3))
    tf2 = tb2.text_frame
    tf2.word_wrap = True
    tf2.text = "Implemented System Capabilities:"
    tf2.paragraphs[0].font.bold = True
    tf2.paragraphs[0].font.size = Pt(13)
    tf2.paragraphs[0].font.color.rgb = C_EMERALD

    caps = [
        ("sysinfo / status: ", "One-shot comprehensive dashboard showing CWD, Uptime, Memory utilization, Git branch/commits, and Docker containers."),
        ("workflow <pipeline>: ", "Executes automated multi-step pipelines with error trapping."),
        ("deploy <script>: ", "Validates and runs staging/production release scripts safely."),
        ("build: ", "Smart builder auto-detecting Makefile, CMakeLists.txt, package.json, or C source."),
        ("history & log: ", "Persistent history recording (.devops_shell_history) and timestamped execution logging (devops_shell.log)."),
        ("remote <user@host> <cmd>: ", "Seamless remote execution via SSH integration.")
    ]
    for title, desc in caps:
        p = tf2.add_paragraph()
        p.text = f"• {title}"
        p.font.bold = True
        p.font.size = Pt(11.5)
        p.font.color.rgb = C_NAVY_DARK
        pd = tf2.add_paragraph()
        pd.text = f"   {desc}"
        pd.font.size = Pt(11)
        pd.font.color.rgb = C_TEXT_MUTED

    # =========================================================================
    # SLIDE 7: SYSTEM ARCHITECTURE DIAGRAM
    # =========================================================================
    slide7 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide7, C_BG_LIGHT)
    add_header(slide7, "System Architecture: Layered Decomposition", "System Architecture", "Modular decomposition illustrating data flow from terminal input to OS primitives")

    # Layer 1: Presentation & REPL
    l1 = slide7.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.8), Inches(11.7), Inches(0.95))
    l1.fill.solid()
    l1.fill.fore_color.rgb = C_NAVY_DARK
    l1.line.color.rgb = C_CYAN_ACCENT
    tf = l1.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "LAYER 1: USER INTERACTION & REPL ENGINE"
    p.font.bold = True
    p.font.size = Pt(12)
    p.font.color.rgb = C_CYAN_ACCENT
    p2 = tf.add_paragraph()
    p2.text = "Interactive Terminal Prompt (devops:<cwd>$)  |  ANSI 256-Color Engine  |  Asynchronous SIGINT (Ctrl+C) Signal Trapping"
    p2.font.size = Pt(11)
    p2.font.color.rgb = C_TEXT_LIGHT

    # Layer 2: Parser & Lexer
    l2 = slide7.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(2.95), Inches(11.7), Inches(1.05))
    l2.fill.solid()
    l2.fill.fore_color.rgb = RGBColor(241, 245, 249)
    l2.line.color.rgb = C_CYAN_ACCENT
    tf = l2.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "LAYER 2: PARSING & COMMAND CHAINING ENGINE"
    p.font.bold = True
    p.font.size = Pt(12)
    p.font.color.rgb = C_NAVY_DARK
    p2 = tf.add_paragraph()
    p2.text = "• trim(): Strips whitespace  |  • Chaining Parser: Separates ';' (Unconditional) and '&&' (Conditional on Success)"
    p2.font.size = Pt(11)
    p2.font.color.rgb = C_TEXT_MUTED
    p3 = tf.add_paragraph()
    p3.text = "• parse_arguments(): Quote-aware tokenization preserving string arguments (e.g., git commit -m \"initial commit\")"
    p3.font.size = Pt(11)
    p3.font.color.rgb = C_TEXT_MUTED

    # Layer 3: Dispatch & Dual Execution
    l3_left = slide7.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(4.2), Inches(5.7), Inches(1.5))
    l3_left.fill.solid()
    l3_left.fill.fore_color.rgb = RGBColor(238, 242, 255)
    l3_left.line.color.rgb = RGBColor(99, 102, 241)
    tf = l3_left.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "LAYER 3A: BUILT-IN COMMAND SUBSYSTEM"
    p.font.bold = True
    p.font.size = Pt(11.5)
    p.font.color.rgb = RGBColor(67, 56, 202)
    p2 = tf.add_paragraph()
    p2.text = "Executed directly in-process without fork overhead:\n• cd, pwd, clear, help, exit\n• sysinfo, free, uptime, df\n• workflow, deploy, build, history, log"
    p2.font.size = Pt(10.5)
    p2.font.color.rgb = C_TEXT_DARK

    l3_right = slide7.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.8), Inches(4.2), Inches(5.7), Inches(1.5))
    l3_right.fill.solid()
    l3_right.fill.fore_color.rgb = RGBColor(236, 253, 245)
    l3_right.line.color.rgb = C_EMERALD
    tf = l3_right.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "LAYER 3B: POSIX PROCESS EXECUTION ENGINE"
    p.font.bold = True
    p.font.size = Pt(11.5)
    p.font.color.rgb = C_EMERALD
    p2 = tf.add_paragraph()
    p2.text = "External binary dispatch with OS process isolation:\n• Process Creation: fork() system call\n• Binary Image Overlay: execvp() (git, docker, make, etc.)\n• Parent Synchronization: waitpid() & exit status analysis"
    p2.font.size = Pt(10.5)
    p2.font.color.rgb = C_TEXT_DARK

    # Layer 4: Persistence & Telemetry
    l4 = slide7.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(5.9), Inches(11.7), Inches(1.1))
    l4.fill.solid()
    l4.fill.fore_color.rgb = C_NAVY_LIGHT
    l4.line.color.rgb = C_CYAN_ACCENT
    tf = l4.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "LAYER 4: KERNEL TELEMETRY & PERSISTENCE ENGINE"
    p.font.bold = True
    p.font.size = Pt(12)
    p.font.color.rgb = C_CYAN_ACCENT
    p2 = tf.add_paragraph()
    p2.text = "• /proc Virtual Filesystem (/proc/meminfo, /proc/uptime)  |  • Persistent History (.devops_shell_history)"
    p2.font.size = Pt(11)
    p2.font.color.rgb = C_TEXT_LIGHT
    p3 = tf.add_paragraph()
    p3.text = "• Structured Execution Audit Log (devops_shell.log with ISO-8601 Timestamps and Process Exit Codes)"
    p3.font.size = Pt(11)
    p3.font.color.rgb = RGBColor(148, 163, 184)

    # =========================================================================
    # SLIDE 8: OPERATING SYSTEMS PRINCIPLES & LOW-LEVEL MECHANISMS
    # =========================================================================
    slide8 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide8, C_BG_LIGHT)
    add_header(slide8, "Operating System Principles & Mechanisms", "OS Concepts", "Deep dive into low-level POSIX and System Programming primitives implemented in C")

    os_cards = [
        (Inches(0.8), "1. Process Management (`fork()`)", C_NAVY_DARK, [
            ("Mechanism: ", "Invokes the 'fork()' system call to duplicate the parent shell process into a child process."),
            ("PID Isolation: ", "Child receives PID 0; parent receives child's PID. Shell address space is completely isolated."),
            ("Fault Protection: ", "If an external command crashes (e.g., Segfault), only the child terminates; the shell REPL survives intact.")
        ]),
        (Inches(3.8), "2. Image Overlay (`execvp()`)", C_CYAN_ACCENT, [
            ("Mechanism: ", "Child process executes 'execvp(args[0], args)', replacing its virtual memory image with the target binary."),
            ("PATH Resolution: ", "Automatically traverses the system PATH environment variable to locate tools like 'git' and 'docker'."),
            ("Argument Vector: ", "Passes NULL-terminated argument array, preserving flags and quoted string literals.")
        ]),
        (Inches(6.8), "3. Synchronization (`waitpid()`)", C_EMERALD, [
            ("Mechanism: ", "Parent blocks using 'waitpid(pid, &status, 0)' until child execution finishes."),
            ("Exit Evaluation: ", "Uses 'WIFEXITED(status)' and 'WEXITSTATUS(status)' to extract precise return code (0 = success)."),
            ("Conditional Gating: ", "Status code feeds directly into the '&&' chaining logic to skip remaining commands on failure.")
        ]),
        (Inches(9.8), "4. Kernel /proc & Signals", C_AMBER, [
            ("Signal Trapping: ", "'signal(SIGINT, handle_sigint)' intercepts Ctrl+C so accidental keystrokes don't kill the shell."),
            ("Virtual Filesystem: ", "Directly parses '/proc/meminfo' and '/proc/uptime' kernel files rather than spawning subshells."),
            ("Near-Zero Latency: ", "Direct file descriptor reads ensure telemetry returns in sub-millisecond execution times.")
        ])
    ]

    for left, title, color, points in os_cards:
        add_card(slide8, left, Inches(1.8), Inches(2.7), Inches(5.1), title, color)
        tb = slide8.shapes.add_textbox(left + Inches(0.15), Inches(2.5), Inches(2.4), Inches(4.2))
        tf = tb.text_frame
        tf.word_wrap = True
        first = True
        for p_title, p_desc in points:
            p = tf.paragraphs[0] if first else tf.add_paragraph()
            first = False
            p.text = p_title
            p.font.bold = True
            p.font.size = Pt(11)
            p.font.color.rgb = color
            pd = tf.add_paragraph()
            pd.text = p_desc
            pd.font.size = Pt(10.5)
            pd.font.color.rgb = C_TEXT_MUTED

    # =========================================================================
    # SLIDE 9: HOW THE SYSTEM WORKS: STEP-BY-STEP EXECUTION FLOW
    # =========================================================================
    slide9 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide9, C_BG_LIGHT)
    add_header(slide9, "How My System Works: Execution Lifecycle", "Execution Flow", "Step-by-step trace of command ingestion, chaining evaluation, dispatch, and logging")

    # Step cards arranged horizontally across the page
    steps = [
        ("Step 1: Input & Prompt", "Shell fetches CWD via getcwd(), displays prompt, and reads user input using fgets(). Empty inputs are skipped.", C_NAVY_DARK),
        ("Step 2: History Recording", "Input string is trimmed and appended to .devops_shell_history before execution for persistence.", C_CYAN_ACCENT),
        ("Step 3: Chaining Parser", "String is scanned for ';' and '&&'. Split into an array of ChainedCommand structs with conditional flags.", C_EMERALD),
        ("Step 4: Tokenizer & Quotes", "parse_arguments() converts tokens into argv[]. Supports single/double quotes (e.g. commit messages).", C_AMBER),
        ("Step 5: Command Dispatch", "Built-ins execute in-process. External tools trigger fork() -> execvp() -> waitpid().", C_ROSE),
        ("Step 6: Logging & Chain Gate", "Exit status logged to devops_shell.log. If '&&' follows and status != 0, subsequent commands are safely skipped.", C_NAVY_LIGHT)
    ]

    for idx, (st_title, st_desc, color) in enumerate(steps):
        row = idx // 3
        col = idx % 3
        left = Inches(0.8) + col * Inches(3.95)
        top = Inches(1.8) + row * Inches(2.6)
        
        card = add_card(slide9, left, top, Inches(3.8), Inches(2.35), st_title, color)
        tb = slide9.shapes.add_textbox(left + Inches(0.2), top + Inches(0.7), Inches(3.4), Inches(1.5))
        tf = tb.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = st_desc
        p.font.size = Pt(11.5)
        p.font.color.rgb = C_TEXT_DARK

    # =========================================================================
    # SLIDE 10: IMPLEMENTED MODULES: GIT, DOCKER & SMART BUILD
    # =========================================================================
    slide10 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide10, C_BG_LIGHT)
    add_header(slide10, "Implemented Modules: Git, Docker & Smart Build", "Module Implementation", "Native tooling integrations built into the DevOps Mini Shell")

    mod_cards = [
        (Inches(0.8), "Git & Version Control Module", C_NAVY_DARK, [
            ("git status: ", "Displays current repository state and unstaged modifications."),
            ("git summary (Built-in): ", "Custom automated status: verifies .git directory, fetches active branch, and outputs last 3 commits in oneline format."),
            ("git log: ", "Inspects chronological commit history."),
            ("git add & commit: ", "Supports full staging and message committing preserving quoted descriptions."),
            ("git push & pull: ", "Synchronizes code with remote Git origins effortlessly.")
        ]),
        (Inches(4.8), "Docker & Container Module", C_CYAN_ACCENT, [
            ("docker ps: ", "Inspects currently running container instances."),
            ("docker ps -a: ", "Shows all containers including stopped/exited containers."),
            ("docker images: ", "Lists locally cached container images and tags."),
            ("docker status (Built-in): ", "Checks Docker daemon responsiveness and outputs formatted container summary table."),
            ("docker build / run: ", "Builds container images and runs containers directly from current project directory.")
        ]),
        (Inches(8.8), "Smart Build Automation Engine", C_EMERALD, [
            ("build (Smart Detector): ", "Automatically inspects workspace directory using 'stat()' to detect build configurations:"),
            ("1. Makefile: ", "Triggers 'make' compilation."),
            ("2. CMakeLists.txt: ", "Triggers 'cmake --build .'."),
            ("3. package.json: ", "Triggers 'npm run build'."),
            ("4. devops_shell.c: ", "Self-compilation via 'gcc devops_shell.c -o devops-shell'."),
            ("make [target]: ", "Executes explicit Makefile targets (all, run, test, clean).")
        ])
    ]

    for left, title, color, points in mod_cards:
        add_card(slide10, left, Inches(1.8), Inches(3.7), Inches(5.1), title, color)
        tb = slide10.shapes.add_textbox(left + Inches(0.2), Inches(2.5), Inches(3.3), Inches(4.2))
        tf = tb.text_frame
        tf.word_wrap = True
        first = True
        for p_title, p_desc in points:
            p = tf.paragraphs[0] if first else tf.add_paragraph()
            first = False
            p.text = p_title
            p.font.bold = True
            p.font.size = Pt(11.5)
            p.font.color.rgb = color
            pd = tf.add_paragraph()
            pd.text = p_desc
            pd.font.size = Pt(11)
            pd.font.color.rgb = C_TEXT_MUTED

    # =========================================================================
    # SLIDE 11: IMPLEMENTED MODULES: WORKFLOW ENGINE & DEPLOYMENT
    # =========================================================================
    slide11 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide11, C_BG_LIGHT)
    add_header(slide11, "Workflow Automation & Automated Deployment", "Module Implementation", "CI/CD execution engine parsing .workflow pipelines and deployment runners")

    # Left: Workflow Pipeline Runner
    add_card(slide11, Inches(0.8), Inches(1.8), Inches(5.7), Inches(5.1), "CI/CD Pipeline Engine (workflow)", C_NAVY_DARK)
    tb = slide11.shapes.add_textbox(Inches(1.0), Inches(2.4), Inches(5.3), Inches(4.3))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.text = "Automated Pipeline Execution (ci_pipeline.workflow):"
    tf.paragraphs[0].font.bold = True
    tf.paragraphs[0].font.size = Pt(13)
    tf.paragraphs[0].font.color.rgb = C_NAVY_DARK

    wf_features = [
        ("Declarative File Format: ", "Parses plain text .workflow files line-by-line."),
        ("Comment & Whitespace Filtering: ", "Ignores comment lines starting with '#' and blank rows."),
        ("Sequential Step Dispatch: ", "Executes each command through execute_command_line(), supporting chaining inside workflow files."),
        ("Error Propagation & Halting: ", "If any step returns a non-zero exit status, the entire workflow halts immediately, preventing faulty deployments."),
        ("Pipeline Exit Isolation: ", "Ignores internal 'exit' commands to preserve parent shell session.")
    ]
    for title, desc in wf_features:
        p = tf.add_paragraph()
        p.text = f"• {title}"
        p.font.bold = True
        p.font.size = Pt(11.5)
        p.font.color.rgb = C_CYAN_ACCENT
        pd = tf.add_paragraph()
        pd.text = f"   {desc}"
        pd.font.size = Pt(11)
        pd.font.color.rgb = C_TEXT_MUTED

    # Right: Deploy Engine
    add_card(slide11, Inches(6.8), Inches(1.8), Inches(5.7), Inches(5.1), "Automated Deployment Engine (deploy)", C_EMERALD)
    tb2 = slide11.shapes.add_textbox(Inches(7.0), Inches(2.4), Inches(5.3), Inches(4.3))
    tf2 = tb2.text_frame
    tf2.word_wrap = True
    tf2.text = "Deployment Script Execution (deploy deploy_sample.sh):"
    tf2.paragraphs[0].font.bold = True
    tf2.paragraphs[0].font.size = Pt(13)
    tf2.paragraphs[0].font.color.rgb = C_EMERALD

    dep_features = [
        ("File Validation: ", "Uses stat() to verify deployment script exists and is accessible before spawning execution."),
        ("Interpreter Auto-Detection: ", "Inspects script extension: invokes 'bash' for .sh scripts, 'python3' for .py scripts, or direct binary execution."),
        ("Multi-Stage Release Simulation: ", "Sample deploy_sample.sh demonstrates 4 production stages:\n  [1/4] Artifact Validation\n  [2/4] Resource Availability Check\n  [3/4] Release Package Deployment\n  [4/4] HTTP Health Check Smoke Tests"),
        ("Exit Status Audit: ", "Returns and logs exact deployment return code to devops_shell.log.")
    ]
    for title, desc in dep_features:
        p = tf2.add_paragraph()
        p.text = f"• {title}"
        p.font.bold = True
        p.font.size = Pt(11.5)
        p.font.color.rgb = C_NAVY_DARK
        pd = tf2.add_paragraph()
        pd.text = f"   {desc}"
        pd.font.size = Pt(11)
        pd.font.color.rgb = C_TEXT_MUTED

    # =========================================================================
    # SLIDE 12: SYSTEM MONITORING, DASHBOARD & AUDIT LOGGING
    # =========================================================================
    slide12 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide12, C_BG_LIGHT)
    add_header(slide12, "System Observability, Dashboard & Audit Logging", "Observability & Audit", "Instant system telemetry and comprehensive execution audit trail")

    # Left: Dashboard & Monitoring
    add_card(slide12, Inches(0.8), Inches(1.8), Inches(5.7), Inches(5.1), "DevOps Dashboard & Telemetry", C_NAVY_DARK)
    tb = slide12.shapes.add_textbox(Inches(1.0), Inches(2.4), Inches(5.3), Inches(4.3))
    tf = tb.text_frame
    tf.word_wrap = True
    
    dash_items = [
        ("sysinfo / status (Unified Dashboard): ", "Presents a single consolidated status card containing: Working Directory, System Uptime, Memory utilization, Git repo state, and Docker containers."),
        ("uptime: ", "Calculates hours, minutes, seconds from /proc/uptime with sub-second accuracy."),
        ("free / memory: ", "Parses /proc/meminfo to extract Total, Used, Available, Free RAM with percentage utilization."),
        ("df / disk: ", "Displays filesystem storage space and mount partition utilization."),
        ("ps: ", "Monitors running OS processes.")
    ]
    first = True
    for title, desc in dash_items:
        p = tf.paragraphs[0] if first else tf.add_paragraph()
        first = False
        p.text = f"• {title}"
        p.font.bold = True
        p.font.size = Pt(11.5)
        p.font.color.rgb = C_CYAN_ACCENT
        pd = tf.add_paragraph()
        pd.text = f"   {desc}"
        pd.font.size = Pt(11)
        pd.font.color.rgb = C_TEXT_MUTED

    # Right: History & Log Terminal Box
    add_card(slide12, Inches(6.8), Inches(1.8), Inches(5.7), Inches(5.1), "Command History & Audit Trail", C_AMBER)
    tb2 = slide12.shapes.add_textbox(Inches(7.0), Inches(2.4), Inches(5.3), Inches(2.2))
    tf2 = tb2.text_frame
    tf2.word_wrap = True
    tf2.text = "Audit Logging Specifications:"
    tf2.paragraphs[0].font.bold = True
    tf2.paragraphs[0].font.size = Pt(12)
    tf2.paragraphs[0].font.color.rgb = C_AMBER

    p = tf2.add_paragraph()
    p.text = "• history: Persistent record stored in .devops_shell_history."
    p.font.size = Pt(11)
    p.font.color.rgb = C_TEXT_DARK
    p2 = tf2.add_paragraph()
    p2.text = "• log [N]: Displays last N entries from devops_shell.log."
    p2.font.size = Pt(11)
    p2.font.color.rgb = C_TEXT_DARK

    # Terminal box sample
    term = slide12.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(7.0), Inches(3.7), Inches(5.3), Inches(3.0))
    term.fill.solid()
    term.fill.fore_color.rgb = C_CODE_BG
    term.line.color.rgb = RGBColor(71, 85, 105)
    tf_term = term.text_frame
    tf_term.word_wrap = True
    sample_log = (
        "=== SAMPLE devops_shell.log ENTRIES ===\n\n"
        "[2026-10-08 18:20:10] [EXIT:  0] uptime\n"
        "[2026-10-08 18:20:12] [EXIT:  0] free\n"
        "[2026-10-08 18:20:15] [EXIT:  0] git summary\n"
        "[2026-10-08 18:20:20] [EXIT:  0] workflow ci_pipeline.workflow\n"
        "[2026-10-08 18:20:25] [EXIT:  0] deploy deploy_sample.sh\n"
        "[2026-10-08 18:20:30] [EXIT:127] invalid_cmd\n"
        "[2026-10-08 18:20:35] [EXIT:  0] uptime ; pwd"
    )
    p = tf_term.paragraphs[0]
    p.text = sample_log
    p.font.name = "Consolas"
    p.font.size = Pt(9.5)
    p.font.color.rgb = C_CODE_GREEN

    # =========================================================================
    # SLIDE 13: HARDWARE & SOFTWARE REQUIREMENTS
    # =========================================================================
    slide13 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide13, C_BG_LIGHT)
    add_header(slide13, "Hardware & Software Requirements & Portability", "Requirements", "Environmental specifications and cross-platform compatibility layer")

    # Left: Requirements
    add_card(slide13, Inches(0.8), Inches(1.8), Inches(5.7), Inches(5.1), "System Specifications", C_NAVY_DARK)
    tb = slide13.shapes.add_textbox(Inches(1.0), Inches(2.4), Inches(5.3), Inches(4.3))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.text = "Minimum Hardware Requirements:"
    tf.paragraphs[0].font.bold = True
    tf.paragraphs[0].font.size = Pt(13)
    tf.paragraphs[0].font.color.rgb = C_NAVY_DARK

    hw = [
        ("Processor: ", "Intel Core i3 / AMD Ryzen 3 or equivalent (x86_64 or ARM64)"),
        ("System Memory: ", "4 GB RAM minimum (DevOps Shell requires < 1 MB RAM)"),
        ("Storage: ", "50 MB available disk space for source and binaries"),
        ("Input/Output: ", "Standard terminal console (80x24 minimum)")
    ]
    for title, desc in hw:
        p = tf.add_paragraph()
        p.text = f"• {title}{desc}"
        p.font.size = Pt(11.5)
        p.font.color.rgb = C_TEXT_DARK

    p_sw = tf.add_paragraph()
    p_sw.text = "\nSoftware & Tooling Stack:"
    p_sw.font.bold = True
    p_sw.font.size = Pt(13)
    p_sw.font.color.rgb = C_NAVY_DARK

    sw = [
        ("Operating System: ", "Linux (Ubuntu/Debian) or Windows Subsystem for Linux (WSL2)"),
        ("Compiler: ", "GCC (GNU Compiler Collection) or Clang (C99 standard)"),
        ("Build Tool: ", "GNU Make 4.0+"),
        ("DevOps Tooling: ", "Git 2.20+, Docker Engine 20.10+ (optional for containers)")
    ]
    for title, desc in sw:
        p = tf.add_paragraph()
        p.text = f"• {title}{desc}"
        p.font.size = Pt(11.5)
        p.font.color.rgb = C_TEXT_DARK

    # Right: Cross-Platform Engineering
    add_card(slide13, Inches(6.8), Inches(1.8), Inches(5.7), Inches(5.1), "Cross-Platform Engineering Strategy", C_CYAN_ACCENT)
    tb2 = slide13.shapes.add_textbox(Inches(7.0), Inches(2.4), Inches(5.3), Inches(4.3))
    tf2 = tb2.text_frame
    tf2.word_wrap = True
    tf2.text = "Engineered for Seamless Portability:"
    tf2.paragraphs[0].font.bold = True
    tf2.paragraphs[0].font.size = Pt(13)
    tf2.paragraphs[0].font.color.rgb = C_CYAN_ACCENT

    port = [
        ("WSL Integration (run.bat): ", "Windows batch launcher automatically detects WSL Ubuntu, transparently mounts the project folder, compiles with GCC, and starts devops-shell."),
        ("Native Windows API Fallback: ", "Conditional compilation directives (#ifdef _WIN32) integrate Windows process spawning (_spawnvp), memory info (GlobalMemoryStatusEx), and uptime (GetTickCount64)."),
        ("Linux / Shell Launcher (run.sh): ", "Executable shell script setting permissions and executing devops-shell directly."),
        ("Makefile Target Suite: ", "'make', 'make run', 'make test', 'make clean' provide standardized build hooks.")
    ]
    for title, desc in port:
        p = tf2.add_paragraph()
        p.text = f"• {title}"
        p.font.bold = True
        p.font.size = Pt(11.5)
        p.font.color.rgb = C_NAVY_DARK
        pd = tf2.add_paragraph()
        pd.text = f"   {desc}"
        pd.font.size = Pt(11)
        pd.font.color.rgb = C_TEXT_MUTED

    # =========================================================================
    # SLIDE 14: TESTING, VALIDATION & LIVE DEMONSTRATION
    # =========================================================================
    slide14 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide14, C_BG_LIGHT)
    add_header(slide14, "Testing, Validation & Live Demonstration", "Verification", "Empirical results from automated smoke tests and pipeline execution")

    # Left: Automated Smoke Testing
    add_card(slide14, Inches(0.8), Inches(1.8), Inches(5.7), Inches(5.1), "Automated Smoke Test Suite (make test)", C_EMERALD)
    tb = slide14.shapes.add_textbox(Inches(1.0), Inches(2.4), Inches(5.3), Inches(4.3))
    tf = tb.text_frame
    tf.word_wrap = True
    
    t_items = [
        ("Automated Test Harness: ", "Executed via 'make test' using piped input stream: 'help\\npwd\\nuptime\\nfree\\ndf\\nhistory\\nlog 5\\nexit\\n' | ./devops-shell"),
        ("Command Parsing Validation: ", "100% pass rate on single commands, whitespace stripping, and argument tokenization."),
        ("Chaining Verification: ", "Validated unconditional execution (cmd1 ; cmd2) and conditional failure interception (failing_cmd && next_cmd)."),
        ("Workflow Pipeline Run: ", "ci_pipeline.workflow executed 5 consecutive steps, correctly aborting upon injected failure scenarios.")
    ]
    first = True
    for title, desc in t_items:
        p = tf.paragraphs[0] if first else tf.add_paragraph()
        first = False
        p.text = f"• {title}"
        p.font.bold = True
        p.font.size = Pt(11.5)
        p.font.color.rgb = C_NAVY_DARK
        pd = tf.add_paragraph()
        pd.text = f"   {desc}"
        pd.font.size = Pt(11)
        pd.font.color.rgb = C_TEXT_MUTED

    # Right: Terminal Demo Output
    term2 = slide14.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(6.8), Inches(1.8), Inches(5.7), Inches(5.1))
    term2.fill.solid()
    term2.fill.fore_color.rgb = C_CODE_BG
    term2.line.color.rgb = RGBColor(71, 85, 105)
    tf2 = term2.text_frame
    tf2.word_wrap = True
    
    demo_text = (
        "devops:/workspace$ workflow ci_pipeline.workflow\n"
        "══════════════════════════════════════════════════\n"
        " ⚡ EXECUTING DEVOPS WORKFLOW PIPELINE\n"
        "══════════════════════════════════════════════════\n"
        "--> [Step 1] Executing: uptime\n"
        "System Uptime: 2 hours, 14 mins, 10 secs\n"
        "✓ [Step 1 Completed Successfully]\n\n"
        "--> [Step 2] Executing: free\n"
        "=== Memory Monitoring (/proc/meminfo) ===\n"
        "  Total: 7748 MB | Used: 703 MB (9.1%)\n"
        "✓ [Step 2 Completed Successfully]\n\n"
        "--> [Step 3] Executing: uptime ; pwd\n"
        "/workspace\n"
        "✓ [Step 3 Completed Successfully]\n\n"
        "🎉 ALL WORKFLOW STEPS COMPLETED SUCCESSFULLY!"
    )
    p = tf2.paragraphs[0]
    p.text = demo_text
    p.font.name = "Consolas"
    p.font.size = Pt(9.5)
    p.font.color.rgb = C_CODE_GREEN

    # =========================================================================
    # SLIDE 15: CONCLUSION & FUTURE ENHANCEMENTS
    # =========================================================================
    slide15 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide15, C_BG_LIGHT)
    add_header(slide15, "Project Conclusion & Future Roadmap", "Conclusion", "Summary of engineering outcomes and roadmap for extended capabilities")

    # Left Card: Project Summary
    add_card(slide15, Inches(0.8), Inches(1.8), Inches(5.7), Inches(5.1), "Project Achievements & Summary", C_NAVY_DARK)
    tb = slide15.shapes.add_textbox(Inches(1.0), Inches(2.4), Inches(5.3), Inches(4.3))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.text = "Key Project Milestones Reached:"
    tf.paragraphs[0].font.bold = True
    tf.paragraphs[0].font.size = Pt(13)
    tf.paragraphs[0].font.color.rgb = C_NAVY_DARK

    achievements = [
        ("Working POSIX Shell: ", "Successfully constructed a specialized C-based shell demonstrating core Operating Systems concepts (fork, execvp, waitpid, signals)."),
        ("DevOps Tool Consolidation: ", "Bridged Git, Docker, Make, Smart Build, and Deploy commands into a unified developer interface."),
        ("Native Pipeline Automation: ", "Built a zero-overhead CI/CD pipeline runner (.workflow) with step gating and failure isolation."),
        ("Production-Grade Logging: ", "Implemented timestamped audit logging and history persistence for complete visibility.")
    ]
    for title, desc in achievements:
        p = tf.add_paragraph()
        p.text = f"• {title}"
        p.font.bold = True
        p.font.size = Pt(12)
        p.font.color.rgb = C_EMERALD
        pd = tf.add_paragraph()
        pd.text = f"   {desc}"
        pd.font.size = Pt(11)
        pd.font.color.rgb = C_TEXT_MUTED

    # Right Card: Future Enhancements
    add_card(slide15, Inches(6.8), Inches(1.8), Inches(5.7), Inches(5.1), "Planned Future Enhancements", C_CYAN_ACCENT)
    tb2 = slide15.shapes.add_textbox(Inches(7.0), Inches(2.4), Inches(5.3), Inches(4.3))
    tf2 = tb2.text_frame
    tf2.word_wrap = True
    tf2.text = "Roadmap for Version 2.0:"
    tf2.paragraphs[0].font.bold = True
    tf2.paragraphs[0].font.size = Pt(13)
    tf2.paragraphs[0].font.color.rgb = C_CYAN_ACCENT

    future = [
        ("Background Job Control (&): ", "Support asynchronous background process execution with 'jobs', 'bg', and 'fg' commands."),
        ("I/O Redirection & Piping (|): ", "Extend parsing to support inter-process pipes ('|') and file redirection ('>', '>>', '<')."),
        ("Kubernetes Cluster Dashboard: ", "Add 'k8s status' module to monitor pods, services, and namespaces via kubectl integration."),
        ("Webhook Notifications: ", "Send Slack/Discord/Email notifications upon pipeline completion or failure."),
        ("Multi-Node Orchestration: ", "Run parallel workflow steps across remote servers via SSH agent integration.")
    ]
    for title, desc in future:
        p = tf2.add_paragraph()
        p.text = f"• {title}"
        p.font.bold = True
        p.font.size = Pt(11.5)
        p.font.color.rgb = C_NAVY_DARK
        pd = tf2.add_paragraph()
        pd.text = f"   {desc}"
        pd.font.size = Pt(11)
        pd.font.color.rgb = C_TEXT_MUTED

    # =========================================================================
    # SLIDE 16: THANK YOU & Q&A (DARK THEME)
    # =========================================================================
    slide16 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide16, C_NAVY_DARK)

    # Accent decorative bar
    accent_bar16 = slide16.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(0.4), Inches(7.5))
    accent_bar16.fill.solid()
    accent_bar16.fill.fore_color.rgb = C_CYAN_ACCENT
    accent_bar16.line.fill.background()

    # Center card
    card16 = slide16.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(2.5), Inches(1.5), Inches(8.33), Inches(4.5))
    card16.fill.solid()
    card16.fill.fore_color.rgb = C_NAVY_LIGHT
    card16.line.color.rgb = C_CYAN_ACCENT
    card16.line.width = Pt(2)
    tf16 = card16.text_frame
    tf16.word_wrap = True

    p = tf16.paragraphs[0]
    p.text = "Thank You!"
    p.font.size = Pt(44)
    p.font.bold = True
    p.font.color.rgb = C_TEXT_LIGHT
    p.alignment = PP_ALIGN.CENTER

    p2 = tf16.add_paragraph()
    p2.text = "DevOps Mini Shell (devops-shell)"
    p2.font.size = Pt(22)
    p2.font.bold = True
    p2.font.color.rgb = C_CYAN_ACCENT
    p2.alignment = PP_ALIGN.CENTER

    p3 = tf16.add_paragraph()
    p3.text = "Operating Systems and System Programming Project\n"
    p3.font.size = Pt(14)
    p3.font.color.rgb = RGBColor(148, 163, 184)
    p3.alignment = PP_ALIGN.CENTER

    p4 = tf16.add_paragraph()
    p4.text = "TEAM MEMBERS:"
    p4.font.size = Pt(14)
    p4.font.bold = True
    p4.font.color.rgb = C_EMERALD
    p4.alignment = PP_ALIGN.CENTER

    p5 = tf16.add_paragraph()
    p5.text = "01 Gokul Arnav   |   02 Wasim   |   03 Binamra   |   04 Yogith"
    p5.font.size = Pt(14)
    p5.font.color.rgb = C_TEXT_LIGHT
    p5.alignment = PP_ALIGN.CENTER

    p6 = tf16.add_paragraph()
    p6.text = "\nQuestions & Feedback Welcome"
    p6.font.size = Pt(16)
    p6.font.bold = True
    p6.font.color.rgb = C_CYAN_ACCENT
    p6.alignment = PP_ALIGN.CENTER

    prs.save(output_path)
    print(f"Successfully generated presentation with {len(prs.slides)} slides at: {output_path}")

if __name__ == "__main__":
    out = "DevOps_Mini_Shell_Project_Presentation.pptx"
    build_presentation(out)
