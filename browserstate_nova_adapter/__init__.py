from contextlib import contextmanager
from typing import Optional, Literal
from browserstate import BrowserState, BrowserStateOptions

_user_browserstate_instance = None  # Global so unmount can access it

@contextmanager
def with_browserstate(
    user_id: str,
    session_id: str,
    provider: Literal["local", "s3", "gcs", "redis"] = "local",
    storage_path: Optional[str] = None,
    temp_dir: Optional[str] = None,
    redis_options: Optional[dict] = None
):
    """
    Context manager for using BrowserState with Nova Act.
    
    Args:
        user_id: Unique identifier for the user
        session_id: Identifier for this specific browser session
        provider: Storage provider ("local", "s3", "gcs", "redis")
        storage_path: Path for local storage (used with "local" provider)
        temp_dir: Path for temporary directory to mount session
        redis_options: Configuration for Redis connection (used with "redis" provider)
        
    Yields:
        str: Path to the mounted browser session directory to use with Nova
    """
    state_path = mount_browserstate(
        user_id=user_id,
        session_id=session_id,
        provider=provider,
        storage_path=storage_path,
        temp_dir=temp_dir,
        redis_options=redis_options
    )
    try:
        yield state_path
    finally:
        unmount_browserstate()


def mount_browserstate(
    user_id: str,
    session_id: str,
    provider: Literal["local", "s3", "gcs", "redis"] = "local",
    storage_path: Optional[str] = None,
    temp_dir: Optional[str] = None,
    redis_options: Optional[dict] = None
) -> str:
    """
    Mount browser session for use with Nova Act.
    
    Args:
        user_id: Unique identifier for the user
        session_id: Identifier for this specific browser session
        provider: Storage provider ("local", "s3", "gcs", "redis")
        storage_path: Path for local storage (used with "local" provider)
        temp_dir: Path for temporary directory to mount session
        redis_options: Configuration for Redis connection (used with "redis" provider)
        
    Returns:
        str: Path to the mounted browser session directory to use with Nova
    """
    global _user_browserstate_instance
    options = BrowserStateOptions(
        user_id=user_id,
        provider=provider,
        storage_path=storage_path,
        temp_dir=temp_dir,
        redis_options=redis_options
    )
    _user_browserstate_instance = BrowserState(options)
    return _user_browserstate_instance.mount_session(session_id=session_id)["path"]


def unmount_browserstate():
    """
    Unmount the currently mounted browser session.
    
    This function should be called when finished with the browser session to ensure proper cleanup.
    """
    global _user_browserstate_instance
    if _user_browserstate_instance:
        _user_browserstate_instance.unmount_session()
        _user_browserstate_instance = None 