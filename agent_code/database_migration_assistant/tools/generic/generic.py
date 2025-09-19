from abc import ABC, abstractmethod
from typing import Dict, Any

class GenericDBAssessment(ABC):
    """
    Generic Class Structure for DB Assessment tool
    """
    
    @classmethod
    @abstractmethod
    def process_assessment(DBHostName: str,
        DBHostPort:int,
        DBHostUserName: str,
        DBHostUserPass: str
    ) -> Dict[str, Any]:
        """
        Performs a comprehensive database assessment.

        This abstract class method must be implemented by subclasses to connect 
        to a specific database type (e.g., MySQL, PostgreSQL) and execute 
        assessment logic. It encapsulates the core business logic of the 
        DBA assessment.

        Args:
            DBHostName: The network hostname or IP address of the database server.
            DBHostPort: The network port the database server is listening on.
            DBHostUserName: The username credential for connecting to the database.
            DBHostUserPass: The password credential for connecting to the database.

        Returns:
            A dictionary containing the assessment results, typically including 
            status, metrics, configuration warnings, and recommendations. 
            Example structure: 
            {'status': 'Success', 'metrics': {...}, 'recommendations': [...]}
        """
        pass