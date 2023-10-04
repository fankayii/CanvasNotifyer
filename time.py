from datetime import datetime
import pytz

def convert_utc_to_pst(utc_time_str):
    # Parse the UTC time string to a datetime object
    utc_time = datetime.strptime(utc_time_str, "%Y-%m-%dT%H:%M:%SZ")
    
    # Localize the time to UTC
    utc_time = pytz.utc.localize(utc_time)
    
    # Convert to Pacific Time
    pst = pytz.timezone('America/Los_Angeles')
    pst_time = utc_time.astimezone(pst)
    
    # Return the PST time as a string
    return pst_time.strftime("%Y-%m-%d %H:%M:%S %Z")

# Test the function
utc_time_str = "2023-09-12T18:59:59Z"
pst_time_str = convert_utc_to_pst(utc_time_str)
print(f"The time in PST is: {pst_time_str}")
