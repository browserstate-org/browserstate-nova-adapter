# 🧩 browserstate-nova-adapter

This package makes it easy to use [BrowserState](https://github.com/browserstate-org/browserstate) with [Amazon Nova Act](https://labs.amazon.science/blog/nova-act). It ensures persistent browser memory across Nova sessions by mounting and unmounting full `user_data_dir` browser state.

> Store and restore cookies, localStorage, IndexedDB, and more — across runs, machines, and cloud environments.

---


## 📦 Install (Coming Soon)

> This package is under active development and will be published to PyPI soon. In the meantime, clone or install directly from source if you're contributing or testing.

---

---

## 🚀 Quickstart Example (Nova + BrowserState)

```python
from browserstate_nova_adapter import with_browserstate
from nova_act import NovaAct

with with_browserstate(
    user_id="demo-user",
    session_id="nova-session",
    provider="redis",  # or 'local', 's3', 'gcs'
    redis_options={"host": "localhost", "port": 6379}
) as user_data_dir:
    with NovaAct(starting_page="https://example.com", user_data_dir=user_data_dir) as nova:
        nova.act("search for something")
```

---

## 🔧 Manual Usage

```python
from browserstate_nova_adapter import mount_browserstate, unmount_browserstate
from nova_act import NovaAct

user_data_dir = mount_browserstate(
    user_id="demo",
    session_id="session1",
    provider="local"
)

try:
    with NovaAct(starting_page="https://example.com", user_data_dir=user_data_dir) as nova:
        nova.act("search for something")
finally:
    unmount_browserstate()
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
from browserstate_nova_adapter import with_browserstate, create_session_config
from nova_act import NovaAct

# Create a reusable session configuration
amazon_config = create_session_config(
    user_id="amazon-shopper",
    session_id="amazon-shopping-session",
    provider="local",
    storage_path="./browser_sessions"
)

# Step 1: Login to Amazon and add item to cart
def amazon_login_and_add_to_cart():
    with with_browserstate(**amazon_config) as user_data_dir:
        with NovaAct(starting_page="https://www.amazon.com", user_data_dir=user_data_dir) as nova:
            # Login to Amazon
            nova.act("click on sign in")
            nova.act("enter email address")
            nova.act("click continue")
            nova.act("enter password")
            nova.act("click sign in")
            
            # Search for product
            nova.act("search for wireless headphones")
            nova.act("click on the first result")
            
            # Add to cart
            nova.act("add to cart")
            print("✅ Successfully logged in and added item to cart")
            # Session will be automatically saved when exiting the context manager

# Step 2: Later, complete the purchase using the same session (persisted cart and login)
def amazon_complete_purchase():
    with with_browserstate(**amazon_config) as user_data_dir:
        with NovaAct(starting_page="https://www.amazon.com/cart", user_data_dir=user_data_dir) as nova:
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
