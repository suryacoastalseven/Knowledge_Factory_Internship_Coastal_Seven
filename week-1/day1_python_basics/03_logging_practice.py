# 03_logging_practice.py
import logging

# Configuring the logger
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def process_payment(amount: float):
    logging.info(f"Starting payment process for amount: ${amount}")
    
    if amount <= 0:
        logging.error("Invalid payment amount detected!")
        return
        
    if amount > 1000:
        logging.warning("Large transaction detected. Extra verification might be needed.")
        
    # Simulating processing
    logging.debug("Connecting to payment gateway...")
    logging.info("Payment processed successfully!")

# Testing the logging functionality
process_payment(-50)   # Triggers Error
process_payment(1500)  # Triggers Warning
process_payment(200)   # Normal Info/Debug