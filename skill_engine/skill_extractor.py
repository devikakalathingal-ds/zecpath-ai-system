# skill_extractor.py

from .skill_dictionary import MASTER_SKILLS, SKILL_SYNONYMS, SKILL_STACKS
from .confidence import calculate_confidence


class SkillExtractor:

    def __init__(self):
        self.master_skills = MASTER_SKILLS
        self.synonyms = SKILL_SYNONYMS
        self.stacks = SKILL_STACKS

    def normalize_text(self, text):
        """
        Convert text to lowercase and replace synonyms
        """
        text = text.lower()

        # Replace synonyms (ml → machine learning, etc.)
        for short, full in self.synonyms.items():
            text = text.replace(short, full)

        return text

    def extract_skills(self, text):
        """
        Extract skills from resume text
        """
        text = self.normalize_text(text)
        extracted = {}

        # Step 1: Extract normal skills
        for category, skills in self.master_skills.items():
            extracted[category] = []

            for skill in skills:
                if skill in text:
                    confidence = calculate_confidence(text, skill)

                    extracted[category].append({
                        "skill": skill,
                        "confidence": confidence
                    })

        # Step 2: Handle Skill Stacks (like MERN)
        for stack_name, stack_skills in self.stacks.items():
            if stack_name in text:
                for skill in stack_skills:
                    extracted.setdefault("technical", []).append({
                        "skill": skill,
                        "confidence": 0.9
                    })

        # Step 3: Remove duplicate skills
        for category in extracted:
            unique = {}
            for item in extracted[category]:
                unique[item["skill"]] = item

            extracted[category] = list(unique.values())

        return extracted