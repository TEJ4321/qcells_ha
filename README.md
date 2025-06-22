# QCells Energy for Home Assistant
<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="custom_components/qcells_energy/dark_logo.png">
    <source media="(prefers-color-scheme: light)" srcset="custom_components/qcells_energy/logo.png">
    <img alt="Qcells Logo" src="custom_components/qcells_energy/logo.png" width="400"/>
  </picture>
</p>

## Description
QCells Energy for Home Assistant is a custom integration that allows you to monitor and visualize data from your Q Cells HS4, HS5, and similar systems directly within Home Assistant. The integration communicates with your Q.VOLT inverter over your local network, providing real-time access to key solar, battery, inverter, and grid statistics.

This is for owners of Q Cells systems that have built-in networking functionality via a WiFi dongle or an ethernet port inside the Q.VOLT inverters.

- I have not confirmed whether this works with the Solax modbus integration capable Q.VOLT inverters.

## Features:

- Supports Q Cells inverters with built-in WiFi (dongle) or Ethernet.
- Automatically discovers and creates sensors for battery, solar (PV), grid, inverter, and system status.
- Offers both "simple" and "detailed" integration modes, letting you choose between just seeing essential-ish information or a full detailed view of a lot of the data possible to gather from the system.
- Virtual energy sensors automatically integrate power readings over time for energy tracking.
- Customizable polling interval and display precision.
- Device and sensor icons for a clear, user-friendly dashboard.
- No cloud required—your data stays local.

## Pre-Requisites
1. **Ensure your Q.VOLT inverter is connected to your network** via WiFi or Ethernet. You do NOT need to have internet access, but you still need to be able to access your device on your network **by finding its IP address**.
    - You can find its IP by going into your router settings and checking what devices are connected. Alternatively, you can use apps like Fing on a mobile device to search through devices on your network.
2. **Navigate to https://your-inverter-ip:7000/** and check that you see the Q.OMMAND installer portal shows up.
    - You might need to accept that the certificate is not trusted in your browser.
3. **Check that you can login to the installer portal** if you know the password (it's usually the last 4 digits of your inverter serial number).
    - If the password does not work, click forgot password, input the full serial number of your inverter and reset it to whatever you like. 
    - You should be able to find the serial number of your Q.Volt inverter directly on it (usually on a sticker with a QR code on it).

## Installation
### Pre-Install
Get the Home Assistant Community Store (HACS) at https://hacs.xyz/. This makes installation and update tracking of this integration significantly easier than trying to do things manually.
    
*Alternatively, if you are comfortable using the file editing tools in home assistant, you can put the contents of the custom_components folder within this repo into your home assistant config/custom_components folder.*

### Installing this integration
1. Add this repo to HACS, or click the blue button:

    [![Open your Home Assistant instance and open a repository inside the Home Assistant Community Store.](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=%40TEJ4321&category=Integration&repository=https%3A%2F%2Fgithub.com%2FTEJ4321%2Fqcells_ha)

2. Install the Qcells Energy custom component and Restart home assistant
3. Go to Settings->Devices & services->ADD INTEGRATION and add ***Qcells Energy***.
4. Configure it based on the IP address of your Q.VOLT inverter. 



This project would not have been possible without the information contained within this forum discussion:
https://community.home-assistant.io/t/hanwha-q-cells/446745/41

Special thanks to feldhuegel (https://community.home-assistant.io/u/feldhuegel) and saintmatt81 (https://community.home-assistant.io/u/saintmatt81) on that page for their insightful comments about accessing and using the Qcells installer portal and its routes.
