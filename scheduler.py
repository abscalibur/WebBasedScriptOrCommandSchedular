"""
Scheduler module for running terminal commands at scheduled intervals
"""
import subprocess
import threading
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import json
import os


class JobResult:
    """Represents the result of a job execution"""
    
    def __init__(self, job_id: str, command: str, start_time: datetime):
        self.job_id = job_id
        self.command = command
        self.start_time = start_time
        self.end_time: Optional[datetime] = None
        self.stdout: str = ""
        self.stderr: str = ""
        self.return_code: Optional[int] = None
        self.success: bool = False
    
    def to_dict(self) -> dict:
        """Convert result to dictionary"""
        return {
            'job_id': self.job_id,
            'command': self.command,
            'start_time': self.start_time.isoformat() if self.start_time else None,
            'end_time': self.end_time.isoformat() if self.end_time else None,
            'stdout': self.stdout,
            'stderr': self.stderr,
            'return_code': self.return_code,
            'success': self.success
        }


class ScheduledJob:
    """Represents a scheduled job"""
    
    def __init__(self, job_id: str, command: str, start_time: datetime, interval_seconds: int):
        self.job_id = job_id
        self.command = command
        self.start_time = start_time
        self.interval_seconds = interval_seconds
        self.next_run_time = start_time
        self.enabled = True
        self.results: List[JobResult] = []
    
    def execute(self) -> JobResult:
        """Execute the job and capture output"""
        result = JobResult(self.job_id, self.command, datetime.now())
        
        try:
            # Run the command and capture output
            process = subprocess.run(
                self.command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=300  # 5 minute timeout
            )
            
            result.stdout = process.stdout
            result.stderr = process.stderr
            result.return_code = process.returncode
            result.success = (process.returncode == 0)
            result.end_time = datetime.now()
            
        except subprocess.TimeoutExpired as e:
            result.stderr = f"Command timed out after 300 seconds"
            result.return_code = -1
            result.success = False
            result.end_time = datetime.now()
        except Exception as e:
            result.stderr = f"Error executing command: {str(e)}"
            result.return_code = -1
            result.success = False
            result.end_time = datetime.now()
        
        # Store the result
        self.results.append(result)
        
        # Calculate next run time
        self.next_run_time = datetime.now() + timedelta(seconds=self.interval_seconds)
        
        return result
    
    def to_dict(self) -> dict:
        """Convert job to dictionary"""
        return {
            'job_id': self.job_id,
            'command': self.command,
            'start_time': self.start_time.isoformat(),
            'interval_seconds': self.interval_seconds,
            'next_run_time': self.next_run_time.isoformat(),
            'enabled': self.enabled,
            'total_runs': len(self.results),
            'last_result': self.results[-1].to_dict() if self.results else None
        }


class Scheduler:
    """Simple scheduler for running terminal commands"""
    
    def __init__(self):
        self.jobs: Dict[str, ScheduledJob] = {}
        self.running = False
        self.scheduler_thread: Optional[threading.Thread] = None
        self.lock = threading.Lock()
    
    def add_job(self, job_id: str, command: str, start_time: datetime, interval_seconds: int) -> ScheduledJob:
        """Add a new scheduled job"""
        with self.lock:
            job = ScheduledJob(job_id, command, start_time, interval_seconds)
            self.jobs[job_id] = job
            return job
    
    def remove_job(self, job_id: str) -> bool:
        """Remove a scheduled job"""
        with self.lock:
            if job_id in self.jobs:
                del self.jobs[job_id]
                return True
            return False
    
    def get_job(self, job_id: str) -> Optional[ScheduledJob]:
        """Get a scheduled job by ID"""
        return self.jobs.get(job_id)
    
    def get_all_jobs(self) -> List[ScheduledJob]:
        """Get all scheduled jobs"""
        return list(self.jobs.values())
    
    def get_job_results(self, job_id: str) -> List[JobResult]:
        """Get all results for a job"""
        job = self.get_job(job_id)
        return job.results if job else []
    
    def _scheduler_loop(self):
        """Main scheduler loop"""
        while self.running:
            now = datetime.now()
            
            with self.lock:
                for job in self.jobs.values():
                    if job.enabled and job.next_run_time <= now:
                        # Execute job in a separate thread to avoid blocking
                        threading.Thread(target=job.execute, daemon=True).start()
            
            # Sleep for a short interval before checking again
            time.sleep(1)
    
    def start(self):
        """Start the scheduler"""
        if not self.running:
            self.running = True
            self.scheduler_thread = threading.Thread(target=self._scheduler_loop, daemon=True)
            self.scheduler_thread.start()
    
    def stop(self):
        """Stop the scheduler"""
        self.running = False
        if self.scheduler_thread:
            self.scheduler_thread.join(timeout=5)
