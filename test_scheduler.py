"""
Test script for the scheduler
"""
import sys
import time
from datetime import datetime, timedelta
from scheduler import Scheduler

def test_scheduler():
    """Test basic scheduler functionality"""
    print("Testing scheduler...")
    
    # Create scheduler
    scheduler = Scheduler()
    scheduler.start()
    
    # Add a test job that runs immediately
    start_time = datetime.now()
    job_id = "test-job-1"
    command = "echo 'Hello from test job'"
    interval = 5  # 5 seconds
    
    print(f"\n1. Adding job '{job_id}'...")
    job = scheduler.add_job(job_id, command, start_time, interval)
    print(f"   ✓ Job added: {job.command}")
    print(f"   ✓ Start time: {job.start_time}")
    print(f"   ✓ Interval: {job.interval_seconds} seconds")
    
    # Wait for the job to execute
    print("\n2. Waiting for job to execute...")
    time.sleep(2)
    
    # Check results
    results = scheduler.get_job_results(job_id)
    if results:
        print(f"   ✓ Job executed {len(results)} time(s)")
        result = results[0]
        print(f"   ✓ Return code: {result.return_code}")
        print(f"   ✓ Success: {result.success}")
        print(f"   ✓ Stdout: {result.stdout.strip()}")
    else:
        print("   ✗ No results yet")
    
    # Test with a failing command
    print("\n3. Testing with a failing command...")
    job_id2 = "test-job-2"
    command2 = "false"  # This command always fails
    job2 = scheduler.add_job(job_id2, command2, datetime.now(), 10)
    time.sleep(2)
    
    results2 = scheduler.get_job_results(job_id2)
    if results2:
        result2 = results2[0]
        print(f"   ✓ Job executed")
        print(f"   ✓ Return code: {result2.return_code}")
        print(f"   ✓ Success: {result2.success} (should be False)")
        if not result2.success:
            print("   ✓ Correctly detected failure")
    
    # Test job listing
    print("\n4. Testing job listing...")
    all_jobs = scheduler.get_all_jobs()
    print(f"   ✓ Total jobs: {len(all_jobs)}")
    for job in all_jobs:
        print(f"   - {job.job_id}: {job.command}")
    
    # Test job removal
    print("\n5. Testing job removal...")
    removed = scheduler.remove_job(job_id)
    print(f"   ✓ Removed '{job_id}': {removed}")
    all_jobs = scheduler.get_all_jobs()
    print(f"   ✓ Remaining jobs: {len(all_jobs)}")
    
    # Stop scheduler
    scheduler.stop()
    print("\n✓ All tests passed!")
    return True

if __name__ == '__main__':
    try:
        success = test_scheduler()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"\n✗ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
