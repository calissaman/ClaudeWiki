# Code Reviewer Subagent Setup

## Overview

The Code Reviewer subagent is a specialized AI agent designed to perform comprehensive code reviews, identify improvement opportunities, and provide actionable feedback on code quality, structure, and best practices.

## Purpose

During the ClaudeWiki project development, the code reviewer subagent was used to:
- Review the `demo.py` file for quality and best practices
- Identify 10 specific improvement suggestions
- Ensure code follows Python standards and conventions
- Detect potential bugs, performance issues, and maintainability concerns

## How to Invoke

### Using Claude Code CLI

The code reviewer subagent can be invoked using the Task tool with specialized agent configuration:

```python
# In your Claude Code session
Task(
    subagent_type="general-purpose",
    description="Review demo.py code",
    prompt="""Please perform a comprehensive code review of demo.py.

    Focus on:
    1. Code quality and Python best practices
    2. Performance optimizations
    3. Error handling and edge cases
    4. Code organization and structure
    5. Documentation and readability
    6. Type hints and function signatures
    7. Security considerations
    8. DRY (Don't Repeat Yourself) principle
    9. Input validation
    10. User experience improvements

    Provide specific, actionable suggestions with code examples where appropriate."""
)
```

## Review Criteria

The code reviewer evaluates code across multiple dimensions:

### 1. **Code Structure & Organization**
- Proper separation of concerns
- Logical function decomposition
- Clear module structure

### 2. **Python Best Practices**
- PEP 8 compliance
- Pythonic idioms
- Type hints and annotations
- Docstrings and documentation

### 3. **Error Handling**
- Specific exception catching
- Graceful error recovery
- User-friendly error messages

### 4. **Performance**
- Efficient algorithms
- Resource management
- Caching strategies

### 5. **Security**
- Input validation
- Injection prevention
- Safe data handling

### 6. **Maintainability**
- Code readability
- Magic number elimination
- DRY principle adherence
- Version information

### 7. **User Experience**
- Progress indicators
- Clear feedback
- Help documentation
- Input validation with helpful messages

## Example Output

When reviewing `demo.py`, the code reviewer provided these 10 suggestions:

1. **Constants for Magic Numbers** - Replace hardcoded values (10, 800, 70) with named constants
2. **Separate Data Fetching from Display** - Split concerns into pure data fetching and display logic
3. **Type Hints** - Add type annotations using `typing` module (Dict, List, Optional, Tuple)
4. **Specific Error Handling** - Catch specific exceptions (Timeout, ConnectionError, HTTPError) instead of generic Exception
5. **Input Validation** - Add dedicated validation function with clear error messages
6. **Progress Indicators** - Add visual feedback (⏳/✅/❌) with flush for real-time updates
7. **DRY Principle** - Extract repeated "next steps" text into reusable function
8. **Version Information** - Add `__version__` constant for tracking
9. **Better Exception Handling** - Handle KeyboardInterrupt and EOFError separately for better UX
10. **Enhanced Documentation** - Improve docstrings with examples and edge cases

## Integration Example

```python
# File: demo.py (before review)
# Note: search_wikipedia() is the backend Python function that implements
# the wikipedia_search tool exposed to Claude via the tool schema.
def search_wikipedia(query):
    # ... basic implementation
    pass

# After implementing code review suggestions:
from typing import Dict, List, Optional, Tuple

__version__ = "1.0.0"

# Constants
WIKI_TIMEOUT = 10
DEMO_TRUNCATE_LENGTH = 800

def validate_query(query: Optional[str]) -> Tuple[bool, Optional[str]]:
    """Validate user input query."""
    if not query or not query.strip():
        return False, "Query cannot be empty"
    if len(query.strip()) < 2:
        return False, "Query must be at least 2 characters long"
    return True, None

def fetch_wikipedia_search(query: str, num_results: int) -> Tuple[Optional[List[str]], Optional[str]]:
    """Pure data fetching function - returns (titles, error)."""
    try:
        # ... implementation
        return titles, None
    except requests.Timeout:
        return None, "Request timed out"
    except requests.ConnectionError:
        return None, "Connection error"
```

## Best Practices for Using Code Reviewer

1. **Be Specific**: Provide clear context about what aspects to focus on
2. **Include Files**: Make sure the code reviewer has access to the actual file content
3. **Set Priorities**: Indicate if you want security, performance, or readability focus
4. **Iterate**: Apply suggestions incrementally and re-review if needed
5. **Test Changes**: Verify all suggested improvements work as expected

## Limitations

- Code reviewer provides suggestions but doesn't modify files directly
- Human judgment required to evaluate trade-offs
- May suggest improvements that conflict with project-specific conventions
- Focused on Python; other languages may need different review criteria

## Related Files

- `demo.py` - The file that was reviewed
- `SUBAGENT_PROJECT_MANAGER.md` - Complementary project management subagent
- `README.md` - Overall project documentation

## References

- [PEP 8 - Style Guide for Python Code](https://peps.python.org/pep-0008/)
- [PEP 484 - Type Hints](https://peps.python.org/pep-0484/)
- [Clean Code by Robert C. Martin](https://www.amazon.com/Clean-Code-Handbook-Software-Craftsmanship/dp/0132350882)
