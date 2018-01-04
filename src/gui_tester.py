# Gui tester

from Scheduler.Controllers.ProjectWidget import ProjectWidget
import Scheduler.Configuration.database as database

from PyQt5 import QtWidgets
import sys

database.setup()
app = QtWidgets.QApplication(sys.argv)

# TODO create a project with our sample data, find its project id
unscheduled_sample_project_id = '1'
scheduled_sample_project_id = '1' # TODO
blank_sample_project_id = '1' # TODO

# TEST [VISUAL] load_from_db - Test load scheduled data into project info text boxes and table and produces schedule
ex = ProjectWidget(project_id=scheduled_sample_project_id).show()

# TEST [VISUAL] load_from_db - Test load unscheduled data into project info text boxes and table
ex = ProjectWidget(project_id=unscheduled_sample_project_id)

# TEST [VISUAL] load_from_db - Test loads blank data into project info text boxes and table
ex = ProjectWidget(project_id=unscheduled_sample_project_id)

# TODO  tests
'''
data_to_events_and_activities.py:
  data_to_events_and_activities

ProjectWidget.py:
 - load_from_db
 - update_project_db
 - update_dependeny_listview (maybe)
 - get_event_dependencies (maybe)
 - add_event_from_inputs (maybe)
 - delete_activity (maybe)
 - create_schedule_project (maybe)

plot_gantt.py
 - plot_gantt
'''
sys.exit(app.exec_())
