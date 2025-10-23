# WebBasedScriptOrCommandSchedular

A simple web-based scheduler for running terminal commands at scheduled intervals with stdout/stderr capture.

## Features

- ✅ Schedule terminal commands to run at specific times
- ✅ Configure job intervals (how often to repeat)
- ✅ Capture and display stdout/stderr for each command execution
- ✅ Web-based UI for managing scheduled jobs
- ✅ REST API for programmatic access
- ✅ View execution history and results

## Installation

1. Clone the repository:
```bash
git clone https://github.com/abscalibur/WebBasedScriptOrCommandSchedular.git
cd WebBasedScriptOrCommandSchedular
```

2. Create a virtual environment and install dependencies:
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Usage

### Starting the Scheduler

Run the application:
```bash
python app.py
```

The scheduler will start on `http://localhost:5000`

### Web Interface

Open your browser and navigate to `http://localhost:5000` to access the web interface.

#### Adding a Scheduled Job

1. Fill in the form with:
   - **Job ID**: Unique identifier for the job
   - **Command**: Terminal command to execute (e.g., `echo "Hello World"`, `ls -la`, `python script.py`)
   - **Start Time**: When to first run the command
   - **Interval**: How often to repeat (in seconds)

2. Click "Add Job"

#### Managing Jobs

- View all scheduled jobs and their status
- See the last execution result (stdout/stderr)
- View complete execution history
- Delete jobs

### API Endpoints

#### List All Jobs
```bash
GET /api/jobs
```

#### Add a New Job
```bash
POST /api/jobs
Content-Type: application/json

{
    "job_id": "my-job",
    "command": "echo 'Hello'",
    "start_time": "2024-01-01T10:00:00",
    "interval_seconds": 60
}
```

#### Get Job Details
```bash
GET /api/jobs/{job_id}
```

#### Delete a Job
```bash
DELETE /api/jobs/{job_id}
```

#### Get Job Results
```bash
GET /api/jobs/{job_id}/results
```

## Examples

### Example 1: Simple Echo Command
- **Command**: `echo "Current time: $(date)"`
- **Interval**: 30 seconds
- This will print the current time every 30 seconds

### Example 2: Directory Listing
- **Command**: `ls -la /tmp`
- **Interval**: 60 seconds
- Lists files in /tmp directory every minute

### Example 3: Python Script
- **Command**: `python3 /path/to/script.py`
- **Interval**: 300 seconds (5 minutes)
- Runs a Python script every 5 minutes

### Example 4: System Monitoring
- **Command**: `df -h`
- **Interval**: 3600 seconds (1 hour)
- Checks disk usage every hour

## Architecture

- **scheduler.py**: Core scheduling engine
  - `Scheduler`: Main scheduler class that manages jobs
  - `ScheduledJob`: Represents a scheduled job with execution logic
  - `JobResult`: Stores execution results (stdout, stderr, return code)

- **app.py**: Flask web application
  - Web UI for job management
  - REST API endpoints
  - Auto-refresh functionality

## Technical Details

- Jobs are executed in separate threads to prevent blocking
- Command timeout: 5 minutes per execution
- Results are stored in memory (cleared on restart)
- Scheduler checks for jobs to run every second
- Web interface auto-refreshes every 5 seconds

## License

MIT License