"""
DevPain v2.0 - Git History + File Analysis (Windows Fixed)
"""
import os, sys
from collections import Counter
from datetime import datetime, timedelta
import subprocess

def safe_git_files(days=180):
    """Get files changed most in last N days via git (safe fallback)."""
    try:
        since = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")
        result = subprocess.run(['git', 'log', f'--since={since}', '--name-only', '--pretty=format:'],
                              capture_output=True, text=True, cwd='.')
        counter = Counter()
        for line in result.stdout.splitlines():
            path = line.strip()
            if path and path.endswith(('.py','.js','.java','.ts','.go','.rb','.cpp','.c')):
                counter[path] += 1
        return counter.most_common(20)
    except:
        print("Git not found - skipping git history")
        return []

def get_code_files():
    """Scan folder for code files."""
    code_ext = ('.py','.js','.java','.ts','.go','.rb','.cpp','.c','.html','.css')
    files = []
    for root, _, fs in os.walk('.'):
        for f in fs:
            if f.endswith(code_ext):
                rel_path = os.path.relpath(os.path.join(root, f), '.')
                files.append(rel_path)
    return files[:20]

def generate_report(git_files, code_files):
    """Generate markdown report."""
    lines = []
    lines.append("# DevPain v2 Report")
    lines.append("")
    lines.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append("")

    # Git hotspots section
    lines.append("## Git Hotspots (Most Changed Files)")
    lines.append("| File | Changes |")
    lines.append("|------|---------|")
    if git_files:
        for file_path, count in git_files:
            lines.append(f"| `{file_path}` | {count} |")
    else:
        lines.append("| No git history found | - |")
    
    lines.append("")

    # Current files section
    lines.append("## Current Code Files")
    lines.append("| File | Size |")
    lines.append("|------|--------|")
    for file_path in code_files:
        try:
            size = os.path.getsize(file_path) / 1024
            lines.append(f"| `{file_path}` | {size:.1f}KB |")
        except:
            lines.append(f"| `{file_path}` | Error |")
    
    # Write with UTF-8 encoding
    with open("v2_devpain_report.md", "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    
    print(f"Report saved: v2_devpain_report.md")
    print(f"Git files: {len(git_files)}, Code files: {len(code_files)}")

def main():
    print("DevPain v2 - Git + File Analysis")
    print("=" * 40)
    
    git_files = safe_git_files()
    code_files = get_code_files()
    
    generate_report(git_files, code_files)
    print("COMPLETE")

if __name__ == "__main__":
    main()
