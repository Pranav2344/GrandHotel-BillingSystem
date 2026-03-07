# 🏨 Professional Hotel Billing System

A modern, industry-ready hotel management and billing system built with Flask, featuring an attractive and professional UI/UX design.

## ✨ Features

### 🎨 Professional Design
- **Modern UI/UX**: Clean, intuitive interface with gradient backgrounds and smooth animations
- **Responsive Design**: Fully mobile-friendly and adapts to all screen sizes
- **Custom Color Scheme**: Professional purple gradient theme with carefully selected colors
- **Smooth Animations**: Fade-in effects, hover states, and transition animations
- **Glass Morphism**: Modern frosted-glass effects on cards and components
- **Custom Scrollbar**: Styled scrollbar matching the theme

### 🏨 Core Functionality
- **Dashboard**: Real-time overview of hotel statistics and active bookings
- **Room Management**: Visual catalog of all rooms with status indicators
- **Guest Check-In**: Comprehensive form for new guest registration
- **Guest Check-Out**: Process checkout and generate final bills
- **Billing System**: Professional invoice generation with detailed breakdowns
- **Service Management**: Add additional services to guest bookings

### 💎 Professional Features
- **Scroll-to-Top Button**: Smooth scrolling navigation enhancement
- **Active Navigation Highlighting**: Current page indication in navbar
- **Form Validation**: Client-side validation with visual feedback
- **Auto-hiding Alerts**: Dismissible notifications with smooth animations
- **Print-Friendly Invoices**: Optimized invoice printing layout
- **Loading States**: Professional loading animations
- **Status Badges**: Color-coded badges for different states

### 🎯 UI Components
- **Stat Cards**: Animated dashboard statistics with hover effects
- **Room Cards**: Beautiful room display with gradient headers
- **Data Tables**: Professional tables with hover states and sorting
- **Forms**: Modern form inputs with focus states and validation
- **Buttons**: Gradient buttons with ripple effects
- **Invoices**: Professional invoice layout with company branding

## 🚀 Technology Stack

- **Backend**: Python Flask
- **Database**: SQLite
- **Frontend**: HTML5, CSS3, JavaScript (Vanilla)
- **Fonts**: Inter (Google Fonts)
- **Icons**: Emoji-based (cross-platform compatible)

## 📦 Installation

1. **Clone or navigate to the project directory**
```bash
cd "C:\Users\pranav sarwade\OneDrive\Desktop\Hotel Billing"
```

2. **Create and activate virtual environment** (if not already created)
```bash
python -m venv .venv
.venv\Scripts\Activate.ps1
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Initialize the database**
```bash
python database.py
```

5. **Run the application**
```bash
python app.py
```

6. **Open in browser**
```
http://127.0.0.1:5000
```

## 🎨 Design Highlights

### Color Palette
- **Primary**: Purple gradient (#6366f1 to #4f46e5)
- **Success**: Cyan gradient (#4facfe to #00f2fe)
- **Dark**: Deep slate (#0f172a to #1e293b)
- **Accent Colors**: Success green, Warning orange, Danger red, Info cyan

### Typography
- **Font Family**: Inter (professional, modern sans-serif)
- **Headings**: Bold weights (700-800) with gradient text effects
- **Body**: Regular weight (400) with 1.6 line height for readability

### Animations
- **Fade-in**: Scroll-triggered animations for cards and sections
- **Float**: Gentle floating animation for stat icons
- **Hover**: Lift effect on cards and buttons
- **Slide**: Smooth slide-in for alerts and notifications

## 📱 Responsive Breakpoints

- **Desktop**: 1280px+ (full layout)
- **Tablet**: 768px - 1024px (adjusted grid)
- **Mobile**: 480px - 768px (single column)
- **Small Mobile**: < 480px (optimized for small screens)

## 🖨️ Print Optimization

The invoice page includes print-specific styles:
- Removes navigation, footer, and buttons
- Optimizes layout for paper
- Removes shadows and backgrounds
- Ensures all information is visible

## 🔧 Customization

### Change Color Scheme
Edit the CSS variables in `static/css/style.css`:
```css
:root {
    --primary-color: #6366f1;
    --primary-dark: #4f46e5;
    /* ... other colors */
}
```

### Modify Hotel Information
Update hotel details in `templates/invoice.html`:
```html
<h1>🏨 Your Hotel Name</h1>
<p>📍 Your Address</p>
<p>📞 Phone: Your Phone | 📧 Email: your@email.com</p>
```

## 📝 License

This project is provided as-is for educational and commercial use.

## 🙏 Credits

Designed and developed with ❤️ for professional hotel management.

---

**Version**: 2.0 (Professional Edition)  
**Last Updated**: March 2026
