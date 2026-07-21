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



# FocusGuardian Development Log

## Milestone — Core Analytics & Automated Testing

**Status:** Completed  
**Git Commit:** `0ebc7a2`

### Overview

This milestone significantly expanded FocusGuardian from a basic distraction-monitoring system into a modular focus analytics platform.

The application can now track distraction activity, measure distraction sessions, calculate a weighted Focus Score, adapt reminder frequency, generate reports, and evaluate focus streaks.

A complete automated pytest suite was also introduced to protect the core analytics logic from regressions.

---

## Major Features Added

### 1. Adaptive Reminder Engine

Implemented an adaptive reminder system that changes reminder frequency according to the user's distraction count and current Focus Score.

Higher distraction levels result in more frequent reminders.

The system currently supports reminder intervals ranging from 60 seconds for low distraction levels down to 5 seconds during severe focus loss.

---

### 2. Weighted Focus Score Engine

Implemented a Focus Score ranging from 0 to 100.

Different distraction categories have different penalties.

Examples include:

- YouTube
- Reddit
- Instagram
- Spotify
- Facebook
- Twitter/X
- Browser-level distractions

This allows FocusGuardian to evaluate distraction severity rather than treating every distraction equally.

The score is prevented from dropping below zero.

---

### 3. Session Tracking

Added a session engine capable of tracking how long the user remains inside a distracting activity.

The system can:

- Start a distraction session
- Maintain the active session while the same distraction continues
- Finish the session when the user leaves the distraction
- Track the session duration
- Support transitions between distraction targets

This makes FocusGuardian capable of measuring both distraction frequency and distraction duration.

---

### 4. Time Statistics

Added persistent time-statistics tracking for distraction sessions.

This creates the foundation for future analytics such as:

- Total distraction time
- Daily distraction duration
- Category-specific time usage
- Long-term focus trends

---

### 5. Daily Report Engine

Implemented daily reporting capable of calculating:

- Total distractions
- Most frequent distraction
- Category breakdown

The report system also handles dates for which no statistics are available.

---

### 6. Weekly Report Engine

Implemented aggregation of distraction statistics across multiple days.

The weekly report provides:

- Total distractions
- Category totals
- Worst distraction category

An empty-data edge case was also fixed so that the reporting engine safely returns:

- Total: 0
- Worst category: None
- Categories: empty

instead of failing.

---

### 7. Focus Streak Engine

Implemented focus streak calculation.

A day contributes to the streak when its Focus Score satisfies the configured streak threshold.

The streak engine was refactored to use the main Focus Score Engine instead of maintaining a separate scoring formula.

This establishes the Focus Score Engine as the single source of truth for focus evaluation.

---

## Architecture Improvement

Previously, FocusGuardian contained two different interpretations of focus quality:

1. The Focus Score Engine used category-specific weighted penalties.
2. The Streak Engine used a separate `100 - distractions × 10` calculation.

This could produce contradictory results.

The architecture was refactored so that:

Distraction Statistics
        ↓
Focus Score Engine
        ↓
Canonical Focus Score
        ↓
Streak Engine

This eliminates duplicated scoring logic and improves consistency across the application.

---

## Automated Testing

The previous manual test scripts were converted into a proper automated pytest test suite.

The suite currently tests:

- Adaptive reminder behavior
- Focus Score calculations
- Weighted distraction penalties
- Score boundaries
- Unknown-category handling
- Daily report generation
- Missing report data
- Streak calculation
- Streak threshold boundaries
- Chronological streak processing
- Weekly report aggregation
- Empty weekly statistics
- Other analytics edge cases

### Final Test Result

32 tests collected  
32 tests passed  
0 tests failed

This establishes an automated regression-testing foundation for future development.

---

## Repository Cleanup

The repository was also cleaned for proper Git version control.

Ignored development/runtime artifacts include:

- `.venv/`
- `__pycache__/`
- `.pytest_cache/`
- Python bytecode files
- Generated runtime time-statistics data

A `.gitkeep` file preserves the required data directory structure without requiring generated runtime files to be committed.

---

## Verification

Before this milestone was committed:

- Python modules compiled successfully
- Automated tests passed
- Git staged changes were manually inspected
- Accidental temporary files were removed
- Runtime statistics were excluded from the milestone commit
- Repository working tree was verified after the push

Final verification:

`32 passed`

---

## Git Checkpoint

Commit:

`0ebc7a2`

Commit message:

`feat: add focus analytics engines and automated test suite`

The milestone was successfully pushed to the main GitHub branch.

---

## Current State

FocusGuardian now has a substantially more mature core foundation consisting of:

- Windows distraction detection
- Rule-based classification
- Reminder overlays
- Adaptive reminder timing
- Distraction statistics
- Weighted Focus Score
- Session tracking
- Time tracking
- Daily reports
- Weekly reports
- Focus streaks
- Automated regression testing

The next development stage will focus on completing remaining core reliability work before beginning the dedicated UI/UX layer.