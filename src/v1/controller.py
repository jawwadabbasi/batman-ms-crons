import inspect

from services.logger import Logger
from v1.job import Job

class Ctrl_v1:

	def Response(endpoint, request_data=None, api_data=None, log=True):

		if log is True:
			Logger.CreateServiceLog(endpoint, request_data, api_data)

		return api_data

	def BadRequest(endpoint,request_data = None):

		api_data = {}
		api_data['ApiHttpResponse'] = 400
		api_data['ApiMessages'] = ['ERROR - Missing required parameters']
		api_data['ApiResult'] = []

		Logger.CreateServiceLog(endpoint, request_data, api_data)
		
		return api_data

	def StartJob(request_data):

		if (not request_data.get('Service')
			or not request_data.get('Job')		
		):
			return Ctrl_v1.BadRequest(inspect.stack()[0][3],request_data)

		api_data = Job.Start(
			request_data.get('Service'),
			request_data.get('Job')
		)

		return Ctrl_v1.Response(inspect.stack()[0][3],request_data,api_data)

	def EndJob(request_data):

		if (not request_data.get('LogId')
			or not request_data.get('Status')
		):
			return Ctrl_v1.BadRequest(inspect.stack()[0][3],request_data)

		api_data = Job.End(
			request_data.get('LogId'),
			request_data.get('Status'),
			request_data.get('Result',None)
		)

		return Ctrl_v1.Response(inspect.stack()[0][3],request_data,api_data)