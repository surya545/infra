from flask import Flask, request, jsonify
import mysql.connector
from mysql.connector import Error
import uuid
import os
import phonenumbers
from phonenumbers import carrier
from phonenumbers.phonenumberutil import number_type
import logging
import sys

# Configure logging
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Create a logger object
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Added Log Handler
app.logger.addHandler(logging.StreamHandler(sys.stdout))
app.logger.setLevel(logging.INFO)

# Establish a connection to the MySQL database
try:
    db_connection = mysql.connector.connect(
        host=os.environ['DB_HOST'],
        user=os.environ['DB_USER'],
        password=os.environ['DB_PASSWORD'],
        database=os.environ['DB_NAME'],
        port=os.environ['DB_PORT']
    )
    logger.info("Connected to MySQL database successfully.")
except Error as e:
    logger.error("Failed to connect to MySQL database: %s", e)

# Create a cursor object to execute SQL queries
cursor = db_connection.cursor()

# Create the 'messages' table if it does not exist
create_table_query = """
CREATE TABLE IF NOT EXISTS messages (
    id VARCHAR(36) PRIMARY KEY,
    account_id VARCHAR(255) NOT NULL,
    sender_number VARCHAR(20) NOT NULL,
    receiver_number VARCHAR(20) NOT NULL
);
"""
try:
    cursor.execute(create_table_query)
    db_connection.commit()
    logger.info("Table 'messages' created successfully.")
except Error as e:
    logger.error("Failed to create 'messages' table: %s", e)

def is_valid_phone_number(phone_number):
    try:
        # Check if the country code is already included
        if phone_number.startswith('+'):
            pass
        else:
            # Append country code for Indian phone numbers (considering India to be main location)
            phone_number = '+91' + phone_number
        return carrier._is_mobile(number_type(phonenumbers.parse(phone_number)))
    except Exception as e:
        logger.error("Failed to validate phone number: %s", e)
        return False

def validate_args(account_id=None, sender_number=None, receiver_number=None, message_ids=None):
    if account_id is not None and not isinstance(int(account_id), int):
        return False
    if sender_number is not None and not is_valid_phone_number(sender_number):
        return False
    if receiver_number is not None and not is_valid_phone_number(receiver_number):
        return False 
    if message_ids is not None:
        return True
    return True



@app.route('/')
def health():
    return jsonify({'status': "healthy"}), 200



@app.route('/get/messages/<account_id>', methods=['GET'])
def get_messages(account_id):
    if validate_args(account_id=account_id):
        try:
            select_query = f"SELECT * FROM messages WHERE account_id = '{account_id}'"
            cursor.execute(select_query)
            messages = cursor.fetchall()
            return jsonify([{
                'id': message[0],
                'account_id': message[1],
                'sender_number': message[2],
                'receiver_number': message[3]
            } for message in messages]), 200
        except Error as e:
            logger.error("Failed to retrieve messages: %s", e)
            return jsonify({'Error: ': "No Entries Available!"})
    return jsonify({'Error: ': "Check the given fields. account_id(int)"})
    


@app.route('/create', methods=['POST'])
def create_message():
    data = request.json
    message_id = str(uuid.uuid4())
    validity = validate_args(account_id=data['account_id'], sender_number=data['sender_number'], receiver_number=data['receiver_number'])
    if validity:
        try:
            insert_query = f"INSERT INTO messages VALUES ('{message_id}', '{data['account_id']}', '{data['sender_number']}', '{data['receiver_number']}')"
            cursor.execute(insert_query)
            db_connection.commit()
            return jsonify({'message_id': message_id}), 201
        except Error as e:
            logger.error("Failed to insert message: %s", e)
            return jsonify({'Error: ': "Error in data to be dumped!"})
    return jsonify({'Error: ': "Check the given fields. account_id(int), sender_number(valid phone number), receiver_number(valid phone number)"})




@app.route('/search', methods=['GET'])
def search_messages():
    # Extract query parameters
    message_ids = request.args.get('message_id', None)
    sender_numbers = request.args.get('sender_number', None)
    receiver_numbers = request.args.get('receiver_number', None)

    if sender_numbers:
        sender_numbers = sender_numbers.split(',') 
        for number in sender_numbers:
            if not validate_args(sender_number=number.strip()):
                return jsonify({'error': f'Invalid sender number: {number.strip()}'}), 400
            
    if receiver_numbers:
        receiver_numbers = receiver_numbers.split(',') 
        for number in receiver_numbers:
            if not validate_args(receiver_number=number.strip()):
                return jsonify({'error': f'Invalid receiver number: {number.strip()}'}), 400
            
    if message_ids:
        message_ids = message_ids.split(',')
        for msg in message_ids:
            if not validate_args(message_ids==msg.strip()):
                return jsonify({'error': f'Invalid sender number: {msg.strip()}'}), 400
    try:
        filters = {key: request.args.get(key) for key in ['id', 'sender_number', 'receiver_number']}
        conditions = ' AND '.join([f"{key} = '{value}'" for key, value in filters.items() if value])
        select_query = f"SELECT * FROM messages WHERE {conditions}" if conditions else "SELECT * FROM messages"
        cursor.execute(select_query)
        messages = cursor.fetchall()
        return jsonify([{
            'id': message[0],
            'account_id': message[1],
            'sender_number': message[2],
            'receiver_number': message[3]
        } for message in messages]), 200
    except Error as e:
        logger.error("Failed to search messages: %s", e)
        return jsonify({'Error: ': "No Entries Available!"})

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")
