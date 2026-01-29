# 📚 MangaShelf

MangaShelf is a stylish command-line application built in Python to help you track your manga reading progress, ratings, and statuses.

## ✨ Features

- **Store Detailed Info**: Track title, author, total chapters, current chapter, status, rating, and personal notes.
- **Reading Statuses**: Easily manage titles as `Reading`, `Completed`, `On Hold`, `Dropped`, or `Plan to Read`.
- **Sorting & Filtering**: View your list sorted by title, rating, or last updated date.
- **Search System**: Find specific titles or authors quickly.
- **Progress Tracking**: Update your current chapter with a simple menu option.
- **Statistics**: Get insights into your reading habits, including total count and average rating.
- **Local Storage**: All data is saved locally in a `manga_data.json` file.
- **Beautiful CLI**: Powered by `rich` for a clean, modern terminal experience.

## 🚀 Getting Started

### Prerequisites

- Python 3.8+
- `rich` library

### Installation

1. Clone or download the repository.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Usage

Run the application using:

```bash
python main.py
```

## 🛠️ Project Structure

- `main.py`: Entry point.
- `mangashelf/`: Core logic package.
  - `models.py`: Data structures.
  - `storage.py`: JSON persistent storage.
  - `cli.py`: Interactive menu and UI.
- `manga_data.json`: Local database (created on first run).
