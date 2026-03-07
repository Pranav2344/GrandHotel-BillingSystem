import sqlite3
from datetime import datetime, date
import os

DATABASE_NAME = 'hotel_billing.db'

DEFAULT_ROOMS = [
    ('101', 'Standard Single', 1500.00, 1, 'Cozy single room with basic amenities'),
    ('102', 'Standard Double', 2500.00, 2, 'Comfortable double room with city view'),
    ('103', 'Standard Double', 2500.00, 2, 'Comfortable double room with garden view'),
    ('201', 'Deluxe Suite', 4500.00, 3, 'Spacious suite with living area and premium amenities'),
    ('202', 'Deluxe Suite', 4500.00, 3, 'Luxurious suite with balcony'),
    ('301', 'Executive Suite', 7000.00, 4, 'Premium suite with jacuzzi and panoramic view'),
    ('302', 'Presidential Suite', 12000.00, 6, 'Ultimate luxury with private terrace and dining area'),
    ('303', 'Executive Family Suite', 8000.00, 5, 'Large family suite with lounge and two queen beds'),
    ('401', 'Premium Double', 3200.00, 2, 'Elegant double room with work desk and minibar'),
    ('402', 'Economy Single', 1300.00, 1, 'Budget-friendly single room with essential amenities')
]

def get_db_connection():
    """Create and return a database connection with optimized settings"""
    conn = sqlite3.connect(DATABASE_NAME, timeout=10)
    conn.row_factory = sqlite3.Row
    # Enable query optimization
    conn.execute('PRAGMA journal_mode=WAL')  # Write-Ahead Logging
    conn.execute('PRAGMA synchronous=NORMAL')  # Faster writes
    conn.execute('PRAGMA cache_size=-64000')  # 64MB cache
    conn.execute('PRAGMA temp_store=MEMORY')  # Use memory for temp storage
    return conn

def init_database():
    """Initialize the database with schema"""
    if not os.path.exists(DATABASE_NAME):
        conn = get_db_connection()
        with open('schema.sql', 'r') as f:
            conn.executescript(f.read())
        conn.commit()
        conn.close()
        print("Database initialized successfully!")
    else:
        print("Database already exists!")

    added_rooms = ensure_default_rooms()
    if added_rooms:
        print(f"Added {added_rooms} room(s) to match default inventory of 10 rooms.")

def ensure_default_rooms():
    """Ensure all default room numbers exist, including the new 10-room baseline."""
    conn = get_db_connection()
    existing_room_numbers = {
        row['room_number'] for row in conn.execute('SELECT room_number FROM rooms').fetchall()
    }

    missing_rooms = [room for room in DEFAULT_ROOMS if room[0] not in existing_room_numbers]
    if missing_rooms:
        conn.executemany(
            'INSERT INTO rooms (room_number, room_type, price_per_night, capacity, description) VALUES (?, ?, ?, ?, ?)',
            missing_rooms
        )
        conn.commit()

    conn.close()
    return len(missing_rooms)

def get_available_rooms():
    """Get all available rooms"""
    conn = get_db_connection()
    rooms = conn.execute('SELECT * FROM rooms WHERE status = "Available"').fetchall()
    conn.close()
    return rooms

def get_all_rooms():
    """Get all rooms"""
    conn = get_db_connection()
    rooms = conn.execute('SELECT * FROM rooms ORDER BY room_number').fetchall()
    conn.close()
    return rooms

def get_room_by_id(room_id):
    """Get room by ID"""
    conn = get_db_connection()
    room = conn.execute('SELECT * FROM rooms WHERE room_id = ?', (room_id,)).fetchone()
    conn.close()
    return room

def add_customer(first_name, last_name, email, phone, id_proof_type, id_proof_number, address):
    """Add a new customer"""
    conn = get_db_connection()
    cursor = conn.execute(
        'INSERT INTO customers (first_name, last_name, email, phone, id_proof_type, id_proof_number, address) VALUES (?, ?, ?, ?, ?, ?, ?)',
        (first_name, last_name, email, phone, id_proof_type, id_proof_number, address)
    )
    customer_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return customer_id

def create_booking(customer_id, room_id, check_in_date, number_of_guests, special_requests=''):
    """Create a new booking"""
    conn = get_db_connection()
    cursor = conn.execute(
        'INSERT INTO bookings (customer_id, room_id, check_in_date, number_of_guests, special_requests) VALUES (?, ?, ?, ?, ?)',
        (customer_id, room_id, check_in_date, number_of_guests, special_requests)
    )
    booking_id = cursor.lastrowid
    
    # Update room status
    conn.execute('UPDATE rooms SET status = "Occupied" WHERE room_id = ?', (room_id,))
    conn.commit()
    conn.close()
    return booking_id

def get_active_bookings():
    """Get all active bookings"""
    conn = get_db_connection()
    bookings = conn.execute('''
        SELECT b.*, c.first_name, c.last_name, c.phone, r.room_number, r.room_type, r.price_per_night
        FROM bookings b
        JOIN customers c ON b.customer_id = c.customer_id
        JOIN rooms r ON b.room_id = r.room_id
        WHERE b.booking_status = "Active"
        ORDER BY b.check_in_date DESC
    ''').fetchall()
    conn.close()
    return bookings

def get_booking_by_id(booking_id):
    """Get booking details by ID"""
    conn = get_db_connection()
    booking = conn.execute('''
        SELECT b.*, c.*, r.room_number, r.room_type, r.price_per_night
        FROM bookings b
        JOIN customers c ON b.customer_id = c.customer_id
        JOIN rooms r ON b.room_id = r.room_id
        WHERE b.booking_id = ?
    ''', (booking_id,)).fetchone()
    conn.close()
    return booking

def get_all_services():
    """Get all available services"""
    conn = get_db_connection()
    services = conn.execute('SELECT * FROM services ORDER BY service_name').fetchall()
    conn.close()
    return services

def add_service_to_booking(booking_id, service_id, quantity=1):
    """Add a service to a booking"""
    conn = get_db_connection()
    conn.execute(
        'INSERT INTO booking_services (booking_id, service_id, quantity) VALUES (?, ?, ?)',
        (booking_id, service_id, quantity)
    )
    conn.commit()
    conn.close()

def get_booking_services(booking_id):
    """Get all services for a booking"""
    conn = get_db_connection()
    services = conn.execute('''
        SELECT bs.*, s.service_name, s.service_price
        FROM booking_services bs
        JOIN services s ON bs.service_id = s.service_id
        WHERE bs.booking_id = ?
    ''', (booking_id,)).fetchall()
    conn.close()
    return services

def calculate_bill(booking_id, check_out_date):
    """Calculate bill for a booking"""
    conn = get_db_connection()
    booking = get_booking_by_id(booking_id)
    
    if not booking:
        return None
    
    # Calculate number of nights
    check_in = datetime.strptime(booking['check_in_date'], '%Y-%m-%d').date()
    check_out = datetime.strptime(check_out_date, '%Y-%m-%d').date()
    nights = (check_out - check_in).days
    if nights <= 0:
        nights = 1
    
    # Calculate room charges (price per person per night × nights × number of guests)
    room_charges = booking['price_per_night'] * nights * booking['number_of_guests']
    
    # Calculate service charges
    services = get_booking_services(booking_id)
    service_charges = sum(s['service_price'] * s['quantity'] for s in services)
    
    # Calculate tax (12% GST)
    subtotal = room_charges + service_charges
    tax_amount = subtotal * 0.12
    
    # Total amount
    total_amount = subtotal + tax_amount
    
    return {
        'nights': nights,
        'room_charges': room_charges,
        'service_charges': service_charges,
        'subtotal': subtotal,
        'tax_amount': tax_amount,
        'total_amount': total_amount
    }

def create_bill(booking_id, room_charges, service_charges, tax_amount, discount, total_amount, payment_method):
    """Create a bill for checkout"""
    conn = get_db_connection()
    cursor = conn.execute(
        'INSERT INTO bills (booking_id, room_charges, service_charges, tax_amount, discount, total_amount, payment_status, payment_method) VALUES (?, ?, ?, ?, ?, ?, ?, ?)',
        (booking_id, room_charges, service_charges, tax_amount, discount, total_amount, 'Paid', payment_method)
    )
    bill_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return bill_id

def checkout_booking(booking_id, check_out_date, room_id):
    """Process checkout"""
    conn = get_db_connection()
    conn.execute(
        'UPDATE bookings SET check_out_date = ?, booking_status = "Completed" WHERE booking_id = ?',
        (check_out_date, booking_id)
    )
    conn.execute('UPDATE rooms SET status = "Available" WHERE room_id = ?', (room_id,))
    conn.commit()
    conn.close()

def get_bill_by_id(bill_id):
    """Get bill details"""
    conn = get_db_connection()
    bill = conn.execute('''
        SELECT b.*, bk.booking_id, bk.check_in_date, bk.check_out_date, bk.number_of_guests,
               c.first_name, c.last_name, c.email, c.phone, c.address, c.id_proof_type, c.id_proof_number,
               r.room_number, r.room_type, r.price_per_night
        FROM bills b
        JOIN bookings bk ON b.booking_id = bk.booking_id
        JOIN customers c ON bk.customer_id = c.customer_id
        JOIN rooms r ON bk.room_id = r.room_id
        WHERE b.bill_id = ?
    ''', (bill_id,)).fetchone()
    conn.close()
    return bill

def get_all_bills():
    """Get all bills"""
    conn = get_db_connection()
    bills = conn.execute('''
        SELECT b.*, c.first_name, c.last_name, r.room_number, bk.check_in_date, bk.check_out_date
        FROM bills b
        JOIN bookings bk ON b.booking_id = bk.booking_id
        JOIN customers c ON bk.customer_id = c.customer_id
        JOIN rooms r ON bk.room_id = r.room_id
        ORDER BY b.bill_date DESC
    ''').fetchall()
    conn.close()
    return bills
