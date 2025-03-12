import api_config
import request_sender
from concurrent.futures import ThreadPoolExecutor
import html
import os


def generate_html_report(results, output_file):
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('<html><head><title>API Stress Test Report</title></head><body>\n')
        f.write('<h1>API Stress Test Report</h1>\n')
        f.write('<table border="1">\n')
        f.write('<tr><th>API Name</th><th>Success</th><th>Response Time (s)</th><th>Response Content</th></tr>\n')
        for result in results:
            success_str = 'Yes' if result['success'] else 'No'
            response_content = html.escape(result['response_content'] or 'N/A')
            f.write(
                f'<tr><td>{result["api_name"]}</td><td>{success_str}</td><td>{result["response_time"]:.4f}</td><td>{response_content}</td></tr>\n')
        f.write('</table>\n')
        f.write('</body></html>\n')


def stress_test(api_name=None, concurrency=5, iterations=10):
    results = []
    api_requests_to_test = [req for req in api_config.api_requests if api_name is None or req['name'] == api_name]

    with ThreadPoolExecutor(max_workers=concurrency) as executor:
        future_to_request = {executor.submit(run_test, req, iterations): req for req in api_requests_to_test}
        for future in future_to_request:
            req = future_to_request[future]
            try:
                test_results = future.result()
                results.extend(test_results)
            except Exception as exc:
                print(f"{req['name']} generated an exception: {exc}")

    output_file = 'stress_test_report.html'
    generate_html_report(results, output_file)
    print(f"Test report generated: {output_file}")


def run_test(request, iterations):
    api_name = request['name']
    results = []
    for _ in range(iterations):
        success, response_time, response_content = request_sender.send_request(
            request['url'],
            request['headers'],
            api_name,
            method=request.get('method', 'POST'),
            params=request.get('params'),
            data=request.get('data'),
            files=request.get('files')
        )
        results.append({
            'api_name': api_name,
            'success': success,
            'response_time': response_time,
            'response_content': response_content
        })
    return results


if __name__ == "__main__":
    # Example usage: Run stress test for all APIs with 5 concurrent threads and 10 iterations each
    # stress_test(concurrency=5, iterations=10)
    # Example usage: Run stress test for a specific API by name
    stress_test(api_name="OpenAI-chat", concurrency=1, iterations=1)