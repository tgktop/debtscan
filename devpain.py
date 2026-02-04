"""
DevPain v1.0 - Technical Debt Hotspot Detector
Works WITHOUT Git - analyzes your current folder immediately
Save as devpain.py and run: python devpain.py
"""

import os
import sys
from collections import Counter
from datetime import datetime, timedelta
from typing import List, Tuple
import glob

def get_current_folder() -> str:
    """Return current working directory as analysis root."""
    return os.getcwd()

def get_code_files(max_files: int = 50) -> List[Tuple[str, int]]:
    """
    Scan current folder for code files and count them by type.
    Simulates "hotspot" analysis without git history.
    """
    code_extensions = ('.py', '.js', '.ts', '.java', '.cs', '.go', '.rb', '.cpp', '.c', '.h', '.html', '.css')
    counter = Counter()
    
    # Walk current directory and subdirs
    for root, dirs, files in os.walk('.'):
        for file in files:
            if max_files <= 0:
                break
            if file.endswith(code_extensions):
                rel_path = os.path.relpath(os.path.join(root, file), '.')
                counter[rel_path] += 1
                max_files -= 1
    
    return counter.most_common(30)

def analyze_file_complexity(file_path: str) -> dict:
    """Simple file analysis: lines of code, comments, size."""
    try:
        lines = []
        comment_lines = 0
        blank_lines = 0
        
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            lines = f.readlines()
        
        for line in lines:
            stripped = line.strip()
            if not stripped:
                blank_lines += 1
            elif stripped.startswith('#') or stripped.startswith('//') or stripped.startswith('/*'):
                comment_lines += 1
        
        loc = len([l for l in lines if l.strip() and not l.strip().startswith('#') 
                  and not l.strip().startswith('//')])
        
        return {
            'lines_total': len(lines),
            'lines_code': loc,
            'comments': comment_lines,
            'blank': blank_lines,
            'complexity_score': loc + comment_lines  # Simple heuristic
        }
    except:
        return {'lines_total': 0, 'lines_code': 0, 'comments': 0, 'blank': 0, 'complexity_score': 0}

def generate_markdown_report(
    folder_path: str,
    files: List[Tuple[str, int]],
    output_path: str = "devpain_report.md"
) -> None:
    """Create comprehensive markdown report."""
    lines = []
    lines.append("# 🚨 DevPain Report - Technical Debt Analysis")
    lines.append("")
    lines.append(f"- **Folder**: `{folder_path}`")
    lines.append(f"- **Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append(f"- **Files analyzed**: {len(files)}")
    lines.append("")
    
    # Top files table
    lines.append("## 🔥 Top Files by Complexity")
    lines.append("")
    lines.append("| Rank | File | LOC | Comments | Size (KB) | Risk Score |")
    lines.append("|------|------|-----|----------|-----------|------------|")
    
    for idx, (path, _) in enumerate(files, 1):
        stats = analyze_file_complexity(path)
        size_kb = os.path.getsize(path) / 1024
        risk_score = stats['complexity_score'] * 1.2 + (size_kb / 10)
        
        lines.append(f"| {idx} | `{path}` | {stats['lines_code']} | {stats['comments']} | "
                    f"{size_kb:.1f} | {int(risk_score)} |")
    
    lines.append("")
    lines.append("## 📊 Risk Score Explanation")
    lines.append("")
    lines.append("- **Risk Score** = (Lines of Code × 1.2) + Comments + (File Size ÷ 10)")
    lines.append("- **Higher score** = higher maintenance risk")
    lines.append("- **Target these files first** for refactoring")
    lines.append("")
    lines.append("## 🎯 Next Actions")
    lines.append("")
    lines.append("- Review top 5 files for refactoring opportunities")
    lines.append("- Add tests for files with high comment ratios")
    lines.append("- Consider extracting complex functions into modules")
    lines.append("")
    lines.append("*Run this weekly to track technical debt growth.*")
    
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    
    print(f"✅ Report saved: {output_path}")
    print(f"📈 Found {len(files)} code files to analyze")

def main():
    print("🚀 DevPain - Technical Debt Detector")
    print("=" * 50)
    
    folder = get_current_folder()
    print(f"📁 Analyzing: {folder}")
    
    files = get_code_files()
    if not files:
        print("❌ No code files found. Add some .py, .js, etc files and try again.")
        return
    
    generate_markdown_report(folder, files)
    print("🎉 Analysis complete!")

if __name__ == "__main__":
    main()
