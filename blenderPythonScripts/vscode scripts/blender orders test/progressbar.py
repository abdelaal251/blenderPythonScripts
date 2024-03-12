import time
from tqdm import tqdm

# Create a list to iterate over
items = list(range(10))

# Initialize tqdm with the iterable and set the total parameter
with tqdm(total=len(items), desc="Processing", unit="item") as pbar:
    for item in items:
        # Simulate some processing time
        time.sleep(0.5)
        # Update the progress bar
        pbar.update(1)
        
# Optional: Add a completion message
print("Processing complete!")
