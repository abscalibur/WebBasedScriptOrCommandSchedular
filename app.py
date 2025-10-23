"""
Web-based interface for the command scheduler
"""
from flask import Flask, request, jsonify, render_template_string
from datetime import datetime
from scheduler import Scheduler
import os

app = Flask(__name__)
scheduler = Scheduler()

# HTML template for the web interface
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Command Scheduler</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f5f5f5;
        }
        h1 {
            color: #333;
        }
        .container {
            background-color: white;
            padding: 20px;
            border-radius: 8px;
            margin-bottom: 20px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        .form-group {
            margin-bottom: 15px;
        }
        label {
            display: block;
            margin-bottom: 5px;
            font-weight: bold;
        }
        input[type="text"], input[type="datetime-local"], input[type="number"] {
            width: 100%;
            padding: 8px;
            border: 1px solid #ddd;
            border-radius: 4px;
            box-sizing: border-box;
        }
        button {
            background-color: #4CAF50;
            color: white;
            padding: 10px 20px;
            border: none;
            border-radius: 4px;
            cursor: pointer;
            font-size: 14px;
        }
        button:hover {
            background-color: #45a049;
        }
        .delete-btn {
            background-color: #f44336;
        }
        .delete-btn:hover {
            background-color: #da190b;
        }
        table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 15px;
        }
        th, td {
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid #ddd;
        }
        th {
            background-color: #4CAF50;
            color: white;
        }
        tr:hover {
            background-color: #f5f5f5;
        }
        .success {
            color: green;
        }
        .error {
            color: red;
        }
        .output {
            background-color: #f9f9f9;
            border: 1px solid #ddd;
            padding: 10px;
            margin-top: 5px;
            border-radius: 4px;
            font-family: monospace;
            white-space: pre-wrap;
            max-height: 200px;
            overflow-y: auto;
        }
        .job-card {
            margin-bottom: 10px;
            padding: 10px;
            border: 1px solid #ddd;
            border-radius: 4px;
        }
    </style>
</head>
<body>
    <h1>🕐 Command Scheduler</h1>
    
    <div class="container">
        <h2>Add New Scheduled Job</h2>
        <form id="addJobForm">
            <div class="form-group">
                <label for="jobId">Job ID:</label>
                <input type="text" id="jobId" name="jobId" required placeholder="e.g., backup-job-1">
            </div>
            <div class="form-group">
                <label for="command">Command:</label>
                <input type="text" id="command" name="command" required placeholder="e.g., echo 'Hello World'">
            </div>
            <div class="form-group">
                <label for="startTime">Start Time:</label>
                <input type="datetime-local" id="startTime" name="startTime" required>
            </div>
            <div class="form-group">
                <label for="interval">Interval (seconds):</label>
                <input type="number" id="interval" name="interval" required min="1" value="60">
            </div>
            <button type="submit">Add Job</button>
        </form>
    </div>
    
    <div class="container">
        <h2>Scheduled Jobs</h2>
        <button onclick="refreshJobs()">Refresh</button>
        <div id="jobsList"></div>
    </div>
    
    <script>
        // Set default start time to current time
        const now = new Date();
        now.setMinutes(now.getMinutes() - now.getTimezoneOffset());
        document.getElementById('startTime').value = now.toISOString().slice(0, 16);
        
        // Add job form submission
        document.getElementById('addJobForm').addEventListener('submit', async (e) => {
            e.preventDefault();
            
            const formData = {
                job_id: document.getElementById('jobId').value,
                command: document.getElementById('command').value,
                start_time: document.getElementById('startTime').value,
                interval_seconds: parseInt(document.getElementById('interval').value)
            };
            
            try {
                const response = await fetch('/api/jobs', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(formData)
                });
                
                const result = await response.json();
                
                if (response.ok) {
                    alert('Job added successfully!');
                    document.getElementById('addJobForm').reset();
                    // Reset start time to current time
                    const now = new Date();
                    now.setMinutes(now.getMinutes() - now.getTimezoneOffset());
                    document.getElementById('startTime').value = now.toISOString().slice(0, 16);
                    refreshJobs();
                } else {
                    alert('Error: ' + result.error);
                }
            } catch (error) {
                alert('Error adding job: ' + error);
            }
        });
        
        // Refresh jobs list
        async function refreshJobs() {
            try {
                const response = await fetch('/api/jobs');
                const jobs = await response.json();
                
                const jobsList = document.getElementById('jobsList');
                
                if (jobs.length === 0) {
                    jobsList.innerHTML = '<p>No scheduled jobs</p>';
                } else {
                    jobsList.innerHTML = jobs.map(job => `
                        <div class="job-card">
                            <h3>${job.job_id}</h3>
                            <p><strong>Command:</strong> ${job.command}</p>
                            <p><strong>Interval:</strong> ${job.interval_seconds} seconds</p>
                            <p><strong>Next Run:</strong> ${new Date(job.next_run_time).toLocaleString()}</p>
                            <p><strong>Total Runs:</strong> ${job.total_runs}</p>
                            ${job.last_result ? `
                                <div>
                                    <strong>Last Run:</strong> ${new Date(job.last_result.start_time).toLocaleString()}
                                    <span class="${job.last_result.success ? 'success' : 'error'}">
                                        ${job.last_result.success ? '✓ Success' : '✗ Failed'}
                                    </span>
                                    ${job.last_result.stdout ? `
                                        <div>
                                            <strong>Stdout:</strong>
                                            <div class="output">${job.last_result.stdout}</div>
                                        </div>
                                    ` : ''}
                                    ${job.last_result.stderr ? `
                                        <div>
                                            <strong>Stderr:</strong>
                                            <div class="output error">${job.last_result.stderr}</div>
                                        </div>
                                    ` : ''}
                                </div>
                            ` : '<p>Not yet executed</p>'}
                            <button onclick="viewJobResults('${job.job_id}')">View All Results</button>
                            <button class="delete-btn" onclick="deleteJob('${job.job_id}')">Delete</button>
                        </div>
                    `).join('');
                }
            } catch (error) {
                console.error('Error fetching jobs:', error);
            }
        }
        
        // Delete job
        async function deleteJob(jobId) {
            if (!confirm('Are you sure you want to delete this job?')) {
                return;
            }
            
            try {
                const response = await fetch('/api/jobs/' + jobId, {
                    method: 'DELETE'
                });
                
                if (response.ok) {
                    alert('Job deleted successfully!');
                    refreshJobs();
                } else {
                    alert('Error deleting job');
                }
            } catch (error) {
                alert('Error: ' + error);
            }
        }
        
        // View job results
        async function viewJobResults(jobId) {
            try {
                const response = await fetch('/api/jobs/' + jobId + '/results');
                const results = await response.json();
                
                if (results.length === 0) {
                    alert('No results yet for this job');
                    return;
                }
                
                let output = `Results for ${jobId}:\n\n`;
                results.forEach((result, index) => {
                    output += `Run ${index + 1} - ${new Date(result.start_time).toLocaleString()}\n`;
                    output += `Status: ${result.success ? 'Success' : 'Failed'} (exit code: ${result.return_code})\n`;
                    if (result.stdout) output += `Stdout: ${result.stdout}\n`;
                    if (result.stderr) output += `Stderr: ${result.stderr}\n`;
                    output += '\n---\n\n';
                });
                
                alert(output);
            } catch (error) {
                alert('Error fetching results: ' + error);
            }
        }
        
        // Initial load
        refreshJobs();
        
        // Auto-refresh every 5 seconds
        setInterval(refreshJobs, 5000);
    </script>
</body>
</html>
"""


@app.route('/')
def index():
    """Render the main page"""
    return render_template_string(HTML_TEMPLATE)


@app.route('/api/jobs', methods=['GET', 'POST'])
def jobs():
    """Get all jobs or add a new job"""
    if request.method == 'GET':
        jobs = scheduler.get_all_jobs()
        return jsonify([job.to_dict() for job in jobs])
    
    elif request.method == 'POST':
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['job_id', 'command', 'start_time', 'interval_seconds']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        # Check if job already exists
        if scheduler.get_job(data['job_id']):
            return jsonify({'error': 'Job with this ID already exists'}), 400
        
        try:
            # Parse start time
            start_time = datetime.fromisoformat(data['start_time'].replace('Z', '+00:00'))
            
            # Add the job
            job = scheduler.add_job(
                job_id=data['job_id'],
                command=data['command'],
                start_time=start_time,
                interval_seconds=int(data['interval_seconds'])
            )
            
            return jsonify(job.to_dict()), 201
        except ValueError as e:
            return jsonify({'error': f'Invalid data: {str(e)}'}), 400


@app.route('/api/jobs/<job_id>', methods=['GET', 'DELETE'])
def job_detail(job_id):
    """Get or delete a specific job"""
    job = scheduler.get_job(job_id)
    
    if not job:
        return jsonify({'error': 'Job not found'}), 404
    
    if request.method == 'GET':
        return jsonify(job.to_dict())
    
    elif request.method == 'DELETE':
        scheduler.remove_job(job_id)
        return jsonify({'message': 'Job deleted successfully'})


@app.route('/api/jobs/<job_id>/results', methods=['GET'])
def job_results(job_id):
    """Get all results for a specific job"""
    results = scheduler.get_job_results(job_id)
    
    if results is None:
        return jsonify({'error': 'Job not found'}), 404
    
    return jsonify([result.to_dict() for result in results])


if __name__ == '__main__':
    # Start the scheduler
    scheduler.start()
    
    # Run the Flask app
    print("Starting Command Scheduler on http://localhost:5000")
    print("Press Ctrl+C to stop")
    
    try:
        app.run(host='0.0.0.0', port=5000, debug=True, use_reloader=False)
    finally:
        scheduler.stop()
