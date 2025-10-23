#!/usr/bin/env python3
"""
Demo script to showcase the scheduler capabilities
"""
import time
from datetime import datetime, timedelta
from scheduler import Scheduler

def main():
    print("=" * 70)
    print("Command Scheduler Demo")
    print("=" * 70)
    print()
    
    # Create and start scheduler
    scheduler = Scheduler()
    scheduler.start()
    print("✓ Scheduler started\n")
    
    # Demo 1: Simple echo command
    print("Demo 1: Simple echo command")
    print("-" * 70)
    job1 = scheduler.add_job(
        job_id="demo-echo",
        command="echo 'Current time:' $(date +%T)",
        start_time=datetime.now(),
        interval_seconds=3
    )
    print(f"Added job: {job1.job_id}")
    print(f"Command: {job1.command}")
    print(f"Interval: {job1.interval_seconds} seconds")
    print("Waiting for 3 executions...\n")
    
    time.sleep(10)
    
    results = scheduler.get_job_results("demo-echo")
    print(f"Job executed {len(results)} times:")
    for i, result in enumerate(results, 1):
        print(f"  Run {i}: {result.stdout.strip()}")
    print()
    
    # Demo 2: System info command
    print("Demo 2: System information command")
    print("-" * 70)
    job2 = scheduler.add_job(
        job_id="demo-sysinfo",
        command="uname -a",
        start_time=datetime.now(),
        interval_seconds=5
    )
    print(f"Added job: {job2.job_id}")
    print(f"Command: {job2.command}")
    
    time.sleep(2)
    
    results2 = scheduler.get_job_results("demo-sysinfo")
    if results2:
        print(f"Output:\n  {results2[0].stdout.strip()}")
    print()
    
    # Demo 3: Directory listing with multiple runs
    print("Demo 3: Directory listing (will run twice)")
    print("-" * 70)
    job3 = scheduler.add_job(
        job_id="demo-ls",
        command="ls -la /tmp | head -5",
        start_time=datetime.now(),
        interval_seconds=4
    )
    print(f"Added job: {job3.job_id}")
    print(f"Command: {job3.command}")
    print("Waiting for executions...\n")
    
    time.sleep(9)
    
    results3 = scheduler.get_job_results("demo-ls")
    print(f"Job executed {len(results3)} times")
    if results3:
        print(f"Latest output:\n{results3[-1].stdout}")
    
    # Demo 4: Failing command
    print("Demo 4: Handling command failures")
    print("-" * 70)
    job4 = scheduler.add_job(
        job_id="demo-fail",
        command="ls /nonexistent-directory",
        start_time=datetime.now(),
        interval_seconds=5
    )
    print(f"Added job: {job4.job_id}")
    print(f"Command: {job4.command}")
    
    time.sleep(2)
    
    results4 = scheduler.get_job_results("demo-fail")
    if results4:
        result = results4[0]
        print(f"Status: {'Success' if result.success else 'Failed'}")
        print(f"Return code: {result.return_code}")
        print(f"Stderr: {result.stderr.strip()}")
    print()
    
    # Summary
    print("=" * 70)
    print("Summary")
    print("=" * 70)
    all_jobs = scheduler.get_all_jobs()
    print(f"Total active jobs: {len(all_jobs)}")
    for job in all_jobs:
        print(f"  - {job.job_id}: {len(job.results)} executions")
    print()
    
    # Cleanup
    scheduler.stop()
    print("✓ Scheduler stopped")
    print("\nDemo complete! Visit http://localhost:5000 to see the web interface.")
    print("Run: python app.py")

if __name__ == '__main__':
    main()
