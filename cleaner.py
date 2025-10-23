"""Small helper to remove common temporary files in a repo."""
import os
import shutil
from pathlib import Path

def clean(path='.'):
    p = Path(path)
    removed = []
    for pattern in ['__pycache__', '.pytest_cache', '*.pyc', '.venv', 'dist', 'build']:
        for match in p.rglob(pattern):
            try:
                if match.is_dir():
                    shutil.rmtree(match)
                else:
                    match.unlink()
                removed.append(str(match))
            except Exception:
                pass
    return removed

if __name__ == '__main__':
    removed = clean('.')
    print('Removed items:')
    for r in removed:
        print(' -', r)
