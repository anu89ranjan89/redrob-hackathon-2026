import re

def parse_jd(jd_text):

    requirements = {
        "skills": [],
        "experience": None
    }

    skills = [
        "Python",
        "Embeddings",
        "Retrieval Systems",
        "Ranking Systems",
        "Vector Databases"
    ]

    for skill in skills:
        if skill.lower() in jd_text.lower():
            requirements["skills"].append(skill)

    exp_match = re.search(r"(\d+)\+?\s*years", jd_text.lower())

    if exp_match:
        requirements["experience"] = int(exp_match.group(1))

    return requirements


if __name__ == "__main__":

    sample_jd = """
    Looking for a Senior AI Engineer with
    6+ years experience in Python,
    Embeddings, Retrieval Systems,
    Ranking Systems and Vector Databases.
    """

    print(parse_jd(sample_jd))