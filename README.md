
# Automatic Hotel Guest WiFi Management System

The Automatic Hotel Guest WiFi Management System is designed to automate the process of generating and distributing WiFi credentials to guests upon check-in, as well as removing access for guests upon check-out. This system aims to streamline the guest WiFi management process for hotels, ensuring seamless connectivity for guests while maintaining security and efficiency.


## Features

- Automatically detects new guest check-ins and generates unique WiFi credentials.

- Sends personalized messages to guests containing their WiFi credentials via WhatsApp or text message.

- Removes WiFi access for guests upon check-out to maintain security.

- Splits the system into five stages for efficient processing: checking new check-ins, serializing data for WiFi router, sending messages to guests, removing checked-out guests, and deleting WiFi access for checked-out guests.


## Stages

## Stage 1: Checking New Check-Ins
Check for new guest check-ins every 5 minutes.

## Stage 2: Serializing Data for WiFi Router
Serialize data and send it to the WiFi router for credential generation.

## Stage 3: Sending Messages to Guests
Send personalized messages to guests with their WiFi credentials.

## Stage 4: Removing Checked-Out Guests
Remove guests who have checked out from the system.

## Stage 5: Deleting WiFi Access for Checked-Out Guests
Delete WiFi access for checked-out guests.
## Installation

1)  Install the required dependencies:

```bash
  pip install -r requirements.txt
```

2)  Run the main script:

```bash
  python __main__.py
```


    
## Prerequisites

1. Set up WhatsApp messaging token for sending WhatsApp messages  and configure text message API for sending text messages.

2. Set up your PostgreSQL database credentials in the `sql_connector/sql_connect.py` file before running the project.


## Contributing

Contributions are welcome! If you encounter any issues or have suggestions for improvements, please feel free to open an issue or submit a pull request..

