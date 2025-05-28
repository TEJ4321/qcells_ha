import sys
import os
import asyncio
if sys.platform.startswith("win"):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
from datetime import timedelta
from unittest.mock import MagicMock
from custom_components.qcells_energy.coordinator import QcellsDataUpdateCoordinator

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Mock HomeAssistant object
mock_hass = MagicMock()

# Replace with your actual device IP and password for real testing
ip = "192.168.0.162"
password = "invertertest1!"
update_interval = timedelta(seconds=5)

async def test_login():
    coordinator = QcellsDataUpdateCoordinator(mock_hass, ip, password, update_interval)
    try:
        coordinator._login()
        print("Login successful")
    except Exception as e:
        print(f"Login failed: {e}")

async def test_update_data():
    coordinator = QcellsDataUpdateCoordinator(mock_hass, ip, password, update_interval)
    try:
        data = await coordinator._async_update_data()
        print("Data:", data)
    except Exception as e:
        print(f"Update failed: {e}")

if __name__ == "__main__":
    print("\nTesting login...\n===========================================\n")
    asyncio.run(test_login())
    # Or to test update:
    print("\nTesting data update...\n===========================================\n")
    asyncio.run(test_update_data())