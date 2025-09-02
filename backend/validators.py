from pathlib import Path
from fastapi import UploadFile

class DocumentValidator:
    def __init__(self, max_size: int = 10 * 1024 * 1024):  # 10MB max
        self.max_size = max_size
        self.allowed_extensions = {'.pdf', '.txt', '.json'}

    async def validate_file(self, file: UploadFile) -> dict:
        result = {"valid": True, "errors": []}

        # Check if user selected a file
        if not file.filename or file.filename.strip() == "":
            result["valid"] = False
            result["errors"].append("No file selected")
            return result

        # Check file extension
        file_ext = Path(file.filename).suffix.lower()
        if file_ext not in self.allowed_extensions:
            result["valid"] = False
            result["errors"].append(
                f"File extension '{file_ext}' not allowed. Use .txt, or .json"
            )

        # Read file to check size
        content = await file.read()
        await file.seek(0)

        # Check file size
        file_size = len(content)
        if file_size > self.max_size:
            result["valid"] = False
            result["errors"].append(
                f"File too large ({file_size:,} bytes). Maximum: {self.max_size:,} bytes"
            )

        return result
