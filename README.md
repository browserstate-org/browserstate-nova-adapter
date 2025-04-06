# 🧩 browserstate-nova-adapter

This package makes it easy to use [BrowserState](https://github.com/browserstate-org/browserstate) with [Amazon Nova Act](https://labs.amazon.science/blog/nova-act). It ensures persistent browser memory across Nova sessions by mounting and unmounting full `user_data_dir` browser state.

> Store and restore cookies, localStorage, IndexedDB, and more — across runs, machines, and cloud environments.

---

## 📦 Install (Coming Soon)

> This package is under active development and will be published to PyPI soon. In the meantime, clone or install directly from source if you're contributing or testing.

---

## 🚀 Quickstart Example (Nova + BrowserState)

```python
from browserstate_nova_adapter import BrowserStateSession
from nova_act import NovaAct

# Create and use a browser state session
session = BrowserStateSession(
    user_id="demo-user",
    session_id="nova-session",
    provider="redis",
    redis_options={"host": "localhost", "port": 6379}
)

with session as user_data_dir:
    with NovaAct(starting_page="https://example.com", user_data_dir=user_data_dir, clone_user_data_dir=False) as nova:
        nova.act("search for something")
```

---

## 🔧 Manual Usage

```python
from browserstate_nova_adapter import BrowserStateSession
from nova_act import NovaAct

# Create a session
session = BrowserStateSession(
    user_id="demo",
    session_id="session1",
    provider="local"
)

# Mount the session
user_data_dir = session.mount()

try:
    with NovaAct(starting_page="https://example.com", user_data_dir=user_data_dir, clone_user_data_dir=False) as nova:
        nova.act("search for something")
finally:
    # Always unmount when done
    session.unmount()
```

---

## 🌐 Multiple Browser States Example

You can manage multiple browser states for different services, each with its own session:

```python
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

# Use Amazon session
def browse_amazon():
    with amazon_session as user_data_dir:
        with NovaAct(starting_page="https://amazon.com", user_data_dir=user_data_dir, clone_user_data_dir=False) as nova:
            nova.act("search for products")
            # Amazon session state is preserved

# Use Gmail session
def check_gmail():
    with gmail_session as user_data_dir:
        with NovaAct(starting_page="https://gmail.com", user_data_dir=user_data_dir, clone_user_data_dir=False) as nova:
            nova.act("check inbox")
            # Gmail session state is preserved

# Each session maintains its own cookies and state
browse_amazon()  # Uses Amazon session
check_gmail()    # Uses Gmail session
```

---

## 🔐 Authentication and Session Management

### Setting Up Authentication

You can set up authentication for your websites by creating a persistent session:

```python
import os
from browserstate_nova_adapter import BrowserStateSession
from nova_act import NovaAct

# Create a persistent session
auth_session = BrowserStateSession(
    user_id="auth-user",
    session_id="auth-session",
    provider="local",
    storage_path="./browser_sessions/auth",
    temp_dir="./temp/auth"
)

# Set up authentication
with auth_session as user_data_dir:
    with NovaAct(
        starting_page="https://example.com/login",
        user_data_dir=user_data_dir,
        clone_user_data_dir=False
    ) as nova:
        input("Log into your websites, then press enter...")

print(f"Authentication data saved to {auth_session.temp_dir}")
```

### Handling Sensitive Information

For secure handling of passwords and sensitive data:

```python
from getpass import getpass
from browserstate_nova_adapter import BrowserStateSession
from nova_act import NovaAct

def secure_login():
    with auth_session as user_data_dir:
        with NovaAct(
            starting_page="https://example.com/login",
            user_data_dir=user_data_dir,
            clone_user_data_dir=False
        ) as nova:
            # Enter username securely using Playwright
            nova.act("click on the email field")
            nova.page.keyboard.type(getpass("Enter email: "))
            
            # Enter password securely using Playwright
            nova.act("click on the password field")
            nova.page.keyboard.type(getpass())
            
            # Complete login
            nova.act("click sign in button")
```

---

## 🌍 Storage Providers
- Local (default)
- Redis (with TTL, keyPrefix)
- AWS S3 *(experimental)*
- Google Cloud Storage *(experimental)*

---

## 🔗 Related Projects
- [BrowserState Core](https://github.com/browserstate-org/browserstate)
- [Nova Act](https://labs.amazon.science/blog/nova-act)

---

## 🤝 Contributing
PRs welcome — especially if you're using BrowserState with other automation tools.

---

## ⚖️ License
MIT

---

## 🧠 Why this exists
Nova sessions reset browser context every run.
This adapter makes Nova Act automations behave like real users — with memory.
It wraps `BrowserState`'s mounting logic, handles cleanup, and supports Redis/S3/local/gcs.

## 🌐 Practical Example: Amazon Shopping with Session Persistence

This example demonstrates how to maintain login state and shopping carts across multiple runs when automating Amazon shopping tasks.

```python
from browserstate_nova_adapter import BrowserStateSession
from nova_act import NovaAct
import os
from getpass import getpass

# Create a persistent session for Amazon
amazon_session = BrowserStateSession(
    user_id="amazon-shopper",
    session_id="amazon-shopping-session",
    provider="local",
    storage_path="./browser_sessions"
)

# Step 1: Login to Amazon and add item to cart
def amazon_login_and_add_to_cart():
    with amazon_session as user_data_dir:
        with NovaAct(starting_page="https://www.amazon.com", user_data_dir=user_data_dir, clone_user_data_dir=False) as nova:
            # Login to Amazon securely
            nova.act("click on sign in")
            nova.act("click on email field")
            nova.page.keyboard.type(getpass("Enter Amazon email: "))  # Secure email entry
            nova.act("click continue")
            nova.act("enter password field")
            nova.page.keyboard.type(getpass())  # Secure password entry
            nova.act("click sign in")
            
            # Search for product
            nova.act("search for wireless headphones")
            nova.act("click on the first result")
            
            # Add to cart
            nova.act("add to cart")
            print("✅ Successfully logged in and added item to cart")

# Step 2: Later, complete the purchase using the same session (persisted cart and login)
def amazon_complete_purchase():
    with amazon_session as user_data_dir:
        with NovaAct(starting_page="https://www.amazon.com/cart", user_data_dir=user_data_dir, clone_user_data_dir=False) as nova:
            # User is still logged in and cart is preserved from previous session
            nova.act("verify the item is in cart")
            nova.act("proceed to checkout")
            nova.act("select shipping address")
            nova.act("select payment method")
            nova.act("place order")
            print("🎉 Purchase completed successfully")

# Run the shopping process in two separate steps
if __name__ == "__main__":
    print("Step 1: Login and add item to cart")
    amazon_login_and_add_to_cart()
    
    input("Press Enter to continue with purchase...")
    
    print("Step 2: Complete the purchase")
    amazon_complete_purchase()
```

This example demonstrates how BrowserState preserves:
- Login sessions (cookies and authentication)
- Shopping cart contents
- User preferences and settings
- Form data and autofill information

All of this state persists between separate runs of your automation, making the Nova experience more like a real human user.
