# 🍽️ DigiMenu – A Smart Digital Menu Web Application

DigiMenu is a modern **digital menu web application** built using **Django (backend)** and **HTML/CSS/JavaScript (frontend)**.  
It allows restaurant owners to create and manage personalized digital menu cards that can be shared via **custom URLs** or **downloadable QR codes**.

---

## 📖 Features

- 👤 **User Registration & Login** with authentication
- 🛠️ **Admin Panel** for restaurant owners
- 🏪 Add/Edit **Restaurant Info** (name, logo, contact info)
- 📋 **CRUD Operations** for menu items by category
- 🖼️ Upload **item images**
- 🎡 **Featured Items Carousel**
- ⭐ **Today's Specials** section (auto/manual entry)
- 🔍 **Category Filter & Search** (AJAX-powered)
- 🛒 **Live Order Cart Preview** (no payment integration)
- 🔗 **Dynamic Menu URL** (e.g., `/vrindavansweets`)
- 📱 **QR Code Generation** for menu sharing
- 💬 **Customer Ratings & Comments**
- 📱 **Responsive UI** with a modern, visual-rich layout

---

## 🛠️ Tech Stack

### Frontend
- HTML5, CSS3, JavaScript  
- Bootstrap 5 / Tailwind CSS  
- AJAX for real-time filtering/search  
- jQuery (optional for DOM updates)  

### Backend
- Django (v3.0.5 or higher)  
- Django Rest Framework (optional for APIs)  
- SQLite / MySQL / MariaDB  
- Pillow (image uploads)  
- qrcode (QR code generation)  

### Deployment
- GitHub (version control)  
- Render / Vercel / Heroku / Own server  
- Custom domain routing with slugs  

---

## 🚀 Workflow

1. Users register or log in.  
2. Owners set up their restaurant profile (name, logo, contact info).  
3. Add/edit/delete menu categories and items.  
4. Upload images and manage availability.  
5. Highlight specials and featured items.  
6. Save & generate live menu URL.  
7. Auto-generate **QR code** for sharing.  
8. Customers can view, search, and filter menu items.  
9. Customers can add to cart (preview only).  
10. Customers can rate and comment on items.  
11. Owners can update menus anytime.  

---

## ⚙️ Setup & Installation

1. Clone this repo:
   ```bash
   git clone https://github.com/adu-upreti/digi_menu.git
   cd digi_menu

2. Create & activate a virtual environment:

python -m venv venv
source venv/bin/activate   # macOS/Linux
venv\Scripts\activate      # Windows


3. Install dependencies:

pip install -r requirements.txt


4. Apply migrations:

python manage.py migrate


5. Create a superuser (for admin access):

python manage.py createsuperuser


6. Run the server:

python manage.py runserver


7. Open in browser:

http://127.0.0.1:8000/