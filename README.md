# Policy-as-Code Platform for Web Applications

A production-ready academic project demonstrating **Policy-as-Code** principles using Flask, Open Policy Agent (OPA), and Rego policies for externalized authorization.

## 🎯 Project Overview

This platform implements a scalable and flexible authorization system by externalizing access control rules as code. Instead of hardcoding authorization logic in the application, policies are defined in Rego language and evaluated by OPA, enabling dynamic policy updates without application redeployment.

### Key Features

- **Policy-as-Code**: Authorization rules written in Rego, versioned and testable
- **Attribute-Based Access Control (ABAC)**: Decisions based on user, resource, action, and environment attributes
- **Dynamic Policy Updates**: Modify policies at runtime without restarting the application
- **JWT Authentication**: Secure token-based authentication with bcrypt password hashing
- **Comprehensive Audit Logging**: Complete trail of all authorization decisions
- **Admin Dashboard**: Web interface for policy and user management
- **RESTful API**: Clean API endpoints for all operations

## 🏗️ System Architecture

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│                 │     │                 │     │                 │
│   Client App    │────▶│   Flask API     │────▶│   OPA Engine    │
│   (Browser)     │     │   (Backend)     │     │   (Policies)    │
│                 │     │                 │     │                 │
└─────────────────┘     └────────┬────────┘     └─────────────────┘
                                 │
                                 ▼
                        ┌─────────────────┐
                        │                 │
                        │   SQLite DB     │
                        │   (Storage)     │
                        │                 │
                        └─────────────────┘
```

### Authorization Flow

1. Client sends request with JWT token
2. Flask extracts user attributes from JWT
3. Flask builds authorization request with user, action, resource, and environment data
4. Request is sent to OPA for policy evaluation
5. OPA evaluates Rego policy and returns ALLOW/DENY with reason
6. Flask enforces the decision and logs it to audit trail

## 🛠️ Technology Stack

| Component | Technology |
|-----------|------------|
| Backend | Python 3.8+, Flask 2.3 |
| Frontend | HTML5, Tailwind CSS |
| Policy Engine | Open Policy Agent (OPA), Rego |
| Database | SQLite |
| Authentication | JWT (JSON Web Tokens) |
| Password Hashing | bcrypt |

## 📁 Project Structure

```
PolicyAsCodePlatform/
├── app/
│   ├── __init__.py          # Application factory
│   ├── models.py            # Database models (User, Policy, AuditLog)
│   ├── routes.py            # Main routes and dashboard
│   ├── opa_client.py        # OPA integration client
│   ├── auth/
│   │   ├── __init__.py
│   │   └── routes.py        # Authentication endpoints
│   ├── policy/
│   │   ├── __init__.py
│   │   └── routes.py        # Policy management endpoints
│   ├── resources/
│   │   ├── __init__.py
│   │   └── routes.py        # Protected resource endpoints
│   ├── audit/
│   │   ├── __init__.py
│   │   └── routes.py        # Audit log endpoints
│   ├── templates/           # HTML templates
│   │   ├── base.html
│   │   ├── index.html
│   │   ├── login.html
│   │   ├── dashboard.html
│   │   ├── policies.html
│   │   ├── policy_form.html
│   │   ├── users.html
│   │   ├── audit.html
│   │   ├── test.html
│   │   └── api_docs.html
│   └── static/              # Static assets
├── opa_policies/            # Rego policy files
│   ├── authz.rego           # Main ABAC policy
│   ├── rbac.rego            # RBAC example
│   ├── time_based.rego      # Time-based policy
│   └── department.rego      # Department isolation policy
├── tests/                   # Test files
├── config.py                # Configuration settings
├── run.py                   # Application entry point
├── init_db.py               # Database initialization script
├── requirements.txt         # Python dependencies
└── README.md                # This file
```

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- OPA (optional, for full functionality)

### Installation

1. **Clone or navigate to the project directory**
   ```bash
   cd C:\Users\INTEL\Documents\2026-2027\python-projects\PolicyAsCodePlatform
   ```

2. **Create a virtual environment (recommended)**
   ```bash
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   
   # Linux/Mac
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Initialize the database with sample data**
   ```bash
   python init_db.py
   ```

5. **Run the Flask application**
   ```bash
   python run.py
   ```

6. **Access the application**
   - Dashboard: http://localhost:5000/dashboard
   - API Docs: http://localhost:5000/api-docs
   - Login: http://localhost:5000/login

### (Optional) Start OPA Server

For full OPA functionality, start the OPA server in a separate terminal:

```bash
# Download OPA (if not installed)
# Windows: Download from https://www.openpolicyagent.org/docs/latest/#running-opa

# Start OPA server with policies
opa run --server opa_policies/
```

The application works without OPA using a local fallback evaluator.

## 🔑 Test Credentials

| Username | Password | Role | Department |
|----------|----------|------|------------|
| admin | admin123 | Admin | Management |
| manager | manager123 | Manager | Engineering |
| employee | employee123 | Employee | Engineering |
| hr_manager | hr123 | Manager | HR |
| finance_employee | finance123 | Employee | Finance |

## 📡 API Endpoints

### Authentication

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/auth/register` | Register new user |
| POST | `/auth/login` | Login and get JWT token |
| GET | `/auth/profile` | Get current user profile |
| GET | `/auth/users` | List all users (admin only) |

### Policy Management

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/policy/evaluate` | Evaluate authorization request |
| GET | `/policy/list` | List all policies |
| POST | `/policy/create` | Create new policy (admin) |
| PUT | `/policy/update/<id>` | Update policy (admin) |
| PUT | `/policy/toggle/<id>` | Enable/disable policy (admin) |
| DELETE | `/policy/delete/<id>` | Delete policy (admin) |
| GET | `/policy/opa-status` | Check OPA server status |

### Protected Resources

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/resource/data` | Get protected data |
| GET | `/resource/documents` | Get department documents |
| POST | `/resource/documents` | Create document |
| DELETE | `/resource/documents/<id>` | Delete document |
| GET | `/resource/reports` | Get reports |
| GET | `/resource/settings` | Get settings (admin) |

### Audit Logs

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/audit/logs` | Get audit logs |
| GET | `/audit/stats` | Get authorization statistics |
| GET | `/audit/export` | Export audit logs |

## 🧪 API Testing with cURL

### Login and Get Token

```bash
curl -X POST http://localhost:5000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "admin123"}'
```

### Evaluate Policy

```bash
curl -X POST http://localhost:5000/policy/evaluate \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "action": "read",
    "resource": {
      "type": "document",
      "department": "engineering"
    }
  }'
```

### Access Protected Resource

```bash
curl http://localhost:5000/resource/documents \
  -H "Authorization: Bearer YOUR_TOKEN"
```

## 📜 Understanding the Policies

### Main ABAC Policy (authz.rego)

The main policy implements these rules:

1. **Admin**: Full access to all resources at any time
2. **Manager**: Read/write access during office hours (9 AM - 6 PM), own department only
3. **Employee**: Read-only access to own department resources

### Policy Input Structure

```json
{
  "user": {
    "id": 1,
    "username": "employee",
    "role": "employee",
    "department": "engineering"
  },
  "action": "read",
  "resource": {
    "type": "document",
    "department": "engineering"
  },
  "environment": {
    "time": "14:30",
    "hour": 14,
    "day": "Monday",
    "ip": "192.168.1.1"
  }
}
```

### Policy Output

```json
{
  "allow": true,
  "reason": "Employee can read own department resources"
}
```

## 🎓 Academic Project Notes

### Suitable for Viva Questions

1. **Why Policy-as-Code?**
   - Separation of concerns: Business logic vs authorization logic
   - Dynamic updates without redeployment
   - Auditable and testable policies
   - Consistent enforcement across services

2. **Why OPA?**
   - Purpose-built for policy decisions
   - Declarative policy language (Rego)
   - High performance and scalability
   - Cloud-native and widely adopted

3. **ABAC vs RBAC**
   - RBAC: Role-based, simpler but less flexible
   - ABAC: Attribute-based, supports complex rules
   - This project demonstrates both approaches

4. **Security Considerations**
   - JWT tokens for stateless authentication
   - bcrypt for secure password hashing
   - Centralized policy enforcement
   - Complete audit trail

### Key Learning Outcomes

- Understanding Policy-as-Code architecture
- Implementing ABAC with Rego policies
- Integrating OPA with Flask applications
- Building secure authentication systems
- Designing audit logging for compliance

## 🔧 Configuration

Environment variables (optional):

```bash
# Flask configuration
FLASK_CONFIG=development
FLASK_HOST=0.0.0.0
FLASK_PORT=5000
FLASK_DEBUG=True

# Security (change in production!)
SECRET_KEY=your-secret-key
JWT_SECRET_KEY=your-jwt-secret

# OPA server
OPA_SERVER_URL=http://localhost:8181
```

## 📝 License

This project is created for academic purposes as a final-year project demonstration.

## 👨‍💻 Author

Created as an academic project demonstrating Policy-as-Code principles for web application authorization.

---

**Note**: This is an educational project. For production use, ensure proper security hardening, use environment variables for secrets, and deploy OPA in a production-ready configuration.
