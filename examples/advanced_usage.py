import logging
import sys
from browserstate_nova_adapter import with_browserstate, mount_browserstate, unmount_browserstate
from nova_act import NovaAct

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger("browserstate-nova-example")

# Example 1: Using with_browserstate with robust error handling
def run_with_context_manager():
    try:
        with with_browserstate(
            user_id="demo-user",
            session_id="robust-session",
            provider="redis",
            redis_options={
                "host": "localhost",
                "port": 6379,
                "db": 0,
                "key_prefix": "browser:",
                "ttl": 86400  # 24 hours
            }
        ) as user_data_dir:
            logger.info(f"Browser session mounted at: {user_data_dir}")
            
            try:
                with NovaAct(starting_page="https://example.com", user_data_dir=user_data_dir) as nova:
                    # First task
                    logger.info("Executing first task")
                    nova.act("search for 'browser automation'")
                    
                    # Second task
                    logger.info("Executing second task")
                    nova.act("click on the first result")
                    
                    # Third task
                    logger.info("Executing third task")
                    nova.act("scroll down")
            except Exception as e:
                logger.error(f"Error during Nova automation: {e}")
                # The with_browserstate context manager will still handle cleanup
    except Exception as e:
        logger.critical(f"Error with browser session: {e}")

# Example 2: Manual mounting with separate sessions
def run_with_manual_mounting():
    # First mount the session to ensure we have it
    try:
        user_data_dir = mount_browserstate(
            user_id="manual-user",
            session_id="multi-session",
            provider="local",
            storage_path="./browser_storage"
        )
        logger.info(f"Browser session mounted at: {user_data_dir}")
        
        # First session
        try:
            with NovaAct(starting_page="https://example.com", user_data_dir=user_data_dir) as nova:
                logger.info("Starting first session")
                nova.act("navigate to login page")
                nova.act("login with username and password")
                logger.info("First session completed")
        except Exception as e:
            logger.error(f"Error in first session: {e}")
        
        # Second session (reusing the same mounted session)
        try:
            with NovaAct(starting_page="https://dashboard.example.com", user_data_dir=user_data_dir) as nova:
                logger.info("Starting second session")
                # We're already logged in because the session persists
                nova.act("check notifications")
                nova.act("log out")
                logger.info("Second session completed")
        except Exception as e:
            logger.error(f"Error in second session: {e}")
        
    except Exception as e:
        logger.critical(f"Error mounting browser session: {e}")
    finally:
        # Always clean up
        try:
            unmount_browserstate()
            logger.info("Browser session unmounted successfully")
        except Exception as e:
            logger.error(f"Error unmounting browser session: {e}")

if __name__ == "__main__":
    logger.info("Starting example with context manager")
    run_with_context_manager()
    
    logger.info("\nStarting example with manual mounting")
    run_with_manual_mounting()
    
    logger.info("Examples completed") 