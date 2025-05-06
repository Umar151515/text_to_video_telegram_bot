from utils.image_utils.create_description import create_description_image
from config import image_folder_path


class Image:
    def __init__(self, file_name: str, description: str = None):
        self.file_name = file_name
        self.description = description
    
    @property
    def file_path(self):
        return image_folder_path / (self.file_name + ".png")
    
    async def generate_description(self):
        if not self.description:
            self.description = await create_description_image(self)
        return self.description
    
    def __str__(self):
        return f"image: name - {self.file_name}, description - {self.description}"