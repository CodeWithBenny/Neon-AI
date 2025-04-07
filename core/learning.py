import json
import os
from typing import Dict


class LearningEngine:
    def __init__(self, profile_dir="data/user_profiles"):
        self.profile_dir = profile_dir
        os.makedirs(profile_dir, exist_ok=True)
        self.user_profiles = {}

    def load_profile(self, user_id: str) -> Dict:
        profile_path = os.path.join(self.profile_dir, f"{user_id}.json")
        if os.path.exists(profile_path):
            with open(profile_path) as f:
                return json.load(f)
        return {"preferences": {}, "history": []}

    def save_profile(self, user_id: str, profile: Dict):
        profile_path = os.path.join(self.profile_dir, f"{user_id}.json")
        with open(profile_path, "w") as f:
            json.dump(profile, f)

    def learn_from_interaction(self, user_id: str, code: str, language: str, feedback: Dict):
        profile = self.load_profile(user_id)

        # Update coding style preferences
        if "style" not in profile["preferences"]:
            profile["preferences"]["style"] = {}

        # Detect style from code
        if "_" in code and code.islower():
            profile["preferences"]["style"]["naming"] = "snake_case"
        elif code and code[0].islower() and not "_" in code:
            profile["preferences"]["style"]["naming"] = "camelCase"

        # Save interaction history
        profile["history"].append({
            "code": code,
            "language": language,
            "feedback": feedback,
            "timestamp": str(datetime.now())
        })

        self.save_profile(user_id, profile)

    def get_user_style(self, user_id: str) -> Dict:
        profile = self.load_profile(user_id)
        return profile.get("preferences", {}).get("style", {})