# Onboarding System - Technical Architecture

**Date:** 2026-06-12  
**Project:** Batten School Onboarding Process Redesign  
**Recommended Approach:** Modified Option B (Phased Rebuild)

---

## Architecture Decision: Portal vs. Monday.com

### Option 1: Extend Existing Portal ✅ RECOMMENDED
**Pros:**
- Already built and deployed at thebattenspace.org/onboarding
- Full control over features and UI/UX
- Integration with existing Batten Space infrastructure
- No recurring license costs
- Can customize to exact Batten workflows
- Already has Netbadge SSO integration

**Cons:**
- Requires ongoing development/maintenance
- Need to build all features ourselves

### Option 2: Use Monday.com
**Pros:**
- Team already has accounts
- Built-in task management and notifications
- No development required for basic features
- Mobile apps included

**Cons:**
- Monthly per-user cost
- Limited customization
- Separate from other Batten Space tools
- Data lives in external system
- May not fit exact workflow needs
- Need to build integration layer anyway

**Recommendation:** Extend the existing portal. Since you've already built the foundation, we can add workflow tracking, role-based dashboards, and task management directly. Use Monday.com's concepts (boards, tasks, assignments) as inspiration for the UI, but keep everything in our control.

---

## System Architecture Overview

```
┌─────────────────────────────────────────────────────────────────────┐
│                         USER LAYER                                    │
│                                                                       │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐              │
│  │   Managers   │  │  Department  │  │ Associate    │              │
│  │  Dashboard   │  │  Dashboards  │  │ Dean Admin   │              │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘              │
│         │                  │                  │                      │
│         └──────────────────┴──────────────────┘                      │
│                             │                                        │
└─────────────────────────────┼────────────────────────────────────────┘
                              │
┌─────────────────────────────┼────────────────────────────────────────┐
│                       API LAYER (Next.js)                             │
│                             │                                        │
│  ┌──────────────────────────┴───────────────────────────────────┐  │
│  │              Next.js API Routes / tRPC                        │  │
│  │                                                                │  │
│  │  /api/onboarding    /api/tasks    /api/notifications          │  │
│  │  /api/users         /api/reports  /api/integrations           │  │
│  └────────────────────────────────────────────────────────────────┘  │
│                             │                                        │
└─────────────────────────────┼────────────────────────────────────────┘
                              │
┌─────────────────────────────┼────────────────────────────────────────┐
│                    BUSINESS LOGIC LAYER                               │
│                             │                                        │
│  ┌────────────────┐  ┌─────┴──────┐  ┌────────────────┐            │
│  │   Workflow     │  │   Task     │  │  Notification  │            │
│  │   Engine       │  │   Manager  │  │    Engine      │            │
│  └────────────────┘  └────────────┘  └────────────────┘            │
│                                                                       │
└─────────────────────────────────────────────────────────────────────┘
                              │
┌─────────────────────────────┼────────────────────────────────────────┐
│                         DATA LAYER                                    │
│                             │                                        │
│  ┌─────────────────────────┴────────────────────────────────────┐  │
│  │                    PostgreSQL Database                        │  │
│  │                                                                │  │
│  │   onboardings   tasks   notifications   users   audit_log     │  │
│  └────────────────────────────────────────────────────────────────┘  │
│                                                                       │
└─────────────────────────────────────────────────────────────────────┘
                              │
┌─────────────────────────────┼────────────────────────────────────────┐
│                    INTEGRATION LAYER                                  │
│                             │                                        │
│  ┌──────────┐  ┌────────┐  ┌────────────┐  ┌────────────────┐     │
│  │  UVA HR  │  │ Active │  │  Canvas    │  │   Email        │     │
│  │   API    │  │  Dir   │  │   LMS      │  │  (SendGrid)    │     │
│  └──────────┘  └────────┘  └────────────┘  └────────────────┘     │
│                                                                       │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Technology Stack

### Frontend
- **Framework**: Next.js 14+ (App Router)
- **Language**: TypeScript
- **UI Library**: React 18+
- **Styling**: Tailwind CSS (consistent with Batten Space brand)
- **State Management**: React Context + Zustand (for complex state)
- **Forms**: React Hook Form + Zod validation
- **Date Handling**: date-fns
- **HTTP Client**: tRPC or native fetch

### Backend
- **Runtime**: Node.js 20+ LTS
- **Framework**: Next.js API Routes or separate Express app
- **Language**: TypeScript
- **ORM**: Prisma (PostgreSQL)
- **Validation**: Zod
- **Auth**: NextAuth.js with UVA Netbadge provider
- **Background Jobs**: BullMQ + Redis
- **Email**: SendGrid or UVA mail service

### Database
- **Primary DB**: PostgreSQL 15+
- **Cache**: Redis 7+
- **File Storage**: Azure Blob Storage (for attachments/photos)

### Infrastructure
- **Hosting**: Azure App Service (same as current Batten Space)
- **Database**: Azure Database for PostgreSQL
- **Cache**: Azure Cache for Redis
- **CI/CD**: GitHub Actions
- **Monitoring**: Application Insights

### Third-Party Services
- **Authentication**: UVA Netbadge (SAML/OAuth)
- **Email Delivery**: SendGrid or UVA mail service
- **Analytics**: Google Analytics or Application Insights
- **Error Tracking**: Sentry (optional)

---

## Database Schema

```sql
-- Core Tables

CREATE TABLE onboardings (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    employee_name VARCHAR(255) NOT NULL,
    employee_email VARCHAR(255),
    uva_email VARCHAR(255),
    title VARCHAR(255) NOT NULL,
    employee_type VARCHAR(50) NOT NULL, -- staff, faculty, wage, etc.
    department VARCHAR(255) NOT NULL,
    start_date DATE NOT NULL,
    manager_id VARCHAR(50) NOT NULL, -- UVA computing ID
    manager_name VARCHAR(255),
    batten_buddy_id VARCHAR(50),
    office_location VARCHAR(255),
    
    -- Phase tracking
    current_phase VARCHAR(50) NOT NULL DEFAULT 'phase1_preboarding',
    phase1_complete BOOLEAN DEFAULT FALSE,
    phase2_complete BOOLEAN DEFAULT FALSE,
    phase3_complete BOOLEAN DEFAULT FALSE,
    phase4_complete BOOLEAN DEFAULT FALSE,
    phase5_complete BOOLEAN DEFAULT FALSE,
    
    -- Approval tracking
    search_approved BOOLEAN DEFAULT FALSE,
    search_approved_date DATE,
    search_approved_reference VARCHAR(100),
    process_approved BOOLEAN DEFAULT FALSE,
    process_approved_date DATE,
    comp_approved BOOLEAN DEFAULT FALSE,
    comp_approved_date DATE,
    hire_approved BOOLEAN DEFAULT FALSE,
    hire_approved_date DATE,
    
    -- Meta
    status VARCHAR(50) NOT NULL DEFAULT 'pending', -- pending, active, complete, cancelled
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_by VARCHAR(50) NOT NULL,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    completed_at TIMESTAMP
);

CREATE TABLE tasks (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    onboarding_id UUID NOT NULL REFERENCES onboardings(id) ON DELETE CASCADE,
    
    -- Task details
    title VARCHAR(255) NOT NULL,
    description TEXT,
    category VARCHAR(50) NOT NULL, -- it, operations, finance, marcomm, manager
    phase VARCHAR(50) NOT NULL, -- phase1, phase2, etc.
    
    -- Assignment
    assigned_to VARCHAR(50), -- UVA computing ID
    assigned_to_role VARCHAR(50), -- it_admin, ops_team, manager, etc.
    
    -- Status
    status VARCHAR(50) NOT NULL DEFAULT 'pending', -- pending, in_progress, complete, blocked
    completed_by VARCHAR(50),
    completed_at TIMESTAMP,
    due_date DATE,
    
    -- Task-specific data (JSON for flexibility)
    task_data JSONB,
    
    -- Meta
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE notifications (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    onboarding_id UUID REFERENCES onboardings(id) ON DELETE CASCADE,
    task_id UUID REFERENCES tasks(id) ON DELETE CASCADE,
    
    -- Notification details
    recipient VARCHAR(50) NOT NULL, -- UVA computing ID or email
    type VARCHAR(50) NOT NULL, -- task_assigned, task_overdue, phase_complete, etc.
    channel VARCHAR(50) NOT NULL, -- email, in_app
    subject VARCHAR(255),
    body TEXT,
    
    -- Status
    status VARCHAR(50) NOT NULL DEFAULT 'pending', -- pending, sent, failed
    sent_at TIMESTAMP,
    read_at TIMESTAMP,
    
    -- Meta
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE audit_log (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    onboarding_id UUID REFERENCES onboardings(id) ON DELETE CASCADE,
    task_id UUID REFERENCES tasks(id) ON DELETE CASCADE,
    
    -- Action details
    user_id VARCHAR(50) NOT NULL,
    action VARCHAR(100) NOT NULL, -- created_onboarding, completed_task, etc.
    entity_type VARCHAR(50) NOT NULL, -- onboarding, task, notification
    entity_id UUID,
    
    -- Change tracking
    old_value JSONB,
    new_value JSONB,
    
    -- Meta
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    ip_address VARCHAR(50),
    user_agent TEXT
);

CREATE TABLE templates (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    
    -- Template details
    name VARCHAR(255) NOT NULL,
    type VARCHAR(50) NOT NULL, -- email, task_checklist
    category VARCHAR(50), -- it, operations, etc.
    employee_type VARCHAR(50), -- staff, faculty, all
    
    -- Content
    subject VARCHAR(255),
    body TEXT,
    template_data JSONB, -- For task checklists
    
    -- Status
    active BOOLEAN DEFAULT TRUE,
    
    -- Meta
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_by VARCHAR(50)
);

CREATE TABLE users (
    id VARCHAR(50) PRIMARY KEY, -- UVA computing ID
    email VARCHAR(255) NOT NULL,
    name VARCHAR(255),
    department VARCHAR(255),
    roles JSONB, -- ['manager', 'it_admin', 'ops_team', etc.]
    
    -- Preferences
    notification_preferences JSONB,
    
    -- Meta
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP
);

-- Indexes for performance

CREATE INDEX idx_onboardings_status ON onboardings(status);
CREATE INDEX idx_onboardings_start_date ON onboardings(start_date);
CREATE INDEX idx_onboardings_manager ON onboardings(manager_id);
CREATE INDEX idx_onboardings_phase ON onboardings(current_phase);

CREATE INDEX idx_tasks_onboarding ON tasks(onboarding_id);
CREATE INDEX idx_tasks_assigned_to ON tasks(assigned_to);
CREATE INDEX idx_tasks_status ON tasks(status);
CREATE INDEX idx_tasks_category ON tasks(category);
CREATE INDEX idx_tasks_due_date ON tasks(due_date);

CREATE INDEX idx_notifications_recipient ON notifications(recipient);
CREATE INDEX idx_notifications_status ON notifications(status);

CREATE INDEX idx_audit_onboarding ON audit_log(onboarding_id);
CREATE INDEX idx_audit_user ON audit_log(user_id);
CREATE INDEX idx_audit_created ON audit_log(created_at);
```

---

## API Endpoints

### Onboarding Management

```typescript
// Create new onboarding
POST /api/onboarding
{
  employeeName: string;
  title: string;
  employeeType: 'staff' | 'faculty' | 'wage' | 'adjunct' | 'postdoc' | 'student worker' | 'contractor';
  department: string;
  startDate: Date;
  employeeEmail: string; // non-UVA email
  managerId: string;
  approvals: {
    searchApproved: boolean;
    processApproved: boolean;
    compApproved: boolean;
    hireApproved: boolean;
  };
}

// Get all onboardings (with filters)
GET /api/onboarding?status=active&manager=abc1a&startDate=2026-06-01

// Get specific onboarding
GET /api/onboarding/:id

// Update onboarding
PATCH /api/onboarding/:id
{
  status?: string;
  currentPhase?: string;
  battenBuddyId?: string;
  officeLocation?: string;
  // ... other fields
}

// Advance to next phase
POST /api/onboarding/:id/advance-phase

// Cancel onboarding
POST /api/onboarding/:id/cancel
```

### Task Management

```typescript
// Get tasks for onboarding
GET /api/onboarding/:id/tasks

// Get tasks assigned to user
GET /api/tasks/assigned-to-me

// Get tasks by department
GET /api/tasks?category=it&status=pending

// Update task
PATCH /api/tasks/:id
{
  status?: 'pending' | 'in_progress' | 'complete' | 'blocked';
  taskData?: Record<string, any>;
}

// Complete task
POST /api/tasks/:id/complete
{
  notes?: string;
  taskData?: Record<string, any>;
}

// Bulk complete tasks
POST /api/tasks/bulk-complete
{
  taskIds: string[];
}
```

### Dashboard & Reports

```typescript
// Manager dashboard
GET /api/dashboard/manager/:managerId

// Department dashboard
GET /api/dashboard/department/:category

// Admin overview
GET /api/dashboard/admin

// Reports
GET /api/reports/completion-time
GET /api/reports/bottlenecks
GET /api/reports/upcoming-starts
```

### Notifications

```typescript
// Get user notifications
GET /api/notifications/me

// Mark as read
POST /api/notifications/:id/read

// Get notification preferences
GET /api/notifications/preferences

// Update preferences
PATCH /api/notifications/preferences
```

---

## Workflow State Machine

```
┌──────────────────────────────────────────────────────────────┐
│                     ONBOARDING WORKFLOW                       │
└──────────────────────────────────────────────────────────────┘

PHASE 1: PRE-BOARDING
├── Task: Search Approved ✓
├── Task: Process Approved ✓
├── Task: Comp Approved ✓
└── Task: Hire Approved ✓
      │
      ▼
PHASE 2: ASSOCIATE DEAN ADMIN
├── Task: Enter basic information ✓
└── Task: Assign manager ✓
      │
      ▼
PHASE 3: MANAGER SETUP
├── Task: Assign Batten Buddy
├── Task: Assign office
└── Task: Initiate onboarding checklist
      │
      ▼
PHASE 4: DEPARTMENT TASKS (Parallel)
├── 4a: IT
│   ├── Task: Order computing package
│   ├── Task: Create UVA email
│   └── Task: Add to distribution lists
│
├── 4b: MARKETING & COMMUNICATIONS
│   ├── Task: Display welcome slide
│   ├── Task: Update directory
│   └── Task: Remove welcome slide (after 2 weeks)
│
├── 4c: OPERATIONS
│   ├── Task: Clean/furnish office
│   ├── Task: Order business cards
│   ├── Task: Provision building access
│   ├── Task: Schedule Dare to Lead
│   ├── Task: Issue keys
│   ├── Task: Create name-plate
│   └── Task: Update wayfinder guide
│
└── 4d: FINANCE
    ├── Task: Establish payroll costing
    ├── Task: T&E card application
    └── Task: Request security roles
      │
      ▼ (all Phase 4 tasks complete)
      │
PHASE 5: MANAGER FINAL
├── Task: Complete Ground for Success
├── Task: Request application security roles
└── Task: Review training plan
      │
      ▼
COMPLETE ✓
```

### State Transitions

- **Phase progression**: Automatic when all tasks in current phase are complete
- **Task status**: pending → in_progress → complete (or blocked)
- **Notifications**: Triggered on phase transitions and task assignments
- **Rollback**: Admin can move back to previous phase if needed
- **Cancellation**: Can cancel at any point, all future tasks marked cancelled

---

## Integration Points

### 1. UVA HR System (Future)
**Purpose**: Auto-populate start dates and employee info

```typescript
// Webhook endpoint
POST /api/webhooks/hr/new-hire
{
  employeeId: string;
  name: string;
  startDate: Date;
  department: string;
  // ...
}

// Or polling service (if no webhook available)
// Runs daily, checks for new hires with upcoming start dates
```

### 2. Active Directory / Azure AD
**Purpose**: Automated email account creation

```typescript
// Service: src/services/azure-ad.service.ts
export class AzureADService {
  async createUser(data: {
    givenName: string;
    surname: string;
    displayName: string;
    userPrincipalName: string;
    department: string;
  }): Promise<void> {
    // Use Microsoft Graph API
  }
  
  async addToGroups(userId: string, groups: string[]): Promise<void> {
    // Add to distribution lists
  }
}
```

### 3. Canvas LMS
**Purpose**: Auto-enroll in onboarding course

```typescript
// Service: src/services/canvas.service.ts
export class CanvasService {
  async enrollUser(
    courseId: string,
    userId: string,
    role: 'student'
  ): Promise<void> {
    // Use Canvas API to enroll
  }
}
```

### 4. Email Service
**Purpose**: Notifications and welcome emails

```typescript
// Service: src/services/email.service.ts
export class EmailService {
  async sendOnboardingWelcome(data: OnboardingData): Promise<void>
  async sendTaskAssignment(data: TaskData): Promise<void>
  async sendPhaseComplete(data: PhaseData): Promise<void>
  async sendReminder(data: ReminderData): Promise<void>
}
```

### 5. Building Access System (Future)
**Purpose**: Automated card access provisioning

```typescript
// Service: src/services/access-control.service.ts
export class AccessControlService {
  async requestAccess(data: {
    userId: string;
    buildings: string[];
    startDate: Date;
    endDate?: Date;
  }): Promise<string> // Returns request ID
}
```

---

## Security & Authentication

### Authentication Flow
1. User visits portal
2. Redirected to UVA Netbadge login
3. SAML assertion returned
4. Session created with user info
5. Role-based access control applied

### Authorization Levels

```typescript
enum UserRole {
  ADMIN = 'admin', // Full access
  ASSOCIATE_DEAN = 'associate_dean', // Create onboardings
  MANAGER = 'manager', // View own team, complete manager tasks
  IT_ADMIN = 'it_admin', // Complete IT tasks
  OPS_TEAM = 'ops_team', // Complete operations tasks
  FINANCE_TEAM = 'finance_team', // Complete finance tasks
  MARCOMM_TEAM = 'marcomm_team', // Complete marcomm tasks
  VIEWER = 'viewer' // Read-only access
}
```

### Permission Matrix

| Role | Create Onboarding | View All | Complete Tasks | Reports | Admin |
|------|------------------|----------|----------------|---------|-------|
| Admin | ✅ | ✅ | ✅ | ✅ | ✅ |
| Associate Dean | ✅ | ✅ | ❌ | ✅ | ❌ |
| Manager | ❌ | Own team only | Manager tasks only | Own team | ❌ |
| IT Admin | ❌ | Limited | IT tasks only | IT metrics | ❌ |
| Ops Team | ❌ | Limited | Ops tasks only | Ops metrics | ❌ |
| Finance Team | ❌ | Limited | Finance tasks only | Finance metrics | ❌ |
| MarComm Team | ❌ | Limited | MarComm tasks only | MarComm metrics | ❌ |

### Data Security
- **Encryption at rest**: Azure encryption for database
- **Encryption in transit**: HTTPS/TLS 1.3
- **PII handling**: Employee emails, addresses stored securely
- **Audit logging**: All actions logged with user, timestamp, IP
- **FERPA compliance**: If storing student worker data
- **UVA IRM-003 compliance**: Security best practices

---

## Background Jobs (BullMQ + Redis)

### Job Types

```typescript
// 1. Send notifications (async email delivery)
queue.add('send-notification', {
  notificationId: '...',
  type: 'task_assigned',
  recipient: 'abc1a@virginia.edu'
});

// 2. Daily reminders (overdue tasks)
// Cron: 0 9 * * * (9 AM daily)
queue.add('send-overdue-reminders', {});

// 3. Upcoming start date notifications
// Cron: 0 8 * * * (8 AM daily)
// Notify manager 1 week before, 3 days before, 1 day before
queue.add('check-upcoming-starts', {});

// 4. Auto-advance phases
// Check if all tasks complete, advance phase
queue.add('check-phase-completion', {
  onboardingId: '...'
});

// 5. Welcome slide removal
// Cron: 0 10 * * * (10 AM daily)
// Remove slides 2 weeks after start date
queue.add('check-welcome-slide-removal', {});

// 6. Canvas enrollment
// Triggered on Phase 2 completion
queue.add('enroll-in-canvas', {
  onboardingId: '...',
  courseId: '...'
});
```

---

## Deployment Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                         AZURE CLOUD                                   │
│                                                                       │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │  Azure Front Door (CDN + WAF)                                 │  │
│  └──────────────────────┬───────────────────────────────────────┘  │
│                         │                                           │
│  ┌──────────────────────┴───────────────────────────────────────┐  │
│  │  Azure App Service (Next.js)                                  │  │
│  │  - Production: 2+ instances (autoscale)                       │  │
│  │  - Staging: 1 instance                                        │  │
│  │  - Always On: Enabled                                         │  │
│  └──────────────────────┬───────────────────────────────────────┘  │
│                         │                                           │
│         ┌───────────────┴───────────────┐                           │
│         │                                 │                           │
│  ┌──────┴──────────┐         ┌──────────┴────────┐                 │
│  │  PostgreSQL DB  │         │  Redis Cache       │                 │
│  │  (Managed)      │         │  (Background jobs) │                 │
│  └─────────────────┘         └────────────────────┘                 │
│                                                                       │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │  Azure Blob Storage (Attachments, photos)                     │  │
│  └──────────────────────────────────────────────────────────────┘  │
│                                                                       │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │  Application Insights (Monitoring & Logs)                     │  │
│  └──────────────────────────────────────────────────────────────┘  │
│                                                                       │
└─────────────────────────────────────────────────────────────────────┘
```

### CI/CD Pipeline (GitHub Actions)

```yaml
# .github/workflows/deploy.yml
name: Deploy to Azure

on:
  push:
    branches: [main, staging]

jobs:
  deploy:
    - Checkout code
    - Install dependencies
    - Run tests
    - Run linter
    - Build Next.js app
    - Run database migrations (if on main)
    - Deploy to Azure App Service
    - Run smoke tests
    - Notify team (Slack/Teams)
```

---

## Performance Considerations

### Caching Strategy
- **Redis**: Task lists, user dashboards (5 min TTL)
- **Next.js ISR**: Public pages (revalidate every 60s)
- **SWR**: Client-side data fetching with cache

### Database Optimization
- **Indexes**: On frequently queried fields (status, assigned_to, start_date)
- **Connection pooling**: Max 20 connections
- **Read replicas**: For reporting queries (future)

### Monitoring
- **Application Insights**: Response times, errors, dependencies
- **Custom metrics**: Onboardings created, tasks completed, avg time-to-complete
- **Alerts**: Error rate > 5%, response time > 2s, DB CPU > 80%

---

## Testing Strategy

### Unit Tests
- Business logic (workflow engine, task manager)
- Utility functions
- API route handlers

### Integration Tests
- Database operations (Prisma queries)
- API endpoints (request/response)
- Background jobs

### E2E Tests
- Critical user flows (Playwright):
  - Create new onboarding
  - Complete task
  - Advance phase
  - Generate report

### Manual Testing
- UAT with real users before launch
- Accessibility testing (screen readers, keyboard nav)
- Cross-browser testing (Chrome, Edge, Safari, Firefox)

---

## Monitoring & Maintenance

### Health Checks
```typescript
// /api/health
GET /api/health
{
  status: 'healthy',
  database: 'connected',
  redis: 'connected',
  version: '1.0.0',
  uptime: 3600
}
```

### Scheduled Maintenance
- **Database backups**: Daily automated backups, 30-day retention
- **Dependency updates**: Monthly security patches
- **Performance review**: Quarterly analysis of slow queries
- **User feedback review**: Bi-weekly ticket triage

### Support
- **Slack channel**: #batten-onboarding-support
- **Email**: battensupport@virginia.edu
- **Documentation**: Internal wiki with FAQs and troubleshooting

---

## Migration Plan

### Phase 1: Data Preparation (Week 1)
- Export existing onboarding records from current system
- Map to new database schema
- Validate data integrity

### Phase 2: Parallel Running (Weeks 2-3)
- New system deployed but not primary
- Select users test new system
- Compare results with old system
- Fix bugs and issues

### Phase 3: Soft Launch (Week 4)
- Make new system primary
- Keep old system available as backup
- Monitor closely for issues
- Quick rollback plan ready

### Phase 4: Full Cutover (Week 5+)
- Disable old system
- All new onboardings in new system
- Archive old system data
- Celebrate! 🎉

---

## Open Questions / To Decide

1. **Monday.com decision**: Final call on whether to integrate or replace entirely
2. **HR data feed**: Can we get automated feed? If not, manual entry acceptable?
3. **Canvas API access**: Do we have credentials? Need to request?
4. **Building access system**: What system does UVA use? Do they have API?
5. **Email service**: Use SendGrid or UVA mail servers? Deliverability concerns?
6. **Budget approval**: What's the approved budget for Azure resources?
7. **Timeline**: When does James need this by? Q3 2026? Q4 2026?

---

**Next Step:** Review this architecture with Mark Outten, James Cathro, and team for feedback and approval.
