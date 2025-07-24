from utils.logger import logger

BLOCKED_RESOURCES = {"image", "stylesheet", "font", "media", "other"}
BLOCKED_PATTERNS = ["google-analytics", "ads.", "doubleclick", "tracking"]

async def block_junk(route, request):
    try:
        if request.resource_type in BLOCKED_RESOURCES or any(pattern in request.url for pattern in BLOCKED_PATTERNS):
            await route.abort()
        else:
            await route.continue_()
    except Exception as e:
        logger.error(f"Error in block_junk for {request.url}: {e}")
        await route.continue_()