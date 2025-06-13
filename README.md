# Order Handling System using Flask

A lightweight, Flask-based web application for managing customer orders with comprehensive activity logging.
## 🔗 Live Demo

You can try the app here: [saadnadeem.pythonanywhere.com](https://saadnadeem.pythonanywhere.com)

## Project Overview

This Order Handling System provides a simple yet powerful solution for businesses to track orders from creation to completion. The application offers a clean user interface for managing order data and maintains a detailed audit trail of all system activities.

## Technical Approach

### Core Architecture

The application follows a traditional MVC (Model-View-Controller) pattern:

- **Models**: SQLAlchemy ORM models for Orders and Logs
- **Views**: Jinja2 HTML templates with Bootstrap styling
- **Controllers**: Flask routes handling business logic

### Database Design

Two primary database tables form the foundation of the system:

1. **Orders Table**:
   - `id`: Auto-incremented unique identifier
   - `items`: Number of items in the order
   - `delivery_date`: Expected delivery date
   - `sender_name`: Name of the sender
   - `recipient_name`: Name of the recipient
   - `recipient_address`: Delivery address
   - `status`: Current order status (Ongoing/Completed)

2. **Logs Table**:
   - `id`: Auto-incremented unique identifier
   - `type`: Type of action performed
   - `performer`: Name of the person who performed the action
   - `timestamp`: Date and time when the action was performed

### Key Design Decisions

1. **SQLite Database**: Chosen for simplicity and ease of deployment without requiring a separate database server.

2. **Action Logging**: Every system action is logged with user attribution to maintain a comprehensive audit trail.

3. **Modal Confirmations**: Important actions require confirmation through modal dialogs to prevent accidental operations.

4. **User Attribution**: Without a formal authentication system, the application requests the performer's name for each action to maintain accountability.

5. **Status Tracking**: Orders can be tracked as "Ongoing" or "Completed" with clear visual indicators.

6. **Form Validation**: Client-side and server-side validation ensure data integrity.

## Features

### Order Management

- **Create Orders**: Add new orders with complete details
  - Option to mark orders as completed upon creation
  - Duplicate detection to prevent accidental duplicate entries
  
- **View Orders**: See all orders in a clean tabular format
  - Visual indicators for order status (Ongoing/Completed)
  
- **Edit Orders**: Update any order details as needed
  - All changes are tracked in the log system
  
- **Delete Orders**: Remove orders that are no longer needed
  - Confirmation dialog prevents accidental deletion
  
- **Complete Orders**: Mark orders as delivered/completed
  - Orders can be marked complete either during creation or later

### Activity Logging

- All system activities are automatically logged with:
  - Action type (Create/Update/Delete/Complete)
  - User who performed the action
  - Timestamp of when the action occurred
  
- Logs can be viewed in chronological order (newest first)
  - Provides accountability and audit capabilities

## Installation and Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/username/Order-Handling-System-using-Flask.git
   cd Order-Handling-System-using-Flask
   ```

2. **Set up a virtual environment**
   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment**
   - Windows:
     ```bash
     venv\Scripts\activate
     ```
   - macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

4. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

5. **Run the application**
   ```bash
   python app.py
   ```

6. **Access the application**
   - Open a web browser and go to: `http://127.0.0.1:5000/`

## Usage Guide

### Adding an Order

1. Click the "Add New Order" button on the home page
2. Fill in all required fields:
   - Number of items
   - Delivery date
   - Sender name
   - Recipient name
   - Recipient address
3. Optionally check "Mark Order as Completed" if already fulfilled
4. Enter your name for the activity log
5. Click "Add Order"

### Editing an Order

1. Click the "Edit" button next to the order you wish to modify
2. Update any fields as necessary
3. Enter your name for the activity log
4. Click "Update Order"

### Marking an Order as Completed

1. Click the "Complete" button next to an ongoing order
2. Confirm your action in the dialog
3. Enter your name for the activity log
4. Click "Mark as Completed"

### Deleting an Order

1. Click the "Delete" button next to the order
2. Confirm your action in the dialog
3. Enter your name for the activity log
4. Click "Delete"

### Viewing Activity Logs

1. Click the "View Logs" button on the home page
2. Browse the chronological list of all system activities

## Project Structure

```
Order-Handling-System-using-Flask/
│
├── app.py                 # Main application file with routes and models
├── requirements.txt       # Python dependencies
├── README.md              # Documentation
│
├── instance/              # Database directory
│   └── database.db        # SQLite database file
│
└── templates/             # HTML templates
    ├── view_orders.html   # Main order listing page
    ├── add_order.html     # Form for adding new orders
    ├── edit_order.html    # Form for editing existing orders
    └── logs.html          # Activity log display page
```

## About the Logging System

The current implementation requires users to input their name when performing actions because there is no role-based authentication system in place. This approach was chosen for simplicity while still maintaining accountability for all system activities.

In a production environment with multiple users, implementing proper authentication would be recommended. This would allow:
- Automatic capture of user information for logging
- Different permission levels for different user roles
- Enhanced security for sensitive operations
