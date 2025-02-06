import json

from agency_swarm.tools import BaseTool
from pydantic import Field
import io
import tempfile
from pylint.lint import Run
from pylint.reporters import JSONReporter

from CodeAnalyzerAgent.tools.BitbucketGetCodeFromFile import BitbucketGetGetCodeFromFileTool


class CodeQualityAnalyzerTool(BaseTool):
    """
    This tool analyzes code for adherence to quality standards.
    It parses the code, checks for common quality issues such as code style violations,
    complexity, and potential bugs, and generates a report of findings.
    """

    code: str = Field(
        ..., description="The source code to be analyzed for quality issues."
    )

    def run(self):
        """
        Executes the tool's main functionality: analyzing the provided code for quality issues.
        """
        # Write the code string to a temporary Python file
        with tempfile.NamedTemporaryFile(suffix=".py", mode="w+", delete=False) as tmp_file:
            tmp_file.write(self.code)
            tmp_file.flush()
            tmp_filename = tmp_file.name

            # Prepare an in-memory stream to capture JSON output.
            output_stream = io.StringIO()
            reporter = JSONReporter(output=output_stream)

            # Run Pylint with the JSON reporter.
            Run([tmp_filename], reporter=reporter, exit=False)

            # Retrieve the JSON output.
            output_stream.seek(0)
            json_output = output_stream.read()
            results = json.loads(json_output)
            return results


if __name__ == "__main__":
    tool = BitbucketGetGetCodeFromFileTool(
        repository_slug='chatbot-service',
        source_branch_name='development',
        file_path='chatbot_service/database/models/employee_notification_model.py'
    )
    test = tool.run()
    # code_changes = "from typing import Optional, List\nfrom database.database import Base, database_connection\n\nfrom sqlalchemy import (\n    DateTime, String, ForeignKey, Column, Integer\n)\nfrom sqlalchemy.orm import relationship\n\nfrom utils.utils import get_current_utc_time\nfrom database.models.employee_ticket_model import EmployeeTicket\n\n\nclass EmployeeNotificationsFilter:\n    def __init__(self, query=None):\n        self.query = database_connection.query(EmployeeNotification)\n\n    def for_employee(self, employee_id):\n        \"\"\"Filter notifications by employee\"\"\"\n        self.query = self.query.filter_by(employee_id=employee_id)\n        return self\n\n    def for_reference_id(self, reference_id):\n        \"\"\"Filter notifications by reference_id\"\"\"\n        self.query = self.query.filter_by(reference_id=reference_id)\n        return self\n\n    def unread_only(self):\n        \"\"\"Filter for unread notifications\"\"\"\n        self.query = self.query.filter_by(date_notification_viewed=None)\n        return self\n\n    def limit_to(self, limit):\n        \"\"\"Limit the number of results\"\"\"\n        self.query = self.query.limit(limit)\n        return self\n\n    def order_by_date(self, ascending=False):\n        \"\"\"Order by date created\"\"\"\n        order_criteria = EmployeeNotification.date_created.asc() if ascending else EmployeeNotification.date_created.desc()\n        self.query = self.query.order_by(order_criteria)\n        return self\n\n    def of_type(self, notification_type):\n        \"\"\"Filter by notification type\"\"\"\n        self.query = self.query.filter_by(notification_type=notification_type)\n        return self\n\n    def execute(self):\n        \"\"\"Execute the query and return results\"\"\"\n        return self.query.all()\n\n    def first(self):\n        \"\"\"Get first result\"\"\"\n        return self.query.first()\n\n    def count(self):\n        \"\"\"Get count of results\"\"\"\n        return self.query.count()\n\n\nclass EmployeeNotification(Base):\n    __tablename__ = \"app_employeenotification\"\n    __table_args__ = {'extend_existing': True}\n\n    id = Column(Integer, primary_key=True)\n    employee_id = Column(Integer, ForeignKey(\"app_employee.id\"), nullable=False)\n    reference_id = Column(String)\n    data_instance_type = Column(String)\n    notification_type = Column(String)\n    date_notification_sent = Column(DateTime, nullable=True)\n    date_notification_viewed = Column(DateTime, nullable=True)\n    date_created = Column(DateTime, default=get_current_utc_time)\n    date_updated = Column(DateTime, default=get_current_utc_time)\n\n    employee = relationship(\"Employee\")\n\n    MODEL_MAPPING = {\n        \\'EmployeeTicket\\': EmployeeTicket\n    }\n\n    def instance(self):\n        \"\"\"Returns the instance of the data_instance_type using model mapping\"\"\"\n        if not self.data_instance_type or not self.reference_id or not (\n                model_class := self.MODEL_MAPPING.get(self.data_instance_type)):\n            return None\n        return database_connection.query(model_class).get(self.reference_id)\n\n    @classmethod\n    def filter(cls):\n        \"\"\"Returns a new notification filter\"\"\"\n        return EmployeeNotificationsFilter()\n\n    @staticmethod\n    def get_notification(notification_id) -> Optional[\"EmployeeNotification\"]:\n        \"\"\"\n        Get notification by id\n\n        Args:\n            notification_id (int): Notification id\n\n        Returns:\n            Optional[EmployeeNotification]: EmployeeNotification object\n        \"\"\"\n        return database_connection.query(EmployeeNotification).get(notification_id)\n\n\n    @staticmethod\n    def get_notifications_by_reference_id(\n        reference_id: str,\n        include_read: bool = True\n    ) -> List[\"EmployeeNotification\"]:\n        \"\"\"\n        Get notification by reference id\n        Args:\n            reference_id (str): Reference id to filter notifications by\n            include_read (bool, optional): Whether to include already read notifications.\n                Defaults to True.\n        \n        Returns:\n            List[EmployeeNotification]: List of matching notification objects\n        \"\"\"\n        query = EmployeeNotification.filter().for_reference_id(reference_id)\n\n        if not include_read:\n            query = query.unread_only()\n        \n        return query.execute()\n\n    def mark_as_viewed(self):\n        \"\"\"\n        Mark the notification as viewed by setting date_notification_viewed\n        to current UTC time if not already viewed.\n        \"\"\"\n        if self.date_notification_viewed is None:\n            self.date_notification_viewed = get_current_utc_time()\n            database_connection.add(self)\n            database_connection.commit() \n\n    @staticmethod\n    def mark_notifications_by_reference_id_as_viewed(reference_id: str):\n        \"\"\"\n        Mark all unread notifications with the specified reference_id as viewed.\n\n        This method retrieves all unread notifications matching the given reference_id\n        and marks them as viewed by setting their date_notification_viewed to the current\n        UTC time. The changes are committed to the database in a single transaction.\n\n        Args:\n            reference_id (str): The reference ID to filter notifications by\n\n        Note:\n            - Only unread notifications (where date_notification_viewed is None) are affected\n            - If no matching unread notifications are found, the method returns without making any changes\n            - All matching notifications are updated with the same view timestamp\n        \"\"\"\n        notifications = EmployeeNotification.get_notifications_by_reference_id(\n            reference_id=reference_id,\n            include_read=False\n        )\n        \n        if not notifications:\n            return\n            \n        current_time = get_current_utc_time()\n        for notification in notifications:\n            notification.date_notification_viewed = current_time\n            \n        database_connection.add_all(notifications)\n        database_connection.commit()\n\n    @staticmethod\n    def handle_notification_send_trigger(employee_notification_id: int, employee_id: int):\n        from database.models import Employee\n        from services.employee_notification_handlers.employee_notification_handler_factory import \\\n            EmployeeNotificationHandlerFactory\n        from services.employee_notification_handlers.base_employee_notification_handler import \\\n            BaseEmployeeNotificationHandler\n\n        # 1. Get the EmployeeNotification\n        employee_notification = EmployeeNotification.get_notification(notification_id=employee_notification_id)\n        if not employee_notification:\n            raise ValueError(f\"EmployeeNotification {employee_notification_id} not found.\")\n\n        # 2. Get the Employee\n        employee = Employee.get_by_id(employee_id=employee_id)\n        if not employee:\n            raise ValueError(f\"Employee {employee_id} not found.\")\n\n        # 3. Identify the correct handler\n        handler: BaseEmployeeNotificationHandler = EmployeeNotificationHandlerFactory.get_handler(\n            employee_notification.data_instance_type)\n\n        # 4. Use correct handler to send the notification\n        handler.send_out_notification(employee, employee_notification, session=database_connection)\n"
    tool = CodeQualityAnalyzerTool(code=test['file_contents'])
    print(tool.run())