
from PyPDF2 import PdfReader


def extract_resume_text(resume_file):

    try:
        reader = PdfReader(resume_file)

        extracted_text = ""

        for page in reader.pages:
            text = page.extract_text()

            if text:
                extracted_text += text + "\n"

        return extracted_text.strip()

    except Exception as error:
        print("Resume extraction error:", error)
        return ""


def extract_skills(resume_text):

    skill_keywords = [
        'Python',
        'Django',
        'Java',
        'JavaScript',
        'HTML',
        'CSS',
        'SQL',
        'MySQL',
        'PostgreSQL',
        'React',
        'Node.js',
        'C',
        'C++',
        'Machine Learning',
        'Data Analysis',
        'Excel',
        'Power BI',
        'Git',
        'REST API'
    ]

    found_skills = []

    resume_text = resume_text.lower()

    for skill in skill_keywords:

        if skill.lower() in resume_text:
            found_skills.append(skill)

    return found_skills


def calculate_skill_match(candidate_skills, required_skills):

    required_skills_list = [
        skill.strip().lower()
        for skill in required_skills.split(',')
        if skill.strip()
    ]

    candidate_skills_list = [
        skill.lower()
        for skill in candidate_skills
    ]

    if not required_skills_list:
        return 0

    matched_skills = [
        skill
        for skill in required_skills_list
        if skill in candidate_skills_list
    ]

    match_percentage = (
        len(matched_skills) / len(required_skills_list)
    ) * 100

    return round(match_percentage, 2)


def get_skill_details(candidate_skills, required_skills):

    required_skills_list = [
        skill.strip().lower()
        for skill in required_skills.split(',')
        if skill.strip()
    ]

    candidate_skills_list = [
        skill.lower()
        for skill in candidate_skills
    ]

    matched_skills = [
        skill for skill in required_skills_list
        if skill in candidate_skills_list
    ]

    missing_skills = [
        skill for skill in required_skills_list
        if skill not in candidate_skills_list
    ]

    return matched_skills, missing_skills
