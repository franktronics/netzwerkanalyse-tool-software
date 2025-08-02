from abc import ABC, abstractmethod

class FileManagerPort(ABC):
    """
    Abstract base class for file management operations in the analyser module.
    """

    @abstractmethod
    def load_json_file(self, file_path: str) -> dict | None:
        """
        Load a JSON file and return its content as a dictionary.
        The resulting dictionary is cached for future use to avoid repeated file reads.

        Args:
            file_path (str): The path to the JSON file.

        Returns:
            dict: The content of the JSON file.
            None: If the file does not exist or cannot be read.
        """
        pass