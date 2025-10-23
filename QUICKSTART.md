# Quick Start Guide

## Installation

```bash
# Clone the repository
git clone https://github.com/abscalibur/WebBasedScriptOrCommandSchedular.git
cd WebBasedScriptOrCommandSchedular

# Set up Python virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## Running the Scheduler

### Option 1: Web Interface (Recommended)

Start the web application:

```bash
python app.py
```

Then open your browser to: **http://localhost:5000**

### Option 2: Python API

Use the scheduler programmatically:

```python
from datetime import datetime, timedelta
from scheduler import Scheduler

# Create and start scheduler
scheduler = Scheduler()
scheduler.start()

# Add a job
scheduler.add_job(
    job_id="my-job",
    command="echo 'Hello World'",
    start_time=datetime.now(),
    interval_seconds=60  # Run every 60 seconds
)

# Get results
results = scheduler.get_job_results("my-job")
for result in results:
    print(f"Output: {result.stdout}")
```

### Option 3: REST API

With the web app running, use curl or any HTTP client:

```bash
# Add a job
curl -X POST http://localhost:5000/api/jobs \
  -H "Content-Type: application/json" \
  -d '{
    "job_id": "backup-job",
    "command": "tar -czf backup.tar.gz /data",
    "start_time": "2024-01-01T02:00:00",
    "interval_seconds": 3600
  }'

# List all jobs
curl http://localhost:5000/api/jobs

# Get job results
curl http://localhost:5000/api/jobs/backup-job/results

# Delete a job
curl -X DELETE http://localhost:5000/api/jobs/backup-job
```

## Try the Demo

Run the included demo to see the scheduler in action:

```bash
python demo.py
```

This will:
- Create several example jobs
- Show command execution in real-time
- Demonstrate success and failure handling
- Display captured stdout/stderr

## Common Use Cases

### 1. Periodic Backups
```python
scheduler.add_job(
    job_id="daily-backup",
    command="backup.sh",
    start_time=datetime.now() + timedelta(hours=1),
    interval_seconds=86400  # 24 hours
)
```

### 2. System Monitoring
```python
scheduler.add_job(
    job_id="disk-check",
    command="df -h",
    start_time=datetime.now(),
    interval_seconds=300  # 5 minutes
)
```

### 3. Log Rotation
```python
scheduler.add_job(
    job_id="log-rotate",
    command="logrotate /etc/logrotate.conf",
    start_time=datetime.now(),
    interval_seconds=3600  # 1 hour
)
```

### 4. Health Checks
```python
scheduler.add_job(
    job_id="health-check",
    command="curl https://myapi.com/health",
    start_time=datetime.now(),
    interval_seconds=30  # 30 seconds
)
```

## Web Interface Features

- ✅ Add new scheduled jobs with a simple form
- ✅ View all active jobs and their status
- ✅ See last execution results (stdout/stderr)
- ✅ View complete execution history
- ✅ Delete jobs
- ✅ Auto-refresh every 5 seconds
- ✅ Color-coded success/failure indicators

## API Reference

### GET /api/jobs
List all scheduled jobs

**Response:**
```json
[
  {
    "job_id": "example",
    "command": "echo test",
    "interval_seconds": 60,
    "next_run_time": "2024-01-01T10:05:00",
    "total_runs": 5,
    "last_result": {
      "stdout": "test\n",
      "stderr": "",
      "return_code": 0,
      "success": true
    }
  }
]
```

### POST /api/jobs
Create a new scheduled job

**Request:**
```json
{
  "job_id": "unique-id",
  "command": "echo 'Hello'",
  "start_time": "2024-01-01T10:00:00",
  "interval_seconds": 60
}
```

### GET /api/jobs/{job_id}
Get details of a specific job

### DELETE /api/jobs/{job_id}
Remove a scheduled job

### GET /api/jobs/{job_id}/results
Get all execution results for a job

## Tips

- Jobs execute in separate threads to prevent blocking
- Each command has a 5-minute timeout
- Results are stored in memory (lost on restart)
- Use the web interface for easy monitoring
- Check stderr for error messages
- Return code 0 indicates success

## Troubleshooting

**Job not executing?**
- Check that the start_time is in the future or current
- Verify the command is valid on your system
- Check stderr in the results for errors

**Web interface not loading?**
- Ensure Flask is running: `python app.py`
- Check port 5000 is not in use
- Try accessing http://127.0.0.1:5000

**Command fails with timeout?**
- Commands have a 5-minute limit
- Break long tasks into smaller jobs
- Use background processes for very long tasks

## Next Steps

1. Start with the demo: `python demo.py`
2. Try the web interface: `python app.py`
3. Create your first scheduled job
4. Check the execution results
5. Explore the API examples: `api_examples.py`

For more details, see the full [README.md](README.md)
