"""File management functions for txtRefine."""

import os
from pathlib import Path
from typing import List, Optional, Dict, Any
from datetime import datetime


def list_input_files(input_dir: str = "input") -> List[str]:
    """List all .txt files in the input folder."""
    input_folder = Path(input_dir)

    if not input_folder.exists():
        print(f"❌ Folder '{input_dir}' not found")
        return []

    txt_files = list(input_folder.glob("*.txt"))
    return [f.name for f in txt_files]


def list_output_files(output_dir: str = "output") -> List[str]:
    """List all files in the output folder."""
    output_folder = Path(output_dir)

    if not output_folder.exists():
        return []

    return [f.name for f in output_folder.iterdir() if f.is_file()]


def validate_file_path(file_path: str) -> bool:
    """Validate if a file path exists and is accessible."""
    try:
        path = Path(file_path)
        return path.exists() and path.is_file()
    except Exception:
        return False


def read_text_file(file_path: str, encoding: str = "utf-8") -> Optional[str]:
    """Read text content from a file."""
    try:
        with open(file_path, 'r', encoding=encoding) as f:
            return f.read()
    except Exception as e:
        print(f"❌ Error reading file {file_path}: {e}")
        return None


def write_text_file(file_path: str, content: str, encoding: str = "utf-8") -> bool:
    """Write text content to a file."""
    try:
        # Ensure directory exists
        Path(file_path).parent.mkdir(parents=True, exist_ok=True)

        with open(file_path, 'w', encoding=encoding) as f:
            f.write(content)
        return True
    except Exception as e:
        print(f"❌ Error writing to file {file_path}: {e}")
        return False


def get_file_info(file_path: str) -> Dict[str, Any]:
    """Get detailed information about a file."""
    try:
        path = Path(file_path)
        stat = path.stat()

        return {
            'name': path.name,
            'path': str(path.absolute()),
            'size': stat.st_size,
            'size_kb': f"{stat.st_size / 1024:.1f} KB",
            'modified': datetime.fromtimestamp(stat.st_mtime),
            'exists': True
        }
    except Exception as e:
        return {
            'name': Path(file_path).name,
            'path': file_path,
            'size': 0,
            'size_kb': "0 KB",
            'modified': None,
            'exists': False,
            'error': str(e)
        }


def get_file_stats(file_paths: List[str]) -> Dict[str, Any]:
    """Get statistics for multiple files."""
    total_size = 0
    total_words = 0
    file_count = len(file_paths)

    for file_path in file_paths:
        if validate_file_path(file_path):
            info = get_file_info(file_path)
            total_size += info['size']

            # Count words if it's a text file
            content = read_text_file(file_path)
            if content:
                total_words += len(content.split())

    return {
        'file_count': file_count,
        'total_size': total_size,
        'total_size_kb': f"{total_size / 1024:.1f} KB",
        'total_words': total_words,
        'avg_file_size_kb': f"{(total_size / max(file_count, 1)) / 1024:.1f} KB",
        'avg_words_per_file': total_words // max(file_count, 1)
    }


def create_backup_file(original_path: str, backup_dir: str = "backups") -> Optional[str]:
    """Create a backup of a file with timestamp."""
    try:
        original = Path(original_path)
        if not original.exists():
            return None

        # Create backup directory
        backup_path = Path(backup_dir)
        backup_path.mkdir(parents=True, exist_ok=True)

        # Create backup filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_filename = f"{original.stem}_{timestamp}{original.suffix}"
        backup_file = backup_path / backup_filename

        # Copy file
        import shutil
        shutil.copy2(original_path, backup_file)

        return str(backup_file)

    except Exception as e:
        print(f"❌ Error creating backup of {original_path}: {e}")
        return None


def cleanup_old_backups(backup_dir: str = "backups", max_backups: int = 10) -> int:
    """Clean up old backup files, keeping only the most recent ones."""
    try:
        backup_path = Path(backup_dir)
        if not backup_path.exists():
            return 0

        # Get all backup files
        backup_files = list(backup_path.glob("*"))

        if len(backup_files) <= max_backups:
            return 0

        # Sort by modification time (newest first)
        backup_files.sort(key=lambda x: x.stat().st_mtime, reverse=True)

        # Remove older files
        files_to_remove = backup_files[max_backups:]
        removed_count = 0

        for file_path in files_to_remove:
            try:
                file_path.unlink()
                removed_count += 1
            except Exception as e:
                print(f"❌ Error removing backup {file_path}: {e}")

        return removed_count

    except Exception as e:
        print(f"❌ Error cleaning backups: {e}")
        return 0


def generate_output_filename(input_filename: str, prefix: str = "refined") -> str:
    """Generate output filename with prefix."""
    input_path = Path(input_filename)
    return f"{prefix}_{input_path.name}"


def ensure_directories(*dirs: str) -> None:
    """Ensure that specified directories exist."""
    for dir_path in dirs:
        Path(dir_path).mkdir(parents=True, exist_ok=True)


def validate_directory(dir_path: str) -> bool:
    """Validate if a directory exists and is accessible."""
    try:
        path = Path(dir_path)
        if not path.exists():
            return False
        if not path.is_dir():
            return False
        # Try to list contents to check permissions
        list(path.iterdir())
        return True
    except Exception:
        return False
