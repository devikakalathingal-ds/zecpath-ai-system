from skill_engine.skill_extractor import SkillExtractor
import json

if __name__ == "__main__":

    sample_resume = """
    I am a Python developer with experience in Machine Learning and Deep Learning.
    Skilled in React, NodeJS, and MongoDB.
    Strong communication and leadership abilities.
    Experienced in MERN stack development.
    """

    extractor = SkillExtractor()
    result = extractor.extract_skills(sample_resume)

    # Print to terminal
    print(json.dumps(result, indent=4))

    # Save output to file
    with open("day9_output.json", "w") as f:
        json.dump(result, f, indent=4)

    print("\nOutput saved to day9_output.json")