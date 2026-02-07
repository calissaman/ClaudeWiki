#!/usr/bin/env python3
"""
ClaudeWiki Demo Mode
====================
Demonstrates Wikipedia search functionality without requiring an Anthropic API key.

This script shows:
- How Wikipedia searches are performed
- What data is retrieved from articles
- How results are formatted
- Sample queries across different topics

Usage:
    python3 demo.py              # Full demo with multiple examples
    python3 demo.py --quick      # Quick test with single example
    python3 demo.py --query "Mars planet"   # Custom search query
"""

__version__ = "1.0.0"

import requests
import json
import sys
import argparse
from typing import Dict, List, Optional, Tuple

# Constants
WIKI_BASE_URL = "https://en.wikipedia.org/w/api.php"
WIKI_TIMEOUT = 10  # seconds
WIKI_USER_AGENT = "ClaudeWiki-Demo/1.0 (Educational demonstration tool)"
DEFAULT_SEARCH_RESULTS = 3
MAX_ARTICLES_TO_FETCH = 2
DEMO_TRUNCATE_LENGTH = 800
SEPARATOR_WIDTH = 70
WIKI_PAGE_NOT_FOUND = "-1"  # Wikipedia's indicator for page not found


def fetch_wikipedia_search(query: str, num_results: int = DEFAULT_SEARCH_RESULTS) -> Tuple[Optional[List[str]], Optional[str]]:
    """
    Search Wikipedia for articles matching the query.

    Args:
        query: Search term
        num_results: Number of results to retrieve

    Returns:
        Tuple of (list of article titles, error message)
        - On success: (["Title1", "Title2", ...], None)
        - On failure: (None, "Error message")
    """
    headers = {"User-Agent": WIKI_USER_AGENT}

    search_params = {
        "action": "query",
        "list": "search",
        "srsearch": query,
        "format": "json",
        "utf8": 1,
        "srlimit": num_results
    }

    try:
        response = requests.get(
            WIKI_BASE_URL,
            params=search_params,
            headers=headers,
            timeout=WIKI_TIMEOUT
        )
        response.raise_for_status()
        data = response.json()
    except requests.Timeout:
        return None, "Request timed out. Please check your internet connection."
    except requests.ConnectionError:
        return None, "Could not connect to Wikipedia. Please check your internet connection."
    except requests.HTTPError as e:
        return None, f"HTTP error occurred: {e}"
    except requests.RequestException as e:
        return None, f"Network error: {e}"
    except ValueError:
        return None, "Invalid JSON response from Wikipedia API."

    # Validate response structure
    if not isinstance(data, dict) or "query" not in data:
        return None, "Unexpected response format from Wikipedia API."

    results = data.get("query", {}).get("search", [])

    if not results:
        return None, f"No Wikipedia articles found for '{query}'"

    titles = [r["title"] for r in results if "title" in r]
    return titles, None


def fetch_wikipedia_content(titles: List[str]) -> Tuple[Optional[Dict], Optional[str]]:
    """
    Fetch content for the specified Wikipedia articles.

    Args:
        titles: List of article titles to fetch

    Returns:
        Tuple of (dict of page content, error message)
        - On success: ({"Title": "content", ...}, None)
        - On failure: (None, "Error message")
    """
    headers = {"User-Agent": WIKI_USER_AGENT}

    # Limit to MAX_ARTICLES_TO_FETCH
    titles_to_fetch = titles[:MAX_ARTICLES_TO_FETCH]

    content_params = {
        "action": "query",
        "prop": "extracts",
        "exintro": 0,
        "explaintext": 1,
        "exsectionformat": "plain",
        "titles": "|".join(titles_to_fetch),
        "format": "json",
        "exlimit": MAX_ARTICLES_TO_FETCH
    }

    try:
        response = requests.get(
            WIKI_BASE_URL,
            params=content_params,
            headers=headers,
            timeout=WIKI_TIMEOUT
        )
        response.raise_for_status()
        data = response.json()
    except requests.Timeout:
        return None, "Request timed out while fetching content."
    except requests.ConnectionError:
        return None, "Connection error while fetching content."
    except requests.HTTPError as e:
        return None, f"HTTP error: {e}"
    except requests.RequestException as e:
        return None, f"Network error: {e}"
    except ValueError:
        return None, "Invalid JSON response from Wikipedia API."

    # Validate response structure
    if not isinstance(data, dict) or "query" not in data:
        return None, "Unexpected response format from Wikipedia API."

    pages = data.get("query", {}).get("pages", {})

    # Extract content
    content_dict = {}
    for page_id, page in pages.items():
        if page_id == WIKI_PAGE_NOT_FOUND:
            continue

        title = page.get("title", "Unknown")
        extract = page.get("extract", "No content available")
        content_dict[title] = extract

    if not content_dict:
        return None, "Could not retrieve content for the specified articles."

    return content_dict, None


def format_search_results(titles: List[str], content: Dict[str, str], truncate: bool = True) -> str:
    """
    Format search results for display.

    Args:
        titles: List of article titles found
        content: Dict mapping titles to content
        truncate: Whether to truncate long content for demo

    Returns:
        Formatted string ready for display
    """
    output_parts = []

    for title, text in content.items():
        if truncate and len(text) > DEMO_TRUNCATE_LENGTH:
            text = text[:DEMO_TRUNCATE_LENGTH] + "...\n[Content truncated for demo]"

        output_parts.append(f"\n## {title}\n\n{text}")

    separator = "\n\n" + ("─" * SEPARATOR_WIDTH) + "\n"
    return separator.join(output_parts)


def display_search_progress(query: str, show_progress: bool = True):
    """Display search progress to user."""
    print(f"\n{'='*SEPARATOR_WIDTH}")
    print(f"🔍 Searching Wikipedia for: '{query}'")
    print('='*SEPARATOR_WIDTH)

    if show_progress:
        print("⏳ Searching...", end="", flush=True)


def display_search_results_summary(titles: List[str]):
    """Display summary of search results."""
    print(f"\r✅ Search complete!{' '*20}")  # Clear the loading message
    print(f"\n📚 Found {len(titles)} article(s):")
    for i, title in enumerate(titles, 1):
        print(f"   {i}. {title}")


def display_fetch_progress(num_articles: int):
    """Display content fetch progress."""
    print(f"\n📖 Retrieving content from top {num_articles} article(s)...")
    print("⏳ Fetching...", end="", flush=True)


def search_wikipedia(query: str, num_results: int = DEFAULT_SEARCH_RESULTS, verbose: bool = True) -> str:
    """
    Search Wikipedia and return formatted results.

    Args:
        query: Search term
        num_results: Number of search results to retrieve
        verbose: Whether to show progress and details

    Returns:
        Formatted string containing search results and article content,
        or error message starting with "❌" on failure.

    Side Effects:
        Prints search progress and results to stdout if verbose=True.
    """
    if verbose:
        display_search_progress(query)

    # Step 1: Search for articles
    titles, error = fetch_wikipedia_search(query, num_results)

    if error:
        if verbose:
            print(f"\r❌ Search failed{' '*20}")
        return f"❌ {error}"

    if verbose:
        display_search_results_summary(titles)
        display_fetch_progress(min(MAX_ARTICLES_TO_FETCH, len(titles)))

    # Step 2: Fetch content
    content, error = fetch_wikipedia_content(titles)

    if error:
        if verbose:
            print(f"\r❌ Fetch failed{' '*20}")
        return f"❌ {error}"

    if verbose:
        print(f"\r✅ Content retrieved!{' '*20}")

    # Step 3: Format results
    return format_search_results(titles, content)


def print_next_steps():
    """Print instructions for running the full ClaudeWiki tool."""
    print("\n🚀 Ready to try the full ClaudeWiki tool?")
    print("   1. Set your Anthropic API key:")
    print("      export ANTHROPIC_API_KEY='sk-ant-api03-...'")
    print("   2. Run: python3 app.py")
    print("   3. Open: http://localhost:5000")
    print("\n📚 See README.md for full installation instructions.\n")


def run_demo_examples():
    """Run through several example queries to demonstrate functionality."""
    print(f"\n{'='*SEPARATOR_WIDTH}")
    print("ClaudeWiki - Demo Mode")
    print('='*SEPARATOR_WIDTH)
    print("\nThis demo shows how Wikipedia searches work in ClaudeWiki.")
    print("No Anthropic API key required!\n")
    print("The demo will run through several example queries...")

    examples = [
        {
            "query": "Marie Curie",
            "description": "Biographical query - person"
        },
        {
            "query": "Python programming",
            "description": "Technical topic with disambiguation"
        },
        {
            "query": "World War 2 end date",
            "description": "Historical fact - specific date"
        },
        {
            "query": "Tokyo Tower height",
            "description": "Numerical fact query"
        }
    ]

    for i, example in enumerate(examples, 1):
        print(f"\n\n{'#'*SEPARATOR_WIDTH}")
        print(f"Example {i}/{len(examples)}: {example['description']}")
        print('#'*SEPARATOR_WIDTH)

        result = search_wikipedia(example["query"])
        print(result)

        if i < len(examples):
            try:
                input("\n⏎ Press Enter to continue to next example...")
            except (KeyboardInterrupt, EOFError):
                print("\n\n⚠️  Demo interrupted by user.")
                return

    print(f"\n\n{'='*SEPARATOR_WIDTH}")
    print("Demo Complete!")
    print('='*SEPARATOR_WIDTH)
    print("\n✨ This was just the Wikipedia search functionality.")
    print("   The full ClaudeWiki tool adds:")
    print("   • AI-powered question understanding")
    print("   • Multi-article synthesis")
    print("   • Inline citations and formatting")
    print("   • Conversational follow-ups")
    print("   • Safety guardrails")

    print_next_steps()


def run_quick_test():
    """Run a single quick test to verify Wikipedia API connection."""
    print(f"\n{'='*SEPARATOR_WIDTH}")
    print("ClaudeWiki - Quick Test")
    print('='*SEPARATOR_WIDTH)
    print("\nTesting Wikipedia API connection...\n")

    result = search_wikipedia("Albert Einstein", num_results=1)
    print(result)

    print(f"\n\n{'='*SEPARATOR_WIDTH}")
    print("✅ Quick Test Complete!")
    print('='*SEPARATOR_WIDTH)
    print("\n✨ Wikipedia API is working correctly!")
    print("\n🚀 Want to see more examples?")
    print("   Run: python3 demo.py")

    print_next_steps()


def validate_query(query: Optional[str]) -> Tuple[bool, Optional[str]]:
    """
    Validate user query input.

    Args:
        query: Query string to validate

    Returns:
        Tuple of (is_valid, error_message)
    """
    if query is None:
        return False, "Query cannot be None"

    if not query.strip():
        return False, "Query cannot be empty"

    if len(query.strip()) < 2:
        return False, "Query must be at least 2 characters long"

    return True, None


def main():
    """
    Main entry point for demo script.

    Handles command-line arguments and routes to appropriate demo mode.
    """
    parser = argparse.ArgumentParser(
        description=f"ClaudeWiki Demo v{__version__} - Wikipedia search without API key",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 demo.py              Run full demo with multiple examples
  python3 demo.py --quick      Quick test with single example
  python3 demo.py --query "Mars planet"   Custom search query

Note: This demo shows only Wikipedia search functionality.
      For the full AI-powered experience, see README.md
        """
    )

    parser.add_argument(
        "--quick",
        action="store_true",
        help="Run quick test with single example"
    )

    parser.add_argument(
        "--query",
        type=str,
        help="Custom search query"
    )

    parser.add_argument(
        "--version",
        action="version",
        version=f"ClaudeWiki Demo v{__version__}"
    )

    args = parser.parse_args()

    try:
        if args.query:
            # Validate custom query
            is_valid, error = validate_query(args.query)
            if not is_valid:
                print(f"❌ Error: {error}")
                sys.exit(1)

            # Custom query
            print(f"\n{'='*SEPARATOR_WIDTH}")
            print("ClaudeWiki - Custom Query Demo")
            print('='*SEPARATOR_WIDTH)
            result = search_wikipedia(args.query.strip())
            print(result)
            print()

        elif args.quick:
            # Quick test
            run_quick_test()
        else:
            # Full demo
            run_demo_examples()

    except KeyboardInterrupt:
        print("\n\n⚠️  Demo interrupted by user.")
        print("Thank you for trying ClaudeWiki demo!\n")
        sys.exit(0)
    except requests.RequestException as e:
        print(f"\n❌ Network error: {e}")
        print("Please check your internet connection and try again.\n")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        print("Please report this issue if it persists.\n")
        sys.exit(1)


if __name__ == "__main__":
    main()
