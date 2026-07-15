# FocusGuardian

A distraction detection and productivity assistant for students.

FocusGuardian monitors active applications and browser tabs and reminds users when they spend too much time on distracting content.

---

## Features

- Active window detection
- Process monitoring
- Browser tab title detection
- Keyword based distraction recognition
- Configurable monitoring rules
- Timer based reminders
- Popup notifications

---

## Architecture

Detector
↓
Rule Engine
↓
Timer Engine
↓
Overlay Engine

---

## Example

Watching YouTube videos for an extended period triggers:

"You have been distracted by:
Benson Boone - In The Stars (Official Music Video)

Return to your task."

---

## Technologies

- Python
- psutil
- pywin32
- tkinter

---

## Project Status

Current Version:
v0.1

Status:
Prototype complete and functional.

---

## Roadmap

### v0.2
- System tray support
- Background execution

### v0.3
- Productivity analytics
- Daily statistics

### v0.4
- CSV export
- Session reports

### v0.5
- AI productivity suggestions

### v1.0
- Installer
- Production release

---

## Repository

Development progress and milestones are documented through Git commits and releases.