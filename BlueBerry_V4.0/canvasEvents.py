from canvas import Canvas
import json, time
from threading import Thread
from assignment import Assignment


class Json:
    def update_currentAssignments(obj: json, course_teacher: str):
        with open(f"jsons/current_course_assignments/{course_teacher}.json", "w") as f:
            json.dump(obj, f)

    def get_currentAssignments(course_teacher: str) -> dict:
        with open(f"jsons/current_course_assignments/{course_teacher}.json", "r") as f:
            return json.load(f)


class EventsHandler(Canvas):

    @classmethod
    def _get_new_assignments(cls, previous_assignments: dict, new_assignments: dict, teacher: str) -> list:
        if len(list(new_assignments.keys())) > len(list(previous_assignments.keys())):
            """ if new assignment was posted: """

            _new_assignments = []

            # check for differences in the keys
            old_keys = list(previous_assignments.keys())
            new_keys = list(new_assignments.keys())
            for key in (new_keys):
                if key not in old_keys:
                    _new_assignments.append((new_assignments.get(key), key))

            # create "assignment" obj for each of the new _new_assignments
            _new_assignments = [Assignment(_assignment, assignment_name=_name, assigned_in=teacher) for _assignment, _name in _new_assignments]
            return _new_assignments

        """ new_assignments was shorter than previous_assignments. Means an assignment was removed. No need to trigger new_assignment event """
        return False


    @classmethod
    def __new_assignment_posted__(cls, on_new_assignment_posted) -> None:

        """ custom event-handler function decorator """

        def _wrapper():
            class_teachers = list(cls.courses.keys())
            while True:
                time.sleep(15)
                current_assignments = { teacher: Json.get_currentAssignments(teacher) for teacher in class_teachers }
                for teacher in class_teachers:
                    assignments = cls.parseAssignments(cls.getAssignments(teacher))
                    if len(list(current_assignments.get(teacher).keys())) != len(list(assignments.keys())):
                        _new_assignments = cls._get_new_assignments(previous_assignments=current_assignments.get(teacher), new_assignments=assignments, teacher=teacher)

                        # update 'comparison' variables
                        Json.update_currentAssignments(assignments, course_teacher=teacher)
                        current_assignments[teacher] = Json.get_currentAssignments(course_teacher=teacher)

                        if _new_assignments:
                            # trigger events
                            for _assignment in _new_assignments:
                                on_new_assignment_posted(_assignment)

        thread = Thread(daemon=True, target=_wrapper)
        thread.start()