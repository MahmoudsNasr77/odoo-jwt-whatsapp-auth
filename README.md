# 🔐 Odoo 17 JWT Authentication + WhatsApp API 🌐💬

A custom Odoo 17 module that provides:

- ✅ JWT-based login via `/api/login`
- ✅ Secured WhatsApp messaging via `/api/send-whatsapp`
- ✅ Token validation and secret key management via `ir.config_parameter`
- ✅ Ready for React or Postman integration

---

## 📦 Features

- 🔐 **Secure Login API** using JWT
- 💬 **Send WhatsApp Messages** through protected API
- 🛡️ Token-based protection for routes
- ⚙️ Stores JWT secret key in `ir.config_parameter`
- 📦 Easily extendable for custom frontend use (React, etc.)
- 📬 Comes with full API integration (ready for Postman)


## 🔐 Authentication API

### 📤 POST `/api/login`

Authenticates user and returns a JWT token.

#### 🧪 Example Request (JSON):
```
{
  "login": "admin",
  "password": "admin"
}
```
#### ✅ Example Response:
```
{
  "token": "eyJhbGciOiJIUzI1NiIsInR5..."
}
```
💬 WhatsApp API
📤 POST /api/send-whatsapp
Send a message to a Company phone number via WhatsApp API. Protected by JWT.

🔐 Header:
```
Authorization: Bearer <JWT_TOKEN>
```
📦 Body (JSON):
```
{
  "Name": "Mahmoud",
  "message": "Hello from Odoo!"
}

```
✅ Example Response:
```
{
  "success": "Message sent"
}

```
### Configuration
Set JWT Secret Key

You must set the JWT secret before using the API:

# 👚 Odoo Shell
```
env['ir.config_parameter'].sudo().set_param('jwt_secret_key', 'your_secret_key_here')
```

### 🛠️ Installation

# Clone this repo into your custom-addons folder:

```git clone https://github.com/YOUR_USERNAME/odoo-jwt-whatsapp-auth.git```

#Add the module path to your odoo.conf:

```addons_path = /your/path/to/custom-addons```

# Restart Odoo server and install the module from Apps menu.

### 🧰 Dependencies

# PyJWT

```pip install PyJWT```

### 🤝 Author

Mahmoud Sabry
# 📧 mahmoudsabrynasr@gmail.com








