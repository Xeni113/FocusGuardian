# FocusGuardian Development Log

Author: Chinmoy Das
GitHub: https://github.com/Xeni113/FocusGuardian

---

## 15 July 2026

### Goal
Build an AI-assisted productivity system capable of detecting distractions and reminding users to return to work.

### Features completed
- Created project architecture
- Implemented active window detection
- Implemented process identification
- Added keyword-based distraction detection
- Added JSON configuration system
- Connected project to GitHub
- Created evidence collection system

### Technical challenges
- Import errors due to missing __init__.py
- Git remote misconfiguration
- Indentation errors in main loop

### Lessons learned
- Python package imports
- Git workflow basics
- Windows process monitoring using pywin32

### Next target
Implement actual popup reminder window using Tkinter.


# FocusGuardian Development Log

---

## 15 July 2026 — Project Initialization

### Completed
- Created project architecture
- Created detector engine using:
  - win32gui
  - win32process
  - psutil
- Successfully detects:
  - active process name
  - active window title
  - process PID
  - timestamp

### Rule Engine
- Implemented process-based monitoring
- Implemented keyword-based monitoring
- Added configurable JSON rules

### Timer Engine
- Built distraction duration tracker
- Tracks continuous exposure to distractions
- Supports configurable reminder intervals

### Overlay Engine
- Implemented tkinter popup overlay
- Added always-on-top reminder window
- Added "Back to Work" button

### Integration
- Connected:
  Detector → Rule Engine → Timer → Overlay

### Successful Demonstration
Verified working with:
- YouTube
- Music videos
- Browser distractions

System successfully:
1. Detects distraction.
2. Tracks duration.
3. Displays reminder popup.
4. Resets timer after returning to work.

### Evidence
Stored:
- screenshots/
- videos/

### GitHub
Initial commit pushed successfully.

## v0.2 — Configurable Rule Engine
Date: 15 July 2026

### Completed
- Moved distraction keywords into external JSON configuration
- Moved monitored processes into external JSON configuration
- Added configurable reminder delay
- Refactored rule engine to load settings dynamically
- Verified compatibility with existing popup system

### Files Added
config/rules.json
data/stats.json

### Files Modified
src/rule_engine.py
main.py

### Status
Stable and tested successfully.