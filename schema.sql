-- Hotel Billing System Database Schema

-- Rooms Table
CREATE TABLE IF NOT EXISTS rooms (
    room_id INTEGER PRIMARY KEY AUTOINCREMENT,
    room_number VARCHAR(10) UNIQUE NOT NULL,
    room_type VARCHAR(50) NOT NULL,
    price_per_night DECIMAL(10, 2) NOT NULL,
    status VARCHAR(20) DEFAULT 'Available',
    capacity INTEGER NOT NULL,
    description TEXT
);

-- Customers Table
CREATE TABLE IF NOT EXISTS customers (
    customer_id INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(100),
    phone VARCHAR(20) NOT NULL,
    id_proof_type VARCHAR(50) NOT NULL,
    id_proof_number VARCHAR(50) NOT NULL,
    address TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Bookings Table
CREATE TABLE IF NOT EXISTS bookings (
    booking_id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_id INTEGER NOT NULL,
    room_id INTEGER NOT NULL,
    check_in_date DATE NOT NULL,
    check_out_date DATE,
    number_of_guests INTEGER NOT NULL,
    booking_status VARCHAR(20) DEFAULT 'Active',
    special_requests TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id),
    FOREIGN KEY (room_id) REFERENCES rooms(room_id)
);

-- Services Table
CREATE TABLE IF NOT EXISTS services (
    service_id INTEGER PRIMARY KEY AUTOINCREMENT,
    service_name VARCHAR(100) NOT NULL,
    service_price DECIMAL(10, 2) NOT NULL,
    description TEXT
);

-- Booking Services Table (Junction table)
CREATE TABLE IF NOT EXISTS booking_services (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    booking_id INTEGER NOT NULL,
    service_id INTEGER NOT NULL,
    quantity INTEGER DEFAULT 1,
    service_date DATE DEFAULT CURRENT_DATE,
    FOREIGN KEY (booking_id) REFERENCES bookings(booking_id),
    FOREIGN KEY (service_id) REFERENCES services(service_id)
);

-- Bills Table
CREATE TABLE IF NOT EXISTS bills (
    bill_id INTEGER PRIMARY KEY AUTOINCREMENT,
    booking_id INTEGER NOT NULL,
    room_charges DECIMAL(10, 2) NOT NULL,
    service_charges DECIMAL(10, 2) DEFAULT 0,
    tax_amount DECIMAL(10, 2) NOT NULL,
    discount DECIMAL(10, 2) DEFAULT 0,
    total_amount DECIMAL(10, 2) NOT NULL,
    payment_status VARCHAR(20) DEFAULT 'Pending',
    payment_method VARCHAR(50),
    bill_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (booking_id) REFERENCES bookings(booking_id)
);

-- Insert Sample Room Data
INSERT INTO rooms (room_number, room_type, price_per_night, capacity, description) VALUES
('101', 'Standard Single', 1500.00, 1, 'Cozy single room with basic amenities'),
('102', 'Standard Double', 2500.00, 2, 'Comfortable double room with city view'),
('103', 'Standard Double', 2500.00, 2, 'Comfortable double room with garden view'),
('201', 'Deluxe Suite', 4500.00, 3, 'Spacious suite with living area and premium amenities'),
('202', 'Deluxe Suite', 4500.00, 3, 'Luxurious suite with balcony'),
('301', 'Executive Suite', 7000.00, 4, 'Premium suite with jacuzzi and panoramic view'),
('302', 'Presidential Suite', 12000.00, 6, 'Ultimate luxury with private terrace and dining area'),
('303', 'Executive Family Suite', 8000.00, 5, 'Large family suite with lounge and two queen beds'),
('401', 'Premium Double', 3200.00, 2, 'Elegant double room with work desk and minibar'),
('402', 'Economy Single', 1300.00, 1, 'Budget-friendly single room with essential amenities');

-- Insert Sample Services
INSERT INTO services (service_name, service_price, description) VALUES
('Room Service - Breakfast', 500.00, 'Continental breakfast delivered to room'),
('Room Service - Lunch', 800.00, 'Lunch meal service'),
('Room Service - Dinner', 1000.00, 'Dinner meal service'),
('Laundry Service', 300.00, 'Per piece laundry service'),
('Spa & Massage', 2000.00, 'One hour spa and massage session'),
('Airport Pickup', 1500.00, 'Airport to hotel transfer'),
('Mini Bar', 500.00, 'Mini bar consumption'),
('Extra Bed', 800.00, 'Additional bed in room'),
('Wi-Fi Premium', 200.00, 'High-speed internet access per day'),
('Conference Room', 5000.00, 'Conference room rental per hour');

-- Create Indexes for Performance Optimization
CREATE INDEX IF NOT EXISTS idx_rooms_status ON rooms(status);
CREATE INDEX IF NOT EXISTS idx_bookings_customer_id ON bookings(customer_id);
CREATE INDEX IF NOT EXISTS idx_bookings_room_id ON bookings(room_id);
CREATE INDEX IF NOT EXISTS idx_bookings_status ON bookings(booking_status);
CREATE INDEX IF NOT EXISTS idx_bookings_check_in ON bookings(check_in_date);
CREATE INDEX IF NOT EXISTS idx_bookings_check_out ON bookings(check_out_date);
CREATE INDEX IF NOT EXISTS idx_booking_services_booking_id ON booking_services(booking_id);
CREATE INDEX IF NOT EXISTS idx_booking_services_service_id ON booking_services(service_id);
CREATE INDEX IF NOT EXISTS idx_bills_booking_id ON bills(booking_id);
CREATE INDEX IF NOT EXISTS idx_bills_status ON bills(payment_status);
CREATE INDEX IF NOT EXISTS idx_bills_date ON bills(bill_date);
CREATE INDEX IF NOT EXISTS idx_customers_phone ON customers(phone);
