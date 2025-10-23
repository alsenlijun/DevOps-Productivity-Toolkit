"""DevOps Productivity Toolkit - simple CLI entrypoint."""
import os
import subprocess
import sys
from pathlib import Path
import click

@click.group()
def cli():
    """DevOps Productivity Toolkit: small utilities for local use."""
    pass

@cli.command()
@click.option('--output', '-o', default='CHANGELOG.md', help='Output file')
def changelog(output):
    """Generate a basic changelog from git commits (conventional commit lines preferred)."""
    try:
        p = subprocess.run(['git', 'log', '--pretty=%s'], capture_output=True, text=True, check=True)
        commits = p.stdout.strip().splitlines()
    except Exception as e:
        click.echo(f"Error reading git log: {e}")
        sys.exit(1)

    # naive grouping: list commits under Unreleased
    lines = ['# Changelog', '', '## Unreleased', '']
    for c in commits:
        lines.append(f'- {c}')
    Path(output).write_text('\n'.join(lines), encoding='utf-8')
    click.echo(f'Wrote changelog to {output}')

@cli.command()
def ci_check():
    """Run quick local CI checks (lint placeholder)."""
    click.echo('Running quick checks...')
    try:
        subprocess.run([sys.executable, '-m', 'flake8', 'src'], check=False)
    except FileNotFoundError:
        click.echo('flake8 not installed. Install with: pip install flake8')
    click.echo('Done.')

@cli.command()
@click.option('--app', required=True, help='Path to your Python app entrypoint (e.g. main.py)')
@click.option('--output', default='Dockerfile', help='Dockerfile path to write')
def dockerize(app, output):
    """Create a minimal Dockerfile for a Python app."""
    content = f"""FROM python:3.11-slim
WORKDIR /app
COPY . /app
RUN pip install --no-cache-dir -r requirements.txt || true
CMD ["python", "{app}"]
""""
    Path(output).write_text(content, encoding='utf-8')
    click.echo(f'Generated {output}')

if __name__ == '__main__':
    cli()
