"""
Script to delete all files from the database and file system.
"""
import frappe
import sys

from pymysql.err import InterfaceError


def main():
	if len(sys.argv) != 2:
		print("Usage (inside /sites directory): python attachment_delete.py <site_name>")
		sys.exit(1)
	site_name = sys.argv[1]
	frappe.init(site_name)
	frappe.connect()
	files = frappe.get_all("File", ["name", "file_url"])
	print(f"Deleting {len(files)} files")
	for i, file in enumerate(files, start=1):
		try:
			frappe.delete_doc("File", file.name, delete_permanently=True)
		except InterfaceError:
			frappe.db.connect()
			frappe.delete_doc("File", file.name, delete_permanently=True)
		except Exception as e:
			print(f"Error deleting file {file.name} with url {file.file_url}: {e}")
		if i % 1000 == 0:
			frappe.db.commit()
	frappe.db.commit()
	frappe.destroy()


if __name__ == "__main__":
	main()
