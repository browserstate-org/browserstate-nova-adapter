"""
Example showing how to manage multiple browser sessions for different services.
Each service gets its own isolated session with separate cookies and state.
"""

from browserstate_nova_adapter import BrowserStateSession
from nova_act import NovaAct

# Create sessions for different services
amazon_session = BrowserStateSession(
    user_id="shopper",
    session_id="amazon-session",
    provider="local",
    storage_path="./browser_sessions/amazon"
)

gmail_session = BrowserStateSession(
    user_id="email-user",
    session_id="gmail-session",
    provider="local",
    storage_path="./browser_sessions/gmail"
)

banking_session = BrowserStateSession(
    user_id="bank-user",
    session_id="banking-session",
    provider="local",
    storage_path="./browser_sessions/banking"
)

def browse_amazon():
    """Browse Amazon with persistent session."""
    with amazon_session as user_data_dir:
        with NovaAct(starting_page="https://amazon.com", user_data_dir=user_data_dir, clone_user_data_dir=False) as nova:
            nova.act("search for products")
            # Amazon session state is preserved

def check_gmail():
    """Check Gmail with persistent session."""
    with gmail_session as user_data_dir:
        with NovaAct(starting_page="https://gmail.com", user_data_dir=user_data_dir, clone_user_data_dir=False) as nova:
            nova.act("check inbox")
            # Gmail session state is preserved

def check_banking():
    """Check banking with persistent session."""
    with banking_session as user_data_dir:
        with NovaAct(starting_page="https://bank.com", user_data_dir=user_data_dir, clone_user_data_dir=False) as nova:
            nova.act("check balance")
            # Banking session state is preserved

if __name__ == "__main__":
    # Each session maintains its own cookies and state
    browse_amazon()  # Uses Amazon session
    check_gmail()    # Uses Gmail session
    check_banking()  # Uses banking session 