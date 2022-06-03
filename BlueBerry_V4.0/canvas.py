import requests, json, re


# ---------------------------------------------------------------------


class _Data:
    # codes expire 06/15/22
    chris_code = "17094~qbFPFes2sOvfeqUCVnRhCxvENw19Xx8Gk3UaDcVznsD5vH8sCj0BwscssyRzQ3SJ"
    dylan_code = "17094~VVKLS9VJ7ykmviJWQX1xYmGNuycm549i6Lpq4bVBePh7Uzak2Bss4mr3FXQlCDkL"
    noah_code = "17094~8sh68HQhrf9S9s7iaprL3VvLMztyrjOgHBAxHOgVVe2EAWYJiZXhU8kXfZj10THJ"
    madisen_code = "17094~CxRS2HCuK7mSasrVIFT8jgUzLzP0fqwhx1Jzevn2oQMxT6Y9zPXmKFqqugXFvzJM"
    bella_code = "17094~1aKU5fYKidu16lQQ5v5FGQvKTysFTbynY2fpQbFjJ5idQN38NzzERqv6w9AfPM2k"
    
    courses = {
        "simons": ("3294", chris_code),
        "piper": ("3268", chris_code),
        "hagerty": ("3387", chris_code),
        "king": ("3485", chris_code),
        "de_la_torre": ("3641", chris_code),
      
        "konish": ("3689", dylan_code),
      
        "decoste": ("3321", noah_code),
        "kilbane": ("3110", noah_code),
        "zaragoza": ("3262", noah_code),

        "fullerton": ("3526", madisen_code),
      
        "jones": ("4312", bella_code)
    }
    
    request_parameters = [
        "name",
        "description",
        "due_at",
        "points_possible",
        "submission_types",
        "html_url"
    ]

    _possible_params = [
        'id', 'description', 'due_at', 'unlock_at', 'lock_at', 'points_possible', 'grading_type', 'assignment_group_id', 
        'grading_standard_id', 'created_at', 'updated_at', 'peer_reviews', 'automatic_peer_reviews', 'position',
        'grade_group_students_individually', 'anonymous_peer_reviews', 'group_category_id', 'post_to_sis', 'moderated_grading',
        'omit_from_final_grade', 'intra_group_peer_reviews', 'anonymous_instructor_annotations', 'anonymous_grading',
        'graders_anonymous_to_graders', 'grader_count', 'grader_comments_visible_to_graders', 'final_grader_id',
        'grader_names_visible_to_final_grader', 'allowed_attempts', 'annotatable_attachment_id', 'secure_params', 'course_id',
        'name', 'submission_types', 'has_submitted_submissions', 'due_date_required', 'max_name_length', 'in_closed_grading_period',
        'is_quiz_assignment', 'can_duplicate', 'original_course_id', 'original_assignment_id', 'original_lti_resource_link_id',
        'original_assignment_name', 'original_quiz_id', 'workflow_state', 'important_dates', 'muted', 'html_url', 'published',
        'only_visible_to_overrides', 'bucket', 'locked_for_user', 'submissions_download_url', 'post_manually', 'anonymize_students', 'require_lockdown_browser'
    ]


# ---------------------------------------------------------------------


def _cleanhtml(raw: str) -> str:
    """ Parse all html from a string. Return cleaned string. Any links that may have been cleaned by the regex will be appended to the return value """
    
    def _find(string: str) -> list:
        """ return all links in a string """
        regex = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"
        url = re.findall(regex, string)
        return [x[0] for x in url]

    regex = re.compile('<.*?>')
    cleantext = re.sub(regex, '', str(raw))

    while "&nbsp;" in cleantext:
        cleantext = cleantext.replace("&nbsp;", "")

    links = _find(str(raw))
    return f"{cleantext}\n" + "\n".join(links)
    

# ---------------------------------------------------------------------


class Canvas(_Data):
    @classmethod
    def getClassInfo(cls, teacher: str) -> list:
        return cls.courses.get(teacher)

    @classmethod
    def getCourseInfo(cls, teacher: str) -> dict:
      classCode, canvasKey = cls.getClassInfo(teacher)
      if teacher in (cls.courses.keys()):
        headers = {
        'Authorization': 'Bearer {}'.format(canvasKey),
        }
        data = {
        'query': 'query courseInfo($courseId: ID!) {\n       course(id: $courseId) {\n        id\n        _id\n        name\n       }\n     }',
        'variables[courseId]': classCode
        }
        return json.loads(requests.post('https://mrpk.instructure.com/api/graphql', headers=headers, data=data).text)

    @classmethod
    def getAssignments(cls, teacher: str) -> dict:
      if teacher in list(cls.courses.keys()):
        classCode, canvasKey = cls.getClassInfo(teacher)
        headers = {
        'Authorization': 'Bearer {}'.format(canvasKey),
        }
        return json.loads((requests.get(f"https://mrpk.instructure.com/api/v1/courses/{classCode}/assignments?bucket=upcoming", headers=headers)).text)

    @classmethod
    def parseAssignments(cls, assignments: list) -> dict:
        params = cls.request_parameters

        # make sure name was passed in params
        if "name" not in params:
            raise Exception("'Parameters' argument must include 'name' paramater")
        
        # check to see if params exist
        for param in params:
            if param not in cls._possible_params:
                raise Exception(f"Given parameter ({param}) does not exist")

        parsed_assignments = {}

        for assignment in assignments:
            # get all values but name from assignment
            assignment_name = assignment.get("name")
            parsed_assignments[assignment_name] = {params[i]: assignment[params[i]] for i in range(len(params)) if params[i] != "name"}
            if "description" in params: 
                parsed_assignments[assignment_name]["description"] = _cleanhtml(parsed_assignments.get(assignment_name).get("description")) if (parsed_assignments.get(assignment_name).get("description") != None) else "This assignment has no description"

        return parsed_assignments

    @classmethod
    def remove_params(cls, *params: str) -> None:
        '''
        If the param does not exist in the current parameters nothing will happen.
        Taboo params will be ignored
        '''
        for param in params:
            if param in cls.request_parameters:
                cls.request_parameters.remove(param)

    @classmethod
    def add_params(cls, *params: str) -> None:
        """
        An exception will be raised if the user tries to add a param that could not exist 
        If the param is already in the request parameters it will not be added again
        """
        for param in params:
            if param in cls._possible_params:
                if param not in cls.request_parameters:
                    cls.request_parameters.append(param)
            else:
                raise Exception(f"{param} does not exit")
        
    @classmethod
    def get_params(cls) -> list:
        return cls.request_parameters

    @classmethod
    def list_possible_params(cls) -> str:
        return ", ".join(cls._possible_params)


# ---------------------------------------------------------------------


if __name__ == "__main__":
    raw_response = Canvas.getAssignments(Canvas.courses.get("simons"), Canvas.code)
    assignments = Canvas.parseAssignments(raw_response, Canvas.request_parameters)