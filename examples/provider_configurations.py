from browserstate_nova_adapter import with_browserstate
from nova_act import NovaAct

# Example with local storage provider
with with_browserstate(
    user_id="local-user",
    session_id="local-session",
    provider="local",
    storage_path="/path/to/storage"
) as user_data_dir:
    with NovaAct(starting_page="https://example.com", user_data_dir=user_data_dir) as nova:
        nova.act("search for something")

# Example with Redis provider
with with_browserstate(
    user_id="redis-user",
    session_id="redis-session",
    provider="redis",
    redis_options={
        "host": "localhost",
        "port": 6379,
        "db": 0,
        "password": None,
        "key_prefix": "browserstate:",
        "ttl": 86400  # 24 hours
    }
) as user_data_dir:
    with NovaAct(starting_page="https://example.com", user_data_dir=user_data_dir) as nova:
        nova.act("search for something")

# Example with S3 provider (requires boto3)
with with_browserstate(
    user_id="s3-user",
    session_id="s3-session",
    provider="s3",
    # S3 configuration is handled through boto3 credentials
    # Make sure AWS credentials are configured in your environment
) as user_data_dir:
    with NovaAct(starting_page="https://example.com", user_data_dir=user_data_dir) as nova:
        nova.act("search for something")

# Example with Google Cloud Storage provider (requires google-cloud-storage)
with with_browserstate(
    user_id="gcs-user",
    session_id="gcs-session",
    provider="gcs",
    # GCS configuration is handled through application default credentials
    # Make sure GCP credentials are configured in your environment
) as user_data_dir:
    with NovaAct(starting_page="https://example.com", user_data_dir=user_data_dir) as nova:
        nova.act("search for something") 