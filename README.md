## Batman Microservice - Crons

### Overview
**batman-ms-crons** is a centralized service that tracks the execution of cron jobs across various microservices. It ensures that scheduled tasks are executed reliably, prevents duplicate runs, and maintains execution logs. This service is essential for orchestrating and monitoring time-based jobs in a Kubernetes environment.

### Features
- **Centralized Job Tracking**: Logs every cron job execution, preventing duplicate runs.
- **Automatic Log Purging**: Periodically removes old logs based on retention settings.
- **Execution Monitoring**: Detects long-running or stuck jobs and marks them as failed.
- **Microservice Integration**: Every microservice has a `cron.py` that interacts with batman-ms-crons to log execution events.

### How It Works
When a Kubernetes cron job starts, a record is created in the `batman-ms-crons` database. The microservice running the job logs the execution by calling `Start()`. Upon completion, it updates the job status using `End()`. If a job exceeds a defined execution threshold, it is marked as failed.

#### Example Flow
1. **Start a Job**
   - The microservice calls `Start(service, job)`, which logs the job as `wip` (work in progress) in the database.
   - If a job with the same name is already running, it prevents duplicate execution.

2. **Check for Running Jobs**
   - Before starting a new execution, the service checks `Running(service, job)` to ensure no duplicate jobs are running.

3. **End a Job**
   - Once the cron job completes, the microservice calls `End(log_id, status, result)` to update the execution record.

4. **Purge Old Logs**
   - Every few days, logs older than a defined threshold are automatically deleted by calling `PurgeLogs()`.

### API Endpoints

#### Start a Job
```python
@app.route('/api/v1/Crons/Start', methods=['POST'])
def StartJob():
    data = Job.Start(request.json['service'], request.json['job'])
    return Response(json.dumps(data), status=data['ApiHttpResponse'], mimetype='application/json')
```

#### End a Job
```python
@app.route('/api/v1/Crons/End', methods=['POST'])
def EndJob():
    data = Job.End(request.json['log_id'], request.json['status'], request.json['result'])
    return Response(json.dumps(data), status=data['ApiHttpResponse'], mimetype='application/json')
```

### Microservice Integration
Each microservice that runs cron jobs integrates with `batman-ms-crons` through `cron.py`, ensuring that all scheduled tasks are logged, preventing duplicate executions, and maintaining a complete history of job runs.

### Future Enhancements
- Implementing alerts for failed or long-running jobs.
- Providing a UI dashboard to visualize scheduled tasks and execution history.

> "Even the Dark Knight needs a reliable scheduler. Gotham never sleeps, and neither do our crons."