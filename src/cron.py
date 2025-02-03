import sys
import settings

from v1.job import Job

class Cron:

	def Start(self,job):

		data = Job.Start(settings.SVC_NAME,job)

		return data['ApiResult'] if data['ApiResult'] else False

	def __init__(self):

		try:
			job = sys.argv[1]

		except:
			sys.exit('ERROR - No job specified')

		job_uuid = self.Start(job)

		if not job_uuid:
			sys.exit('ERROR - Could not start job')

		if job == 'purge-logs':
			result = Job.PurgeLogs()

		else:
			Job.End(job_uuid,'failed','ERROR - Unsupported job')
			sys.exit('ERROR - Unsupported job')

		Job.End(
			job_uuid,
			'success' if (result.get('ApiHttpResponse') is not None and result.get('ApiHttpResponse') != 500) else 'failed',
			result
		)

		sys.exit()

try:
	Cron()

except Exception as e:
	sys.exit(e)