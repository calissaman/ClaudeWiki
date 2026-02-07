#!/usr/bin/env python3
"""
Evaluation Test Runner for ClaudeWiki
Runs test cases from eval_suite.py against the live server.
"""

import requests
import json
import time
import sys
from collections import defaultdict
from eval_suite import TEST_CASES, DIMENSIONS

SERVER_URL = "http://localhost:5000/api/chat"
TIMEOUT = 60  # seconds per request


def run_test_case(test_case, verbose=False):
    """
    Run a single test case against the server.

    Returns:
        dict: Result with status, response, and timing
    """
    if verbose:
        print(f"\n{'='*80}")
        print(f"Test Case: {test_case['id']}")
        print(f"Dimension: D{test_case['dimension']} - {test_case['dimension_name']}")
        print(f"Question Type: Q{test_case['question_type']} - {test_case['question_type_name']}")
        print(f"{'='*80}")
        print(f"\nPrompt: {test_case['prompt']}")
        print(f"\n⏳ Sending request to server...")

    start_time = time.time()

    try:
        response = requests.post(
            SERVER_URL,
            json={"message": test_case['prompt']},
            timeout=TIMEOUT,
            stream=True
        )
        elapsed = time.time() - start_time

        if response.status_code == 200:
            # Parse SSE stream
            answer_parts = []
            for line in response.iter_lines():
                if line:
                    line_str = line.decode('utf-8')
                    if line_str.startswith('data: '):
                        try:
                            data = json.loads(line_str[6:])  # Skip "data: "
                            # Collect both delta and content types
                            if data.get('type') in ['delta', 'content']:
                                answer_parts.append(data.get('content', ''))
                        except json.JSONDecodeError:
                            pass

            answer = ''.join(answer_parts)
            elapsed = time.time() - start_time

            if verbose:
                print(f"✅ Response received ({elapsed:.1f}s)")
                print(f"\n{'─'*80}")
                print("RESPONSE:")
                print('─'*80)
                print(answer[:500] + "..." if len(answer) > 500 else answer)
                print('─'*80)

            return {
                'status': 'success',
                'response': answer,
                'elapsed': elapsed,
                'test_case': test_case
            }
        else:
            if verbose:
                print(f"❌ HTTP Error: {response.status_code}")
                print(f"Response: {response.text[:200]}")
            return {
                'status': 'error',
                'error': f"HTTP {response.status_code}: {response.text[:100]}",
                'elapsed': elapsed,
                'test_case': test_case
            }

    except requests.Timeout:
        if verbose:
            print(f"⏱️  Timeout after {TIMEOUT}s")
        return {
            'status': 'timeout',
            'elapsed': TIMEOUT,
            'test_case': test_case
        }
    except Exception as e:
        if verbose:
            print(f"❌ Error: {e}")
        return {
            'status': 'error',
            'error': str(e),
            'elapsed': time.time() - start_time,
            'test_case': test_case
        }


def run_sample_tests(samples_per_dimension=2, verbose=True):
    """
    Run a sample of test cases from each dimension.
    """
    print("="*80)
    print("CLAUDEWIKI EVALUATION TEST RUNNER")
    print("="*80)
    print(f"\nRunning {samples_per_dimension} test case(s) per dimension...")
    print(f"Total tests to run: {7 * samples_per_dimension}")
    print(f"Server: {SERVER_URL}")
    print("\n")

    results = []

    # Group test cases by dimension
    by_dimension = defaultdict(list)
    for tc in TEST_CASES:
        by_dimension[tc['dimension']].append(tc)

    # Run samples from each dimension
    for dim_id in sorted(by_dimension.keys()):
        dim_name = [d['name'] for d in DIMENSIONS if d['id'] == dim_id][0]
        cases = by_dimension[dim_id][:samples_per_dimension]

        print(f"\n{'#'*80}")
        print(f"DIMENSION {dim_id}: {dim_name}")
        print(f"{'#'*80}")

        for tc in cases:
            result = run_test_case(tc, verbose=verbose)
            results.append(result)

            # Small delay between tests
            if tc != cases[-1]:
                time.sleep(1)

    return results


def print_summary(results):
    """Print summary of test results."""
    print("\n\n" + "="*80)
    print("EVALUATION SUMMARY")
    print("="*80)

    total = len(results)
    success = sum(1 for r in results if r['status'] == 'success')
    errors = sum(1 for r in results if r['status'] == 'error')
    timeouts = sum(1 for r in results if r['status'] == 'timeout')

    avg_time = sum(r['elapsed'] for r in results if r['status'] == 'success') / max(success, 1)

    print(f"\nTotal tests run: {total}")
    print(f"✅ Successful: {success} ({success/total*100:.1f}%)")
    print(f"❌ Errors: {errors} ({errors/total*100:.1f}%)")
    print(f"⏱️  Timeouts: {timeouts} ({timeouts/total*100:.1f}%)")
    print(f"\n⏱️  Average response time: {avg_time:.1f}s")

    # By dimension
    by_dim = defaultdict(lambda: {'success': 0, 'error': 0, 'timeout': 0})
    for r in results:
        dim = r['test_case']['dimension']
        by_dim[dim][r['status']] += 1

    print("\n" + "="*80)
    print("RESULTS BY DIMENSION")
    print("="*80)
    for dim_id in sorted(by_dim.keys()):
        dim_name = [d['name'] for d in DIMENSIONS if d['id'] == dim_id][0]
        stats = by_dim[dim_id]
        total_dim = sum(stats.values())
        success_rate = stats['success'] / total_dim * 100 if total_dim > 0 else 0
        print(f"D{dim_id}: {dim_name:50} {stats['success']}/{total_dim} ({success_rate:.0f}%)")

    # Language distribution for D7
    d7_results = [r for r in results if r['test_case']['dimension'] == 7]
    if d7_results:
        print("\n" + "="*80)
        print("MULTILINGUAL TESTS (Dimension 7)")
        print("="*80)
        for r in d7_results:
            tc = r['test_case']
            status_icon = "✅" if r['status'] == 'success' else "❌"
            prompt_preview = tc['prompt'] if len(tc['prompt']) <= 40 else tc['prompt'][:37] + "..."
            print(f"{status_icon} {tc['id']}: {prompt_preview}")


def main():
    """Main entry point."""
    import argparse

    parser = argparse.ArgumentParser(description="Run ClaudeWiki evaluation tests")
    parser.add_argument('--samples', type=int, default=1,
                       help='Number of samples per dimension (default: 1)')
    parser.add_argument('--quiet', action='store_true',
                       help='Minimal output')
    parser.add_argument('--url', type=str, default="http://localhost:5000/api/chat",
                       help='Server URL')

    args = parser.parse_args()

    server_url = args.url

    try:
        # Check if server is running
        print("Checking server connection...")
        response = requests.get(server_url.replace('/api/chat', ''), timeout=5)
        if response.status_code != 200:
            print(f"❌ Server returned status {response.status_code}")
            sys.exit(1)
        print("✅ Server is running\n")

    except Exception as e:
        print(f"❌ Could not connect to server at {server_url}")
        print(f"   Error: {e}")
        print("\nPlease start the server first:")
        print("   python3 app.py")
        sys.exit(1)

    # Run tests (pass server_url if needed, or update SERVER_URL constant)
    # For now, using the module-level constant
    results = run_sample_tests(
        samples_per_dimension=args.samples,
        verbose=not args.quiet
    )

    # Print summary
    print_summary(results)

    print("\n" + "="*80)
    print("Evaluation complete!")
    print("="*80 + "\n")


if __name__ == "__main__":
    main()
