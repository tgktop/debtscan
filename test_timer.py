"""
DevPain Test Timer - Fixed for Windows
"""
import os
from datetime import datetime

def scan_tests():
    test_files = []
    for root, _, files in os.walk('.'):
        for f in files:
            if 'test' in f.lower() and f.endswith('.py'):
                test_files.append(os.path.join(root, f))
    
    lines = ["# Test Files Report", "", f"Generated: {datetime.now().strftime('%Y-%m-%d')}", ""]
    lines.append("| Test File | Size |")
    lines.append("|-----------|------|")
    
    if test_files:
        for tf in test_files:
            size = os.path.getsize(tf) / 1024
            lines.append(f"| `{tf}` | {size:.1f}KB |")
    else:
        lines.append("| No test files found | - |")
    
    with open("test_report.md", "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print("Test report saved: test_report.md")

if __name__ == "__main__":
    scan_tests()
