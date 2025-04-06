"""
Example of using multiple session configurations for different purposes.
"""
from browserstate_nova_adapter import with_browserstate, create_session_config
from nova_act import NovaAct

# Create different configurations for different websites or tasks
amazon_config = create_session_config(
    user_id="web-user",
    session_id="amazon-session",
    provider="local",
    storage_path="./browser_sessions"
)

gmail_config = create_session_config(
    user_id="web-user",
    session_id="gmail-session",
    provider="local",
    storage_path="./browser_sessions"
)

banking_config = create_session_config(
    user_id="web-user",
    session_id="banking-session",
    provider="local",
    storage_path="./browser_sessions"
)

def browse_amazon():
    with with_browserstate(**amazon_config) as user_data_dir:
        with NovaAct(starting_page="https://www.amazon.com", user_data_dir=user_data_dir) as nova:
            nova.act("browse to deals of the day")

def check_gmail():
    with with_browserstate(**gmail_config) as user_data_dir:
        with NovaAct(starting_page="https://mail.google.com", user_data_dir=user_data_dir) as nova:
            nova.act("check for new emails")

def check_banking():
    with with_browserstate(**banking_config) as user_data_dir:
        with NovaAct(starting_page="https://mybank.example.com", user_data_dir=user_data_dir) as nova:
            nova.act("check account balance")

if __name__ == "__main__":
    # Each service uses a different session - isolation of cookies and state
    browse_amazon()
    check_gmail()
    check_banking()
    
    # You can also reuse any session later by using the same configuration
    print("Checking Amazon again with same session (retaining cart, login, etc.)")
    browse_amazon() 