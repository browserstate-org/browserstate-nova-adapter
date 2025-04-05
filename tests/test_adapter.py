import unittest
from unittest.mock import MagicMock, patch
import os
import tempfile

class TestBrowserStateNovaAdapter(unittest.TestCase):
    
    @patch('browserstate_nova_adapter.BrowserState')
    def test_mount_browserstate(self, mock_browserstate):
        from browserstate_nova_adapter import mount_browserstate, unmount_browserstate
        
        # Setup mock
        mock_instance = MagicMock()
        mock_instance.mount.return_value = "/tmp/browser_data"
        mock_browserstate.return_value = mock_instance
        
        # Test mounting
        result = mount_browserstate(
            user_id="test-user",
            state_id="test-session",
            provider="local"
        )
        
        # Assertions
        self.assertEqual(result, "/tmp/browser_data")
        mock_browserstate.assert_called_once()
        mock_instance.mount.assert_called_once_with(state_id="test-session")
        
        # Test unmounting
        unmount_browserstate()
        mock_instance.unmount.assert_called_once()
    
    @patch('browserstate_nova_adapter.BrowserState')
    def test_with_browserstate_context_manager(self, mock_browserstate):
        from browserstate_nova_adapter import with_browserstate
        
        # Setup mock
        mock_instance = MagicMock()
        mock_instance.mount.return_value = "/tmp/browser_data"
        mock_browserstate.return_value = mock_instance
        
        # Test context manager
        with with_browserstate(
            user_id="test-user",
            state_id="test-session",
            provider="local"
        ) as user_data_dir:
            self.assertEqual(user_data_dir, "/tmp/browser_data")
            mock_browserstate.assert_called_once()
            mock_instance.mount.assert_called_once()
        
        # Verify unmount was called
        mock_instance.unmount.assert_called_once()
    
    @patch('browserstate_nova_adapter.BrowserState')
    def test_with_browserstate_exception_handling(self, mock_browserstate):
        from browserstate_nova_adapter import with_browserstate
        
        # Setup mock
        mock_instance = MagicMock()
        mock_instance.mount.return_value = "/tmp/browser_data"
        mock_browserstate.return_value = mock_instance
        
        # Test context manager with exception
        try:
            with with_browserstate(
                user_id="test-user",
                state_id="test-session",
                provider="local"
            ) as user_data_dir:
                self.assertEqual(user_data_dir, "/tmp/browser_data")
                raise Exception("Test exception")
        except Exception:
            pass
        
        # Verify unmount was still called despite exception
        mock_instance.unmount.assert_called_once()

if __name__ == '__main__':
    unittest.main() 