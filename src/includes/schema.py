import settings

from includes.db import Db

class Schema:

	def CreateDatabase():

		return Db.ExecuteQuery(f"CREATE DATABASE IF NOT EXISTS {settings.DB_NAME} CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci",None,True,True)

	def CreateTables():
		
		#####################################################################################################
		query = """
			CREATE TABLE IF NOT EXISTS logs (
				log_id VARCHAR(45) PRIMARY KEY NOT NULL,
				service VARCHAR(45) NOT NULL,
				job VARCHAR(45) NOT NULL,
				status VARCHAR(15) DEFAULT 'wip',
				result LONGTEXT DEFAULT NULL,
				end_date DATETIME DEFAULT NULL,
				date DATETIME DEFAULT NULL
			) ENGINE=INNODB;
		"""

		if not Db.ExecuteQuery(query,None,True):
			return False

		Db.ExecuteQuery("ALTER TABLE logs ADD INDEX service (service);",None,True)
		Db.ExecuteQuery("ALTER TABLE logs ADD INDEX job (job);",None,True)
		Db.ExecuteQuery("ALTER TABLE logs ADD INDEX status (status);",None,True)
		Db.ExecuteQuery("ALTER TABLE logs ADD INDEX end_date (end_date);",None,True)
		Db.ExecuteQuery("ALTER TABLE logs ADD INDEX date (date);",None,True)
		#####################################################################################################

		return True