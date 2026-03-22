# Diagram Prompts for ChatGPT Image Generation

Use these prompts with ChatGPT or DALL-E to generate professional diagrams for your project report.

---

## 1. System Architecture Diagram

**Prompt:**
```
Create a professional system architecture diagram for a Policy-as-Code web application platform with the following components:

1. CLIENT LAYER (left side):
   - Web Browser with HTML/CSS/JavaScript
   - REST API calls

2. APPLICATION LAYER (center):
   - Flask Web Server (Python)
   - Authentication Module (JWT)
   - Authorization Module
   - Audit Logger
   - OPA Client

3. POLICY ENGINE (right side):
   - Open Policy Agent (OPA) Server
   - Rego Policy Files (RBAC, Department, Time-based)

4. DATA LAYER (bottom):
   - SQLite Database with tables: Users, Policies, AuditLogs

Show arrows indicating:
- HTTP requests from browser to Flask
- Policy queries from Flask to OPA
- Database connections from Flask to SQLite
- JWT token flow

Use a clean, professional style with blue and gray colors. Include icons for each component. Label all connections clearly.
```

---

## 2. Authentication Flow Diagram

**Prompt:**
```
Create a sequence diagram showing the authentication flow for a web application:

ACTORS: User, Web Browser, Flask Server, Database

FLOW:
1. User enters credentials (username, password)
2. Browser sends POST /auth/login request
3. Flask Server receives request
4. Server queries Database for user
5. Server verifies password hash using bcrypt
6. If valid: Server generates JWT token with claims (user_id, role, department)
7. Server returns JWT token to browser
8. Browser stores token in localStorage
9. Subsequent requests include token in Authorization header

Use professional flowchart style with swim lanes for each actor. Use arrows to show data flow direction. Include decision diamonds for password verification. Color code: Green for success paths, Red for failure paths.
```

---

## 3. Authorization Flow Diagram

**Prompt:**
```
Create a detailed flowchart showing the authorization decision flow:

START: User makes API request

STEPS:
1. Request arrives at Flask endpoint
2. JWT token extracted from Authorization header
3. Token validated (signature, expiration)
4. User claims extracted (role, department, designation)
5. Authorization request built with:
   - Subject: user attributes
   - Action: HTTP method + endpoint
   - Resource: requested resource details
6. Query sent to OPA server
7. OPA evaluates Rego policies:
   - RBAC policy (role-based)
   - Department policy (organizational)
   - Time-based policy (business hours)
8. Decision returned: ALLOW or DENY
9. If ALLOW: Execute request, return response
10. If DENY: Return 403 Forbidden
11. Log decision to Audit table

END

Use diamond shapes for decisions, rectangles for processes, cylinders for databases. Show OPA as a distinct component. Use color coding: Blue for normal flow, Green for allow, Red for deny.
```

---

## 4. Data Flow Diagram (DFD)

**Prompt:**
```
Create a Level 1 Data Flow Diagram for a Policy-as-Code Authorization Platform:

EXTERNAL ENTITIES (rectangles):
- End User
- Administrator
- Security Auditor

PROCESSES (circles/ovals):
1.0 User Authentication
2.0 Policy Management
3.0 Resource Access Control
4.0 Audit Logging
5.0 Policy Evaluation (OPA)

DATA STORES (open rectangles):
D1: User Database
D2: Policy Repository
D3: Audit Log Store

DATA FLOWS (arrows with labels):
- Login credentials → 1.0
- JWT Token → End User
- Policy CRUD requests → 2.0
- Rego policies → D2
- Access requests → 3.0
- Authorization queries → 5.0
- Allow/Deny decisions → 3.0
- Audit records → D3
- Audit reports → Security Auditor

Use standard DFD notation. Clean professional style with clear labels on all flows.
```

---

## 5. Database ER Diagram

**Prompt:**
```
Create an Entity-Relationship diagram for a Policy-as-Code platform database:

ENTITIES:

1. USER (Primary entity)
   - id (PK, Integer)
   - username (String, Unique)
   - email (String, Unique)
   - password_hash (String)
   - role (String: admin/manager/employee)
   - department (String)
   - designation (String)
   - is_active (Boolean)
   - created_at (DateTime)
   - updated_at (DateTime)

2. POLICY (Primary entity)
   - id (PK, Integer)
   - name (String, Unique)
   - description (Text)
   - rego_code (Text)
   - is_active (Boolean)
   - created_by (FK → User.id)
   - created_at (DateTime)
   - updated_at (DateTime)

3. AUDIT_LOG (Primary entity)
   - id (PK, Integer)
   - user_id (FK → User.id)
   - action (String)
   - resource (String)
   - decision (String: allowed/denied)
   - reason (Text)
   - ip_address (String)
   - timestamp (DateTime)

RELATIONSHIPS:
- User (1) ——creates——> (N) Policy
- User (1) ——generates——> (N) AuditLog

Use crow's foot notation. Show primary keys underlined. Show foreign key relationships with connecting lines. Professional database diagram style.
```

---

## 6. Component Diagram

**Prompt:**
```
Create a UML Component Diagram for a Flask + OPA Policy Platform:

COMPONENTS:

1. <<component>> Web Interface
   - Templates (Jinja2)
   - Static Assets (CSS, JS)
   
2. <<component>> Flask Application
   - Auth Blueprint
   - Policy Blueprint
   - Resources Blueprint
   - Audit Blueprint
   - Main Routes

3. <<component>> OPA Client
   - Policy Evaluator
   - Fallback Handler
   - Health Checker

4. <<component>> Database Layer
   - SQLAlchemy ORM
   - Models (User, Policy, AuditLog)

5. <<component>> Open Policy Agent
   - Rego Engine
   - Policy Store
   - REST API

INTERFACES (lollipops):
- HTTP REST API
- OPA Query API
- Database Connection

Show dependencies with dashed arrows. Group related components. Use standard UML notation.
```

---

## 7. Deployment Diagram

**Prompt:**
```
Create a UML Deployment Diagram showing how the Policy-as-Code platform is deployed:

NODES:

1. <<device>> Client Machine
   - <<artifact>> Web Browser
   
2. <<execution environment>> Application Server
   - <<artifact>> Flask Application (run.py)
   - <<artifact>> Python 3.8+ Runtime
   - <<artifact>> Virtual Environment
   
3. <<execution environment>> Policy Server
   - <<artifact>> OPA Binary
   - <<artifact>> Rego Policy Files
   
4. <<device>> Database Server
   - <<artifact>> SQLite Database File (app.db)

CONNECTIONS:
- Client → Application Server: HTTPS (Port 5000)
- Application Server → Policy Server: HTTP (Port 8181)
- Application Server → Database: File I/O

Show communication protocols on connections. Use 3D box notation for devices. Include port numbers.
```

---

## 8. Use Case Diagram

**Prompt:**
```
Create a UML Use Case Diagram for a Policy-as-Code Authorization Platform:

ACTORS:
- Employee (basic user)
- Manager (extends Employee)
- Administrator (extends Manager)
- OPA System (system actor)

USE CASES:

Employee:
- Login/Logout
- View Own Profile
- Access Department Resources
- View Own Audit Logs

Manager (includes Employee cases):
- Manage Team Resources
- View Team Audit Logs
- Approve Resource Access

Administrator (includes Manager cases):
- Manage Users (CRUD)
- Manage Policies (CRUD)
- View All Audit Logs
- Configure System Settings
- Monitor OPA Health

OPA System:
- Evaluate Policies
- Enforce Access Control
- Log Decisions

Show inheritance between actors with triangular arrows. Group use cases in a system boundary box labeled "Policy-as-Code Platform". Use <<include>> and <<extend>> relationships where appropriate.
```

---

## 9. Class Diagram

**Prompt:**
```
Create a UML Class Diagram for the Policy-as-Code Platform models:

CLASSES:

1. User
   - Attributes:
     + id: Integer
     + username: String
     + email: String
     - password_hash: String
     + role: String
     + department: String
     + designation: String
     + is_active: Boolean
   - Methods:
     + set_password(password): void
     + check_password(password): Boolean
     + to_dict(): Dictionary

2. Policy
   - Attributes:
     + id: Integer
     + name: String
     + description: String
     + rego_code: Text
     + is_active: Boolean
     + created_by: Integer
   - Methods:
     + validate_rego(): Boolean
     + to_dict(): Dictionary

3. AuditLog
   - Attributes:
     + id: Integer
     + user_id: Integer
     + action: String
     + resource: String
     + decision: String
     + timestamp: DateTime
   - Methods:
     + to_dict(): Dictionary

4. OPAClient
   - Attributes:
     - server_url: String
     - timeout: Integer
   - Methods:
     + evaluate_policy(path, input): Dict
     + check_health(): Boolean
     + load_policy(name, code): Boolean

RELATIONSHIPS:
- User "1" ——→ "*" Policy (creates)
- User "1" ——→ "*" AuditLog (generates)
- OPAClient uses Policy

Show visibility (+public, -private). Use standard UML class notation with three compartments.
```

---

## 10. State Diagram - User Session

**Prompt:**
```
Create a UML State Diagram showing user session states in the authentication system:

STATES:
- [Initial] → Unauthenticated
- Unauthenticated
- Authenticating
- Authenticated
- Session Expired
- Locked Out
- [Final]

TRANSITIONS:
- Unauthenticated → Authenticating: submit credentials
- Authenticating → Authenticated: valid credentials
- Authenticating → Unauthenticated: invalid credentials
- Authenticating → Locked Out: 3 failed attempts
- Authenticated → Unauthenticated: logout
- Authenticated → Session Expired: token expires
- Session Expired → Authenticating: refresh attempt
- Session Expired → Unauthenticated: re-login
- Locked Out → Unauthenticated: timeout (30 min)

Show guard conditions in square brackets. Use rounded rectangles for states. Show entry/exit actions where applicable.
```

---

## Tips for Best Results:

1. **Be specific** about colors, styles, and layout preferences
2. **Request professional/technical style** for academic reports
3. **Ask for labels** on all connections and components
4. **Specify notation** (UML, flowchart, etc.) for consistency
5. **Request high resolution** if needed for printing

---

## Alternative: Text-Based Diagrams

If you need ASCII/text diagrams for documentation, use these tools:
- **Mermaid.js** - For flowcharts, sequence diagrams
- **PlantUML** - For UML diagrams
- **draw.io** - Free online diagram tool
- **Lucidchart** - Professional diagramming

