from contextlib import contextmanager
from typing import Optional, Literal
from browserstate import BrowserState, BrowserStateOptions

_user_browserstate_instance = None  # Global so unmount can access it

@contextmanager
def with_browserstate(
    user_id: str,
    state_id: str,
    provider: Literal["local", "s3", "gcs", "redis"] = "local",
    storage_path: Optional[str] = None,
    temp_dir: Optional[str] = None,
    redis_options: Optional[dict] = None
):
    """
    Context manager for using BrowserState with Nova Act.
    
    Args:
        user_id: Unique identifier for the user
        state_id: Identifier for this specific browser state
        provider: Storage provider ("local", "s3", "gcs", "redis")
        storage_path: Path for local storage (used with "local" provider)
        temp_dir: Path for temporary directory to mount state
        redis_options: Configuration for Redis connection (used with "redis" provider)
        
    Yields:
        str: Path to the mounted browser state directory to use with Nova
    """
    state_path = mount_browserstate(
        user_id=user_id,
        state_id=state_id,
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
    state_id: str,
    provider: Literal["local", "s3", "gcs", "redis"] = "local",
    storage_path: Optional[str] = None,
    temp_dir: Optional[str] = None,
    redis_options: Optional[dict] = None
) -> str:
    """
    Mount browser state for use with Nova Act.
    
    Args:
        user_id: Unique identifier for the user
        state_id: Identifier for this specific browser state
        provider: Storage provider ("local", "s3", "gcs", "redis")
        storage_path: Path for local storage (used with "local" provider)
        temp_dir: Path for temporary directory to mount state
        redis_options: Configuration for Redis connection (used with "redis" provider)
        
    Returns:
        str: Path to the mounted browser state directory to use with Nova
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
    return _user_browserstate_instance.mount(state_id=state_id)


def unmount_browserstate():
    """
    Unmount the currently mounted browser state.
    
    This function should be called when finished with the browser state to ensure proper cleanup.
    """
    global _user_browserstate_instance
    if _user_browserstate_instance:
        _user_browserstate_instance.unmount()
        _user_browserstate_instance = None 