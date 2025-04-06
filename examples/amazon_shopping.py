"""
Example demonstrating how to maintain login state and shopping carts across multiple runs
when automating Amazon shopping tasks.
"""

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
    """Login to Amazon and add an item to cart."""
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
    """Complete the purchase using the persisted session."""
    with amazon_session as user_data_dir:
        with NovaAct(starting_page="https://www.amazon.com/cart", user_data_dir=user_data_dir, clone_user_data_dir=False) as nova:
            # User is still logged in and cart is preserved from previous session
            nova.act("verify the item is in cart")
            nova.act("proceed to checkout")
            nova.act("select shipping address")
            nova.act("select payment method")
            nova.act("place order")
            print("🎉 Purchase completed successfully")

if __name__ == "__main__":
    print("Step 1: Login and add item to cart")
    amazon_login_and_add_to_cart()
    
    input("Press Enter to continue with purchase...")
    
    print("Step 2: Complete the purchase")
    amazon_complete_purchase() 