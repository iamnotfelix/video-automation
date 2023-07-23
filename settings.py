import json


class Settings:

    def __init__(self, settings_file_path: str = "settings.json") -> None:
        self.settings_file = settings_file_path
        with open(self.settings_file, "r") as file:
            self.settings = json.load(file)

    # Getters
    
    def get(self, key: str):
        if key in self.settings:
            return self.settings[key]
        return None

    def get_settings(self) -> dict:
        return self.settings
    
    def get_result_path(self) -> str:
        return self.settings["result_path"]
    
    def get_archive_path(self) -> str:
        return self.settings["archive_path"]
    
    def get_duration(self) -> int:
        return self.settings["duration"]
    
    def get_result_name(self) -> str:
        return self.settings["result_name"]
    
    def get_sources(self) -> list[str]:
        return self.settings["sources"]
    
    def get_tags(self) -> list[str]:
        return self.settings["tags"]

    def get_titles(self) -> list[str]:
        return self.settings["titles"]
    
    def get_description(self) -> list[str]:
        return self.settings["description"]
    
    # Setters
    
    def set(self, new_settings: dict) -> None:
        with open(self.settings_file, "w") as file:
            json.dump(new_settings, file)

    def set_result_path(self, result_path: str) -> None:
        self.settings["result_path"] = result_path
    
    def set_archive_path(self, archive_path: str) -> None:
        self.settings["archive_path"] = archive_path
    
    def set_duration(self, duration: int) -> None:
        self.settings["duration"] = duration
    
    def set_result_name(self, result_name: str) -> None:
        self.settings["result_name"] = result_name
    
    def set_sources(self, sources: list[str]) -> None:
        self.settings["sources"] = sources
    
    def set_tags(self, tags: list[str]) -> None:
        self.settings["tags"] = tags
    
    def set_titles(self, titles: list[str]) -> None:
        self.settings["titles"] = titles
    
    def set_description(self, description: str) -> None:
        self.settings["description"] = description

    def set_new(self, key: str, value) -> None:
        self.settings[key] = value

    # Other

    def save(self) -> None:
        with open(self.settings_file, "w") as file:
            json.dump(self.settings, file)

if __name__ == "__main__":
    settings_manager = Settings("test.json")

    settings_manager.set_result_path("result_path")
    settings_manager.set_archive_path("archive_path")
    settings_manager.set_duration(123)
    settings_manager.set_result_name("result_name")
    settings_manager.set_sources(["sources"])
    settings_manager.set_tags(["tags"])
    settings_manager.set_titles(["titles"])
    settings_manager.set_description("description")

    settings_manager.save()
    # print(settings_manager.get_archive_path())
    # print(settings_manager.get_description())