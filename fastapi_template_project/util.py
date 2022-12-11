"""
Implements async download
"""

from fastapi import UploadFile  # type: ignore
from fastapi_template_project.settings import UPLOAD_CHUNK_SIZE


async def async_download(src: UploadFile, dst: str) -> None:
    """Downloads a file to the destination."""
    with open(dst, mode="wb") as filed:
        while (chunk := await src.read(UPLOAD_CHUNK_SIZE)) != b"":
            filed.write(chunk)
    await src.close()
