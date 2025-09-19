from typing import Dict, Any
from database_migration_assistant.tools.generic import GenericDBAssessment

class MySQLDBAssessment(GenericDBAssessment):

    def process_assessment(DBHostName: str,
        DBHostPort:int,
        DBHostUserName: str,
        DBHostUserPass: str
    ) -> Dict[str, Any]:
        print("Inside Mysql Assessment")
        pass

if __name__ == "__main__":
    MySQLDBAssessment.process_assessment(DBHostName='a', DBHostPort=1, DBHostUserName='a' ,DBHostUserPass='a')