import unittest
from unittest.mock import MagicMock, patch
import os
import tempfile

class TestBrowserStateNovaAdapter(unittest.TestCase):
    
    def test_create_session_config(self):
        from browserstate_nova_adapter import create_session_config
        
        # Test with minimal parameters
        config = create_session_config(
            user_id="test-user",
            session_id="test-session"
        )
        
        self.assertEqual(config["user_id"], "test-user")
        self.assertEqual(config["session_id"], "test-session")
        self.assertEqual(config["provider"], "local")
        self.assertIsNone(config["storage_path"])
        self.assertIsNone(config["temp_dir"])
        self.assertIsNone(config["redis_options"])
        
        # Test with all parameters
        redis_options = {"host": "localhost", "port": 6379}
        config = create_session_config(
            user_id="test-user",
            session_id="test-session",
            provider="redis",
            storage_path="/custom/path",
            temp_dir="/tmp/browser",
            redis_options=redis_options
        )
        
        self.assertEqual(config["user_id"], "test-user")
        self.assertEqual(config["session_id"], "test-session")
        self.assertEqual(config["provider"], "redis")
        self.assertEqual(config["storage_path"], "/custom/path")
        self.assertEqual(config["temp_dir"], "/tmp/browser")
        self.assertEqual(config["redis_options"], redis_options)
    
    @patch('browserstate_nova_adapter.BrowserState')
    def test_config_with_browserstate(self, mock_browserstate):
        from browserstate_nova_adapter import create_session_config, with_browserstate
        
        # Setup mock
        mock_instance = MagicMock()
        mock_session = {"path": "/tmp/browser_data"}
        mock_instance.mount_session.return_value = mock_session
        mock_browserstate.return_value = mock_instance
        
        # Create config
        config = create_session_config(
            user_id="test-user",
            session_id="test-session",
            provider="local"
        )
        
        # Test using config with context manager
        with with_browserstate(**config) as user_data_dir:
            self.assertEqual(user_data_dir, "/tmp/browser_data")
    
    @patch('browserstate_nova_adapter.BrowserState')
    def test_mount_browserstate(self, mock_browserstate):
        from browserstate_nova_adapter import mount_browserstate, unmount_browserstate
        
        # Setup mock
        mock_instance = MagicMock()
        mock_session = {"path": "/tmp/browser_data"}
        mock_instance.mount_session.return_value = mock_session
        mock_browserstate.return_value = mock_instance
        
        # Test mounting
        result = mount_browserstate(
            user_id="test-user",
            session_id="test-session",
            provider="local"
        )
        
        # Assertions
        self.assertEqual(result, "/tmp/browser_data")
        mock_browserstate.assert_called_once()
        mock_instance.mount_session.assert_called_once_with(session_id="test-session")
        
        # Test unmounting
        unmount_browserstate()
        mock_instance.unmount_session.assert_called_once()
    
    @patch('browserstate_nova_adapter.BrowserState')
    def test_with_browserstate_context_manager(self, mock_browserstate):
        from browserstate_nova_adapter import with_browserstate
        
        # Setup mock
        mock_instance = MagicMock()
        mock_session = {"path": "/tmp/browser_data"}
        mock_instance.mount_session.return_value = mock_session
        mock_browserstate.return_value = mock_instance
        
        # Test context manager
        with with_browserstate(
            user_id="test-user",
            session_id="test-session",
            provider="local"
        ) as user_data_dir:
            self.assertEqual(user_data_dir, "/tmp/browser_data")
            mock_browserstate.assert_called_once()
            mock_instance.mount_session.assert_called_once()
        
        # Verify unmount was called
        mock_instance.unmount_session.assert_called_once()
    
    @patch('browserstate_nova_adapter.BrowserState')
    def test_with_browserstate_exception_handling(self, mock_browserstate):
        from browserstate_nova_adapter import with_browserstate
        
        # Setup mock
        mock_instance = MagicMock()
        mock_session = {"path": "/tmp/browser_data"}
        mock_instance.mount_session.return_value = mock_session
        mock_browserstate.return_value = mock_instance
        
        # Test context manager with exception
        try:
            with with_browserstate(
                user_id="test-user",
                session_id="test-session",
                provider="local"
            ) as user_data_dir:
                self.assertEqual(user_data_dir, "/tmp/browser_data")
                raise Exception("Test exception")
        except Exception:
            pass
        
        # Verify unmount was still called despite exception
        mock_instance.unmount_session.assert_called_once()

if __name__ == '__main__':
    unittest.main() 