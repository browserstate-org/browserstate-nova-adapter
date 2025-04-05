import unittest
from unittest.mock import MagicMock, patch

class TestProvidersConfig(unittest.TestCase):
    
    @patch('browserstate_nova_adapter.BrowserState')
    def test_local_provider(self, mock_browserstate):
        from browserstate_nova_adapter import mount_browserstate
        
        # Setup mock
        mock_instance = MagicMock()
        mock_instance.mount.return_value = "/tmp/browser_data"
        mock_browserstate.return_value = mock_instance
        
        # Test with local provider
        result = mount_browserstate(
            user_id="test-user",
            state_id="test-session",
            provider="local",
            storage_path="/custom/storage/path"
        )
        
        # Verify options
        mock_browserstate.assert_called_once()
        options = mock_browserstate.call_args[0][0]
        self.assertEqual(options.user_id, "test-user")
        self.assertEqual(options.provider, "local")
        self.assertEqual(options.storage_path, "/custom/storage/path")
    
    @patch('browserstate_nova_adapter.BrowserState')
    def test_redis_provider(self, mock_browserstate):
        from browserstate_nova_adapter import mount_browserstate
        
        # Setup mock
        mock_instance = MagicMock()
        mock_instance.mount.return_value = "/tmp/browser_data"
        mock_browserstate.return_value = mock_instance
        
        # Test with Redis provider
        redis_options = {
            "host": "redis.example.com",
            "port": 6379,
            "db": 1,
            "password": "secret",
            "key_prefix": "test:",
            "ttl": 3600
        }
        
        result = mount_browserstate(
            user_id="test-user",
            state_id="test-session",
            provider="redis",
            redis_options=redis_options
        )
        
        # Verify options
        mock_browserstate.assert_called_once()
        options = mock_browserstate.call_args[0][0]
        self.assertEqual(options.user_id, "test-user")
        self.assertEqual(options.provider, "redis")
        self.assertEqual(options.redis_options, redis_options)
    
    @patch('browserstate_nova_adapter.BrowserState')
    def test_s3_provider(self, mock_browserstate):
        from browserstate_nova_adapter import mount_browserstate
        
        # Setup mock
        mock_instance = MagicMock()
        mock_instance.mount.return_value = "/tmp/browser_data"
        mock_browserstate.return_value = mock_instance
        
        # Test with S3 provider
        result = mount_browserstate(
            user_id="test-user",
            state_id="test-session",
            provider="s3"
        )
        
        # Verify options
        mock_browserstate.assert_called_once()
        options = mock_browserstate.call_args[0][0]
        self.assertEqual(options.user_id, "test-user")
        self.assertEqual(options.provider, "s3")
    
    @patch('browserstate_nova_adapter.BrowserState')
    def test_gcs_provider(self, mock_browserstate):
        from browserstate_nova_adapter import mount_browserstate
        
        # Setup mock
        mock_instance = MagicMock()
        mock_instance.mount.return_value = "/tmp/browser_data"
        mock_browserstate.return_value = mock_instance
        
        # Test with GCS provider
        result = mount_browserstate(
            user_id="test-user",
            state_id="test-session",
            provider="gcs"
        )
        
        # Verify options
        mock_browserstate.assert_called_once()
        options = mock_browserstate.call_args[0][0]
        self.assertEqual(options.user_id, "test-user")
        self.assertEqual(options.provider, "gcs")

if __name__ == '__main__':
    unittest.main() 