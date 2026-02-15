# config.py

from datetime import time


# ---------------------------------------------------------
# MEAL TIME WINDOWS (ENTRY ALLOWED DURING THIS TIME)
# ---------------------------------------------------------

MEAL_WINDOWS = {
    "breakfast": {
        "start": time(7, 0),   # 7:00 AM
        "end": time(9, 0)      # 9:00 AM
    },
    "lunch": {
        "start": time(12, 0),  # 12:00 PM
        "end": time(14, 0)     # 2:00 PM
    },
    "dinner": {
        "start": time(19, 0),  # 7:00 PM
        "end": time(21, 0)     # 9:00 PM
    }
}


# ---------------------------------------------------------
# BOOKING CUTOFF TIMES (NO BOOKINGS AFTER THIS TIME)
# ---------------------------------------------------------

BOOKING_CUTOFF = {
    "breakfast": time(6, 0),   # 6:00 AM
    "lunch": time(10, 0),      # 10:00 AM
    "dinner": time(16, 0)      # 4:00 PM
}


# ---------------------------------------------------------
# SCHEDULER SETTINGS
# ---------------------------------------------------------

# How often no-show check runs (in seconds)
NO_SHOW_CHECK_INTERVAL = 600  # 10 minutes


# ---------------------------------------------------------
# SYSTEM SETTINGS
# ---------------------------------------------------------

# Allow walk-in buffer (optional)
ALLOW_BUFFER = False
BUFFER_PERCENTAGE = 0.10  # 10% extra capacity (if enabled)


# ---------------------------------------------------------
# DEBUG / DEMO SETTINGS
# ---------------------------------------------------------

# For hackathon demo only
# If True, system can override current time for simulation
ENABLE_TIME_OVERRIDE = False

# Set simulated time manually if override enabled
# Example:
# SIMULATED_TIME = datetime(2026, 1, 1, 12, 30)
SIMULATED_TIME = None
