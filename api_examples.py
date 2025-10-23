"""
Example usage of the scheduler via API

This script demonstrates how to programmatically interact with the scheduler
"""
import requests
import json
from datetime import datetime, timedelta

# Base URL of the scheduler API
BASE_URL = "http://localhost:5000/api"

def add_job_example():
    """Example: Add a new scheduled job"""
    
    # Schedule a job to run 1 minute from now, every 30 seconds
    start_time = (datetime.now() + timedelta(minutes=1)).isoformat()
    
    job_data = {
        "job_id": "example-job-1",
        "command": "echo 'Hello from scheduled job'",
        "start_time": start_time,
        "interval_seconds": 30
    }
    
    response = requests.post(f"{BASE_URL}/jobs", json=job_data)
    
    if response.status_code == 201:
        print("✓ Job added successfully!")
        print(json.dumps(response.json(), indent=2))
    else:
        print(f"✗ Error: {response.json()}")

def list_jobs_example():
    """Example: List all scheduled jobs"""
    
    response = requests.get(f"{BASE_URL}/jobs")
    
    if response.status_code == 200:
        jobs = response.json()
        print(f"\nFound {len(jobs)} job(s):")
        for job in jobs:
            print(f"  - {job['job_id']}: {job['command']}")
            print(f"    Next run: {job['next_run_time']}")
            print(f"    Total runs: {job['total_runs']}")
    else:
        print(f"✗ Error: {response.status_code}")

def get_job_results_example(job_id):
    """Example: Get execution results for a job"""
    
    response = requests.get(f"{BASE_URL}/jobs/{job_id}/results")
    
    if response.status_code == 200:
        results = response.json()
        print(f"\nResults for {job_id} ({len(results)} executions):")
        for i, result in enumerate(results, 1):
            print(f"\n  Execution {i}:")
            print(f"    Time: {result['start_time']}")
            print(f"    Success: {result['success']}")
            print(f"    Stdout: {result['stdout']}")
            if result['stderr']:
                print(f"    Stderr: {result['stderr']}")
    else:
        print(f"✗ Error: {response.status_code}")

def delete_job_example(job_id):
    """Example: Delete a scheduled job"""
    
    response = requests.delete(f"{BASE_URL}/jobs/{job_id}")
    
    if response.status_code == 200:
        print(f"✓ Job {job_id} deleted successfully!")
    else:
        print(f"✗ Error: {response.status_code}")

if __name__ == '__main__':
    print("Scheduler API Examples")
    print("=" * 50)
    print("\nMake sure the scheduler is running:")
    print("  python app.py")
    print("\nThen uncomment the examples below to try them:")
    print()
    
    # Uncomment to try the examples:
    # add_job_example()
    # list_jobs_example()
    # get_job_results_example("example-job-1")
    # delete_job_example("example-job-1")
