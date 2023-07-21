import time
import requests
import statistics
import concurrent.futures

NUM_REQUESTS = 20
NUM_THREADS = 10  # Number of threads to use for concurrent requests

BACKEND_URL = "http://localhost"  # The Nginx load balancer URL
LOAD_TEST_DURATION = 30  # Load test duration in seconds

def make_requests():
    response_times = []
    for _ in range(NUM_REQUESTS):
        start_time = time.time()
        response = requests.get(BACKEND_URL)
        end_time = time.time()
        response_times.append(end_time - start_time)
    return response_times

def calculate_summary_statistics(response_times):
    if not response_times:
        return 0, 0, 0, 0  # Return default values if response_times is empty
    min_time = min(response_times)
    max_time = max(response_times)
    avg_time = statistics.mean(response_times)
    stdev_time = statistics.stdev(response_times)
    return min_time, max_time, avg_time, stdev_time

def run_load_testing():
    print("Testing the approach of dynamically scaling service replicas with environment variables...\n")

    print(f"Testing backend: {BACKEND_URL} using {NUM_THREADS} threads and {NUM_REQUESTS} requests per thread...\n")

    start_time = time.time()

    all_response_times = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=NUM_THREADS) as executor:
        futures = [executor.submit(make_requests) for _ in range(NUM_THREADS)]
        for future in concurrent.futures.as_completed(futures):
            try:
                response_times = future.result()
                all_response_times.extend(response_times)
            except Exception as exc:
                print(f"Thread raised an exception: {exc}")

    end_time = time.time()
    total_time = end_time - start_time

    print(f"All threads completed in {total_time:.2f} seconds.\n")

    # Calculate and display summary statistics
    min_time, max_time, avg_time, stdev_time = calculate_summary_statistics(all_response_times)
    print(f"Minimum Response Time: {min_time:.4f} seconds")
    print(f"Maximum Response Time: {max_time:.4f} seconds")
    print(f"Average Response Time: {avg_time:.4f} seconds")
    print(f"Standard Deviation of Response Time: {stdev_time:.4f} seconds")

    # Calculate and display Requests Per Second (RPS)
    total_requests = NUM_REQUESTS * NUM_THREADS
    rps = total_requests / total_time
    print(f"Requests Per Second (RPS): {rps:.2f}")

if __name__ == "__main__":
    run_load_testing()
