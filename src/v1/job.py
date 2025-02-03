import json
import uuid
import settings

from datetime import datetime
from datetime import timedelta
from includes.db import Db
from includes.common import Common

class Job:

	def SupportedStatuses():

		return [
			'success',
			'wip',
			'failed'
		]

	def Update(log_id,status,result):

		query = """
			UPDATE logs
			SET status = %s,
				result = %s,
				end_date = %s
			WHERE log_id = %s
		"""

		inputs = (
			status,
			json.dumps(result),
			str(Common.Datetime()),
			log_id
		)

		return Db.ExecuteQuery(query,inputs,True)

	def Running(service,job):
		
		query = """
			SELECT
				log_id,
				date
			FROM logs
			WHERE service = %s
				AND job = %s
				AND status = %s
		"""

		inputs = (
			service,
			job,
			'wip'
		)

		result = Db.ExecuteQuery(query,inputs)

		if not result:
			return False

		running = False

		for x in result:
			elapsed_time = datetime.strptime(Common.Datetime(),'%Y-%m-%d %H:%M:%S') - datetime.strptime(str(x['date']),'%Y-%m-%d %H:%M:%S')
			elapsed_time = elapsed_time.total_seconds()
			elapsed_time = divmod(elapsed_time,60)[0]

			if elapsed_time < settings.CRONS_MAX_EXEC_TIME:
				running = True

				continue

			Job.Update(x['log_id'],'failed','MAX_EXEC_TIME')

		return True if running else False

	def Start(service,job):
		
		api_data = {}
		api_data['ApiHttpResponse'] = 500
		api_data['ApiMessages'] = []
		api_data['ApiResult'] = []

		if Job.Running(service,job):
			api_data['ApiHttpResponse'] = 403
			api_data['ApiMessages'] += ['INFO - An existing job is already running']

			return api_data

		log_id = str(uuid.uuid4())

		query = """
			INSERT INTO logs
			SET log_id = %s,
				service = %s,
				job = %s,
				status = %s,
				date = NOW()
		"""

		inputs = (
			log_id,
			service,
			job,
			'wip',
		)

		if Db.ExecuteQuery(query,inputs,True):
			api_data['ApiHttpResponse'] = 202
			api_data['ApiMessages'] += ['INFO - Request processed successfully']

			api_data['ApiResult'] = log_id

			return api_data

		api_data['ApiHttpResponse'] = 500
		api_data['ApiMessages'] += ['ERROR - Could not create record']

		return api_data

	def End(log_id,status,result):
		
		api_data = {}
		api_data['ApiHttpResponse'] = 500
		api_data['ApiMessages'] = []
		api_data['ApiResult'] = []

		try:
			status = status.lower()

		except:
			api_data['ApiHttpResponse'] = 500
			api_data['ApiMessages'] += ['ERROR - Invalid status']

			return api_data

		if status not in Job.SupportedStatuses():
			api_data['ApiHttpResponse'] = 500
			api_data['ApiMessages'] += ['ERROR - Unsupported status']

			return api_data

		if Job.Update(log_id,status,result):
			api_data['ApiHttpResponse'] = 202
			api_data['ApiMessages'] += ['INFO - Request processed successfully']

			return api_data

		api_data['ApiHttpResponse'] = 500
		api_data['ApiMessages'] += ['ERROR - Could not update records']

		return api_data

	def PurgeLogs():

		api_data = {}
		api_data['ApiHttpResponse'] = 500
		api_data['ApiMessages'] = []
		api_data['ApiResult'] = []

		query = """
			DELETE FROM logs
			WHERE date < %s
		"""

		inputs = (
			str(Common.DatetimeObject() - timedelta(minutes = settings.CRONS_MAX_LOG_RETENTION)),
		)

		if Db.ExecuteQuery(query,inputs):
			api_data['ApiHttpResponse'] = 202
			api_data['ApiMessages'] += ['INFO - Request processed successfully']

			return api_data

		api_data['ApiHttpResponse'] = 500
		api_data['ApiMessages'] += ['ERROR - Could not delete records']

		return api_data