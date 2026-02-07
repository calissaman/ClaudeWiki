# Project Manager Subagent Setup

## Overview

The Project Manager subagent is a specialized AI agent designed to verify project structure, ensure documentation accuracy, validate file existence, and maintain consistency between documentation and actual implementation.

## Purpose

During the ClaudeWiki project development, the project manager subagent was used to:
- Verify all files mentioned in README.md actually exist
- Check that project structure matches documentation
- Validate file references and links
- Ensure consistency between documentation and implementation
- Identify missing or outdated documentation

## How to Invoke

### Using Claude Code CLI

The project manager subagent can be invoked using the Task tool with specialized agent configuration:

```python
# In your Claude Code session
Task(
    subagent_type="general-purpose",
    description="Verify project structure",
    prompt="""Please act as a project manager and verify the ClaudeWiki project structure.

    Tasks:
    1. Read README.md and extract all file references
    2. Verify each mentioned file exists in the project
    3. Check that file descriptions match actual file content
    4. Validate directory structure matches documentation
    5. Identify any missing files or outdated references
    6. Ensure all examples and code snippets are accurate
    7. Verify version consistency across files

    Provide a comprehensive report of findings."""
)
```

## Verification Criteria

The project manager evaluates projects across multiple dimensions:

### 1. **File Existence Verification**
- All files mentioned in documentation exist
- No broken file references
- Correct file paths and locations

### 2. **Documentation Accuracy**
- File descriptions match actual content
- Code examples are correct and runnable
- API documentation matches implementation
- Version numbers are consistent

### 3. **Project Structure**
- Directory organization follows documented structure
- Configuration files are present and valid
- Dependencies are properly documented

### 4. **Completeness**
- All promised features have corresponding files
- Test files cover documented functionality
- Documentation covers all implemented features

### 5. **Consistency**
- Naming conventions are uniform
- File organization is logical
- README matches actual project state

## Example Verification Process

### Step 1: Extract File References

```python
# From README.md:
files_mentioned = [
    "app.py",
    "eval_suite.py",
    "run_eval.py",
    "demo.py",
    "system_prompt.txt",
    "EVALUATION_RESULTS.md",
    ".env.example"
]
```

### Step 2: Verify Existence

```bash
# Check each file exists
for file in files_mentioned:
    if os.path.exists(file):
        print(f"✅ {file}")
    else:
        print(f"❌ {file} - MISSING")
```

### Step 3: Validate Content

```python
# Verify file descriptions match content
- app.py: Check it's a Flask application with /api/chat endpoint
- eval_suite.py: Verify 70 test cases exist
- demo.py: Confirm it has --version, --help, --quick flags
- system_prompt.txt: Ensure it contains Wikipedia search instructions
```

### Step 4: Generate Report

```
PROJECT VERIFICATION REPORT
===========================

Files Checked: 7
✅ Found: 7
❌ Missing: 0

Documentation Accuracy:
✅ All file descriptions match actual content
✅ Code examples are runnable
✅ API endpoints documented correctly

Project Structure:
✅ Directory organization logical
✅ Configuration files present
✅ Dependencies documented in README

Completeness:
✅ All features have corresponding files
✅ Evaluation suite matches documentation (70 cases)
✅ Demo mode properly implemented

Recommendations:
- Consider adding CHANGELOG.md for version tracking
- Add .gitignore if planning to use version control
```

## Project Manager Checklist

When verifying a project, the subagent checks:

- [ ] **README.md** exists and is comprehensive
- [ ] All files mentioned in README exist
- [ ] File descriptions are accurate
- [ ] Directory structure is documented
- [ ] Installation instructions are correct
- [ ] Usage examples work as documented
- [ ] Configuration files (.env.example) are present
- [ ] Dependencies are listed and accurate
- [ ] API endpoints match documentation
- [ ] Test suites match documented coverage
- [ ] Version numbers are consistent
- [ ] License file is present (if applicable)
- [ ] Contributing guidelines exist (if open source)

## Integration Example

### Before Project Manager Review

```markdown
# README.md

## Files
- app.py - Main application
- database.py - Database logic
- utils.py - Utility functions
```

### After Project Manager Verification

```markdown
# README.md

## Project Structure

```
wikipedia-tool/
├── app.py                      # Flask server with /api/chat endpoint
├── eval_suite.py               # 70 test cases across 7 dimensions
├── run_eval.py                 # Test runner for evaluation suite
├── demo.py                     # Standalone Wikipedia demo (no API key needed)
├── system_prompt.txt           # System instructions for Claude
├── EVALUATION_RESULTS.md       # Test results and analysis
├── .env.example                # Environment variables template
├── SUBAGENT_CODE_REVIEWER.md   # Code review subagent documentation
└── SUBAGENT_PROJECT_MANAGER.md # This file
```

✅ All files verified to exist
✅ All descriptions match actual file content
```

## Best Practices for Using Project Manager

1. **Run Early and Often**: Verify project structure after major changes
2. **Update Documentation First**: Keep README in sync with implementation
3. **Use for Onboarding**: Help new contributors understand project structure
4. **Validate Before Release**: Ensure documentation matches shipped code
5. **Track Changes**: Document what was added/removed/modified

## Common Issues Detected

The project manager subagent commonly identifies:

1. **Missing Files**: Documentation references non-existent files
2. **Broken Links**: Internal file references that don't resolve
3. **Outdated Descriptions**: File descriptions don't match current implementation
4. **Inconsistent Naming**: Files named differently than documented
5. **Missing Documentation**: Implemented features not documented
6. **Version Mismatches**: Different version numbers in different files
7. **Incorrect Paths**: Wrong directory structures or file locations
8. **Missing Dependencies**: Undocumented required packages or files

## Automated Verification Script

You can create an automated verification script based on project manager findings:

```python
#!/usr/bin/env python3
"""
Project structure verification script
Generated from project manager subagent recommendations
"""

import os
import sys

def verify_project_structure():
    """Verify all required files exist."""
    required_files = [
        'app.py',
        'eval_suite.py',
        'run_eval.py',
        'demo.py',
        'system_prompt.txt',
        'README.md',
        '.env.example',
    ]

    missing = []
    for file in required_files:
        if not os.path.exists(file):
            missing.append(file)
            print(f"❌ Missing: {file}")
        else:
            print(f"✅ Found: {file}")

    if missing:
        print(f"\n❌ {len(missing)} files missing!")
        return False
    else:
        print(f"\n✅ All {len(required_files)} required files present!")
        return True

if __name__ == "__main__":
    success = verify_project_structure()
    sys.exit(0 if success else 1)
```

## Continuous Integration

The project manager subagent findings can be integrated into CI/CD:

```yaml
# .github/workflows/verify-structure.yml
name: Verify Project Structure

on: [push, pull_request]

jobs:
  verify:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Verify project structure
        run: python3 verify_structure.py
```

## Output Format

The project manager provides structured reports:

```
================================================================================
PROJECT MANAGER VERIFICATION REPORT
================================================================================

Project: ClaudeWiki
Date: 2026-02-07
Files Verified: 7

FILE EXISTENCE CHECK
--------------------
✅ app.py
✅ eval_suite.py
✅ run_eval.py
✅ demo.py
✅ system_prompt.txt
✅ README.md
✅ .env.example

DOCUMENTATION ACCURACY
----------------------
✅ app.py: Flask server with /api/chat endpoint (MATCH)
✅ eval_suite.py: Contains 70 test cases (VERIFIED)
✅ demo.py: Has --version, --help, --quick flags (CONFIRMED)
✅ All code examples in README.md are accurate

PROJECT STRUCTURE
-----------------
✅ Directory organization matches documentation
✅ All configuration files present
✅ Dependencies properly documented

RECOMMENDATIONS
---------------
1. Consider adding CHANGELOG.md for version tracking
2. Add CONTRIBUTING.md if planning open source release
3. Consider adding .github/workflows for CI/CD

OVERALL STATUS: ✅ PASS
All critical verification checks passed.
================================================================================
```

## Related Files

- `README.md` - Main project documentation (verification target)
- `SUBAGENT_CODE_REVIEWER.md` - Complementary code review subagent
- `demo.py`, `app.py`, `eval_suite.py` - Verified project files

## References

- [Semantic Versioning](https://semver.org/)
- [Keep a Changelog](https://keepachangelog.com/)
- [README Best Practices](https://github.com/matiassingers/awesome-readme)
