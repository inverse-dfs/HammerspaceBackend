from pydantic import Field
from pydantic_settings import BaseSettingsx

class Config(BaseSettings):
    """
    This class reads the following fields from environment variables (case-insensitive).
    It demands that they exist or it will crash the server on startup.
    """
    mathpixsnip_key: str = Field()
    image_bucket: str = Field()
    download_bucket: str = Field()
