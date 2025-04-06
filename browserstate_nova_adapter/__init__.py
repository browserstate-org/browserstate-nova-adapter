from typing import Dict, Any, Optional, Union, Literal, Generator
from contextlib import contextmanager
import os
import tempfile
from browserstate import BrowserState, BrowserStateOptions

class BrowserStateSession:
    """Manages a single browser state session."""
    
    def __init__(
        self,
        user_id: str,
        session_id: str,
        provider: Literal["local", "redis", "s3", "gcs"] = "local",
        **browserstate_options: BrowserStateOptions
    ):
        """
        Initialize a browser state session.
        
        Args:
            user_id: Unique identifier for the user
            session_id: Unique identifier for the session
            provider: Storage provider (local, redis, s3, gcs)
            **browserstate_options: Additional options to pass to BrowserState
        """
        self.user_id = user_id
        self.session_id = session_id
        self.provider = provider
        self.browserstate_options = browserstate_options
        self._browser_state: Optional[BrowserState] = None
        self._temp_dir: Optional[str] = None
    
    def mount(self) -> str:
        """
        Mount the browser state session.
        
        Returns:
            str: Path to the mounted browser session directory
        """
        if self._browser_state is not None:
            raise RuntimeError("Browser state is already mounted")
            
        self._temp_dir = tempfile.mkdtemp()
        self._browser_state = BrowserState(
            user_id=self.user_id,
            session_id=self.session_id,
            provider=self.provider,
            **self.browserstate_options
        )
        self._browser_state.mount(self._temp_dir)
        return self._temp_dir
    
    def unmount(self) -> None:
        """Unmount the browser state session."""
        if self._browser_state is not None:
            self._browser_state.unmount()
            self._browser_state = None
            self._temp_dir = None
    
    def __enter__(self) -> str:
        """Context manager entry."""
        return self.mount()
    
    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        """Context manager exit."""
        self.unmount()
    
    @property
    def is_mounted(self) -> bool:
        """Check if the browser state is currently mounted."""
        return self._browser_state is not None
    
    @property
    def temp_dir(self) -> Optional[str]:
        """Get the temporary directory path if mounted."""
        return self._temp_dir

def create_session_config(
    user_id: str,
    session_id: str,
    provider: Literal["local", "redis", "s3", "gcs"] = "local",
    **browserstate_options: BrowserStateOptions
) -> Dict[str, Union[str, BrowserStateOptions]]:
    """
    Create a reusable session configuration for BrowserStateSession.
    
    Args:
        user_id: Unique identifier for the user
        session_id: Unique identifier for the session
        provider: Storage provider (local, redis, s3, gcs)
        **browserstate_options: Additional options to pass to BrowserState
        
    Returns:
        Dict[str, Union[str, BrowserStateOptions]]: Configuration dictionary
    """
    return {
        "user_id": user_id,
        "session_id": session_id,
        "provider": provider,
        **browserstate_options
    }

@contextmanager
def with_browserstate(
    user_id: str,
    session_id: str,
    provider: Literal["local", "redis", "s3", "gcs"] = "local",
    **browserstate_options: BrowserStateOptions
) -> Generator[str, None, None]:
    """
    Context manager for mounting and unmounting browser state.
    
    Args:
        user_id: Unique identifier for the user
        session_id: Unique identifier for the session
        provider: Storage provider (local, redis, s3, gcs)
        **browserstate_options: Additional options to pass to BrowserState
        
    Yields:
        str: Path to the mounted browser session directory
    """
    session = BrowserStateSession(
        user_id=user_id,
        session_id=session_id,
        provider=provider,
        **browserstate_options
    )
    with session as user_data_dir:
        yield user_data_dir

def mount_browserstate(
    user_id: str,
    session_id: str,
    provider: Literal["local", "redis", "s3", "gcs"] = "local",
    **browserstate_options: BrowserStateOptions
) -> str:
    """
    Mount a browser state session.
    
    Args:
        user_id: Unique identifier for the user
        session_id: Unique identifier for the session
        provider: Storage provider (local, redis, s3, gcs)
        **browserstate_options: Additional options to pass to BrowserState
        
    Returns:
        str: Path to the mounted browser session directory
    """
    session = BrowserStateSession(
        user_id=user_id,
        session_id=session_id,
        provider=provider,
        **browserstate_options
    )
    return session.mount()

def unmount_browserstate() -> None:
    """Unmount the current browser state session."""
    # This is now a no-op as unmounting is handled by the BrowserStateSession class
    pass 