from browserstate_nova_adapter import with_browserstate
from nova_act import NovaAct

# Example 1: Using with context manager
with with_browserstate(
    user_id="demo-user",
    state_id="nova-session",
    provider="redis",  # or 'local', 's3', 'gcs'
    redis_options={"host": "localhost", "port": 6379}
) as user_data_dir:
    with NovaAct(starting_page="https://example.com", user_data_dir=user_data_dir) as nova:
        nova.act("search for something")
        
# Example 2: Manual mounting and unmounting
from browserstate_nova_adapter import mount_browserstate, unmount_browserstate

user_data_dir = mount_browserstate(
    user_id="demo",
    state_id="session1",
    provider="local"
)

try:
    with NovaAct(starting_page="https://example.com", user_data_dir=user_data_dir) as nova:
        nova.act("search for something")
finally:
    unmount_browserstate() 