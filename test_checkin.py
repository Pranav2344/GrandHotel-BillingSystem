#!/usr/bin/env python
"""Test check-in functionality"""
import sqlite3
import sys

try:
    conn = sqlite3.connect('hotel_billing.db')
    conn.row_factory = sqlite3.Row
    
    # Test available rooms
    rooms = conn.execute('SELECT * FROM rooms WHERE status = "Available" LIMIT 1').fetchall()
    if rooms:
        room = rooms[0]
        print(f"✓ Database OK - Found room: {room['room_number']} (Capacity: {room['capacity']})")
    else:
        print("✗ No available rooms found")
        sys.exit(1)
    
    # Test customer insertion
    cursor = conn.execute(
        'INSERT INTO customers (first_name, last_name, email, phone, id_proof_type, id_proof_number, address) VALUES (?, ?, ?, ?, ?, ?, ?)',
        ('Test', 'Guest', 'test@example.com', '9999999999', 'Aadhar Card', '1234-5678-9012', 'Test Address')
    )
    customer_id = cursor.lastrowid
    print(f"✓ Customer insertion OK - ID: {customer_id}")
    
    # Test booking creation
    cursor = conn.execute(
        'INSERT INTO bookings (customer_id, room_id, check_in_date, number_of_guests, booking_status) VALUES (?, ?, ?, ?, ?)',
        (customer_id, room['room_id'], '2026-03-06', 1, 'Active')
    )
    booking_id = cursor.lastrowid
    conn.commit()
    print(f"✓ Booking creation OK - ID: {booking_id}")
    
    # Clean up test data
    conn.execute('DELETE FROM bookings WHERE booking_id = ?', (booking_id,))
    conn.execute('DELETE FROM customers WHERE customer_id = ?', (customer_id,))
    conn.commit()
    conn.close()
    
    print("\n✓ All check-in operations working correctly!")
    
except Exception as e:
    print(f"✗ Error: {str(e)}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
