import frappe
from frappe.model.document import Document

class UserStory(Document):
	def on_update(self):
		"""
		Automatically create a Software Task when the User Story is approved.
		"""
		if self.status == "Approved" and self.get_db_value("status") != "Approved":
			self.create_task()

	def create_task(self):
		# Check if a task already exists for this User Story to avoid duplicates
		if not frappe.db.exists("Software Task", {"user_story": self.name}):
			task = frappe.get_doc({
				"doctype": "Software Task",
				"title": self.title,
				"user_story": self.name,
				"project": self.project,
				"status": "To Do",
				"description": self.description
			})
			task.insert(ignore_permissions=True)
			# Notify the user that a task has been created
			frappe.msgprint(frappe._("Software Task {0} has been created for the approved User Story.").format(task.name))
