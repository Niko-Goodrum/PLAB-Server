from fastapi import HTTPException


class ImageNotFoundError(Exception):
    pass

class ImageExtensionError(Exception):
    pass

class FileIsNotImageError(Exception):
    pass

class MaxFileSizeError(Exception):
    pass

class UrlLoadError(Exception):
    pass

class UploadError(Exception):
    pass

class PortfolioAvailableError(Exception):
    pass

class PortfolioNotFoundError(Exception):
    pass