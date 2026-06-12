# Onboarding Workflow Mockups

**Date:** 2026-06-12  
**Project:** Batten School Onboarding Process Redesign

---

## Overview

These mockups show the user experience for each role in the new 5-phase onboarding workflow system. The design prioritizes:
- **Clarity**: Users see only what's relevant to their role
- **Progress visibility**: Status always visible
- **Action-oriented**: Clear next steps and CTAs
- **Mobile-friendly**: Responsive design for all devices

---

## 1. Associate Dean Dashboard

### Purpose
Central command center for initiating and monitoring all onboardings.

### Layout

```
┌─────────────────────────────────────────────────────────────────────┐
│  The Batten Space                    [🔍 Search]  [Ben Hartless ▼]  │
├─────────────────────────────────────────────────────────────────────┤
│                                                                       │
│  📋 Onboarding Dashboard                                             │
│                                                                       │
│  ┌───────────────────────────────────────────────────────────────┐  │
│  │  Quick Stats                                                   │  │
│  │                                                                 │  │
│  │   [🟢 5 Active]  [🟡 3 Pending Approval]  [⚪ 12 Complete]    │  │
│  └───────────────────────────────────────────────────────────────┘  │
│                                                                       │
│  [+ New Hire]  [📊 Reports]  [📋 Export]                            │
│                                                                       │
│  ┌───────────────────────────────────────────────────────────────┐  │
│  │ 🔍 [Search by name...]    [Filter: All ▼]  [Sort: Start Date] │  │
│  └───────────────────────────────────────────────────────────────┘  │
│                                                                       │
│  ┌───────────────────────────────────────────────────────────────┐  │
│  │ Jenn Sublette                              🟢 Phase 4: In Prog │  │
│  │ Assistant Director | Staff | Marketing & Communications        │  │
│  │ Start: Jun 15, 2026 | Manager: Amanda Crombie                  │  │
│  │                                                                 │  │
│  │ ●●●●○○○○○○○○○●●○○○○○○●●●○○○○○○○              75% Complete    │  │
│  │ ▔▔▔▔▔▔▔▔▔▔▔▔▔                                                  │  │
│  │ Pre    Admin   Mgr     IT   MarCom  Ops  Finance  Final        │  │
│  │                                                                 │  │
│  │ Next: Operations (3 tasks) · Finance (2 tasks)    [View →]     │  │
│  └───────────────────────────────────────────────────────────────┘  │
│                                                                       │
│  ┌───────────────────────────────────────────────────────────────┐  │
│  │ Marcus Reynolds                            🟡 Phase 1: Pending │  │
│  │ Associate Professor | Faculty | Academic Programs              │  │
│  │ Start: Aug 20, 2026 | Manager: Sarah Chen                      │  │
│  │                                                                 │  │
│  │ ●●○○○○○○○○○○○○○○○○○○○○○○○○○○○○              15% Complete    │  │
│  │ ▔▔                                                              │  │
│  │ Pre    Admin   Mgr     IT   MarCom  Ops  Finance  Final        │  │
│  │                                                                 │  │
│  │ ⚠ Waiting: Process Approval                       [Review →]   │  │
│  └───────────────────────────────────────────────────────────────┘  │
│                                                                       │
│  ┌───────────────────────────────────────────────────────────────┐  │
│  │ Lisa Park                                  ⚪ Phase 5: Complete │  │
│  │ Operations Coordinator | Staff | Operations                    │  │
│  │ Start: May 28, 2026 | Manager: James Cathro                    │  │
│  │                                                                 │  │
│  │ ●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●             100% Complete   │  │
│  │ ▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔                              │  │
│  │ Pre    Admin   Mgr     IT   MarCom  Ops  Finance  Final        │  │
│  │                                                                 │  │
│  │ ✓ Completed May 27, 2026                          [Archive]    │  │
│  └───────────────────────────────────────────────────────────────┘  │
│                                                                       │
│  [< Previous]                                 1 of 3    [Next >]    │
│                                                                       │
└─────────────────────────────────────────────────────────────────────┘
```

### Key Features
- **Visual progress bar**: Shows completion across all phases
- **Status indicators**: Color-coded (green=active, yellow=pending, gray=complete)
- **Quick actions**: Start new hire, view reports
- **Smart filtering**: By status, department, date range
- **At-a-glance info**: Name, role, manager, start date in card format

---

## 2. New Hire Initiation Form (Associate Dean)

```
┌─────────────────────────────────────────────────────────────────────┐
│  ← Back to Dashboard                                                 │
├─────────────────────────────────────────────────────────────────────┤
│                                                                       │
│  Create New Hire Onboarding                                          │
│                                                                       │
│  ●━━━━━━○━━━━━━○━━━━━━○━━━━━━○                                      │
│  Phase 1    Phase 2   Confirm  Submit   Complete                     │
│  Pre-board  Details                                                   │
│                                                                       │
│  ┌───────────────────────────────────────────────────────────────┐  │
│  │                                                                 │  │
│  │  Phase 1: Pre-boarding Approvals                               │  │
│  │                                                                 │  │
│  │  Before we begin onboarding, confirm these approvals:          │  │
│  │                                                                 │  │
│  │  ☑ Search Approved                                             │  │
│  │    Date: Mar 15, 2026  Reference: SR-2026-0042                 │  │
│  │                                                                 │  │
│  │  ☑ Process Approved                                            │  │
│  │    Date: Apr 3, 2026   Reference: HR-2026-1124                 │  │
│  │                                                                 │  │
│  │  ☑ Compensation Approved                                       │  │
│  │    Date: Apr 18, 2026  Reference: FIN-2026-0567                │  │
│  │                                                                 │  │
│  │  ☑ Hire Approved                                               │  │
│  │    Date: May 2, 2026   Reference: OVR-2026-0089                │  │
│  │                                                                 │  │
│  │  [Upload Documentation] (Optional)                             │  │
│  │                                                                 │  │
│  └───────────────────────────────────────────────────────────────┘  │
│                                                                       │
│  [Cancel]                                            [Next: Details →]│
│                                                                       │
└─────────────────────────────────────────────────────────────────────┘

                              ↓ Next Screen ↓

┌─────────────────────────────────────────────────────────────────────┐
│  ← Back                                                               │
├─────────────────────────────────────────────────────────────────────┤
│                                                                       │
│  Create New Hire Onboarding                                          │
│                                                                       │
│  ●━━━━━━●━━━━━━○━━━━━━○━━━━━━○                                      │
│  Phase 1    Phase 2   Confirm  Submit   Complete                     │
│  ✓          Details                                                   │
│                                                                       │
│  ┌───────────────────────────────────────────────────────────────┐  │
│  │                                                                 │  │
│  │  Phase 2: New Hire Details                                     │  │
│  │                                                                 │  │
│  │  Employee Name *                                                │  │
│  │  [Jennifer Sublette                                         ]  │  │
│  │                                                                 │  │
│  │  Title *                                                        │  │
│  │  [Assistant Director of Marketing                           ]  │  │
│  │                                                                 │  │
│  │  Employee Type *                                                │  │
│  │  [Staff                                                      ▼] │  │
│  │                                                                 │  │
│  │  Department / Team *                                            │  │
│  │  [Marketing & Communications                                 ▼] │  │
│  │                                                                 │  │
│  │  Start Date *                                                   │  │
│  │  [06/15/2026                                               📅]  │  │
│  │                                                                 │  │
│  │  Non-UVA Email Address *                                        │  │
│  │  [jennifer.sublette@gmail.com                                ] │  │
│  │  (We'll use this until their UVA email is created)             │  │
│  │                                                                 │  │
│  │  Hiring Manager *                                               │  │
│  │  [Amanda Crombie                                             ▼] │  │
│  │                                                                 │  │
│  └───────────────────────────────────────────────────────────────┘  │
│                                                                       │
│  [← Back]                                            [Review →]      │
│                                                                       │
└─────────────────────────────────────────────────────────────────────┘
```

### Key Features
- **Wizard interface**: Multi-step with clear progress
- **Pre-boarding validation**: Must confirm approvals before proceeding
- **Smart defaults**: Department dropdown, manager lookup
- **Non-UVA email**: Captures external email for early communication
- **Reference tracking**: Links to approval documents

---

## 3. Manager Dashboard

```
┌─────────────────────────────────────────────────────────────────────┐
│  The Batten Space                    [🔍 Search]  [Amanda Crombie ▼]│
├─────────────────────────────────────────────────────────────────────┤
│                                                                       │
│  👥 My Team Onboardings                                              │
│                                                                       │
│  ┌───────────────────────────────────────────────────────────────┐  │
│  │  [📋 My Tasks]  [👥 Team View]  [📊 Timeline]                  │  │
│  └───────────────────────────────────────────────────────────────┘  │
│                                                                       │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  │
│  🔔 Action Required                                                   │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  │
│                                                                       │
│  ┌───────────────────────────────────────────────────────────────┐  │
│  │  ⚡ Jenn Sublette - Onboarding Phase 3                         │  │
│  │                                                                 │  │
│  │  You have 3 tasks to complete:                                 │  │
│  │                                                                 │  │
│  │  ☐  Assign Batten Buddy                                        │  │
│  │      Pair Jenn with a tenured staff member for first 90 days   │  │
│  │      [Assign Buddy]                                            │  │
│  │                                                                 │  │
│  │  ☐  Assign Office Space                                        │  │
│  │      Work with Operations to designate workspace               │  │
│  │      Current availability: Garrett 301, 307, Gibson 205        │  │
│  │      [View Floor Plans] [Assign Office]                        │  │
│  │                                                                 │  │
│  │  ☐  Initiate Onboarding Checklist                             │  │
│  │      Review and customize 30-60-90 day plan                    │  │
│  │      [Create Checklist]                                        │  │
│  │                                                                 │  │
│  │  Due: Jun 10, 2026 (3 days)                                    │  │
│  │                                                                 │  │
│  └───────────────────────────────────────────────────────────────┘  │
│                                                                       │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  │
│  📊 In Progress                                                       │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  │
│                                                                       │
│  ┌───────────────────────────────────────────────────────────────┐  │
│  │  Jenn Sublette · Assistant Director                            │  │
│  │  Start: Jun 15, 2026 (3 days away)                             │  │
│  │                                                                 │  │
│  │  Phase 3: Manager Setup      Phase 4: Departments  Phase 5     │  │
│  │  ●●○                          ○○○○○○○○○○○○○       ○○○          │  │
│  │  2 of 3 complete             Waiting              Not started  │  │
│  │                                                                 │  │
│  │  Recent Activity:                                              │  │
│  │  • ✓ Batten Buddy assigned (Anne Carter Mulligan) - Today     │  │
│  │  • ✓ Office assigned (Garrett 305) - Today                    │  │
│  │  • IT: Computing package ordered - Yesterday                   │  │
│  │  • IT: UVA email created (jas4f@virginia.edu) - Yesterday     │  │
│  │                                                                 │  │
│  │  [View Full Details →]                                         │  │
│  └───────────────────────────────────────────────────────────────┘  │
│                                                                       │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  │
│  ⏳ Upcoming                                                          │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  │
│                                                                       │
│  ┌───────────────────────────────────────────────────────────────┐  │
│  │  Marcus Reynolds · Associate Professor                         │  │
│  │  Start: Aug 20, 2026 (69 days)                                 │  │
│  │                                                                 │  │
│  │  Phase 1: Pre-boarding                                         │  │
│  │  ●●●○                                                           │  │
│  │  Waiting on: Process Approval                                  │  │
│  │                                                                 │  │
│  │  You'll be notified when Phase 3 is ready.                     │  │
│  └───────────────────────────────────────────────────────────────┘  │
│                                                                       │
└─────────────────────────────────────────────────────────────────────┘
```

### Key Features
- **Action-first design**: Tasks requiring action at top
- **Due dates**: Clear deadlines for manager tasks
- **Recent activity feed**: See what other departments have done
- **Phase progress**: Visual indicators for each onboarding stage
- **Countdown to start date**: Urgency indicator
- **Contextual help**: Suggestions (office availability, buddy matching)

---

## 4. IT Dashboard

```
┌─────────────────────────────────────────────────────────────────────┐
│  The Batten Space                    [🔍 Search]  [IT Admin ▼]      │
├─────────────────────────────────────────────────────────────────────┤
│                                                                       │
│  💻 IT Onboarding Tasks                                              │
│                                                                       │
│  ┌───────────────────────────────────────────────────────────────┐  │
│  │  [🔥 Urgent]  [📋 All Tasks]  [✓ Completed]  [📊 Analytics]   │  │
│  └───────────────────────────────────────────────────────────────┘  │
│                                                                       │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  │
│  🔥 Due This Week (3)                                                │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  │
│                                                                       │
│  ┌───────────────────────────────────────────────────────────────┐  │
│  │  Jenn Sublette                                                  │  │
│  │  Assistant Director | Staff | Start: Jun 15 (3 days)           │  │
│  │                                                                 │  │
│  │  ☑ Computing Package        ☑ UVA Email         ☐ Distros      │  │
│  │  ✓ MacBook Pro M3           ✓ jas4f@virginia.edu               │  │
│  │    External monitor                                             │  │
│  │    Keyboard, mouse          Sent welcome email                  │  │
│  │                                                                 │  │
│  │  ☐ Add to Distribution Lists (Action Required)                 │  │
│  │                                                                 │  │
│  │     Recommended based on role:                                 │  │
│  │     ☑ batten-staff@virginia.edu                                │  │
│  │     ☑ batten-marcomm@virginia.edu                              │  │
│  │     ☑ batten-leadership@virginia.edu                           │  │
│  │     ☐ batten-all@virginia.edu                                  │  │
│  │                                                                 │  │
│  │     [💾 Save & Notify]  [Add Custom...]                        │  │
│  │                                                                 │  │
│  │  📝 Notes: Requested dual monitors - ordered 2nd on 6/10       │  │
│  │            Manager: Amanda Crombie (arc9f@virginia.edu)        │  │
│  │                                                                 │  │
│  └───────────────────────────────────────────────────────────────┘  │
│                                                                       │
│  ┌───────────────────────────────────────────────────────────────┐  │
│  │  Lisa Martinez                                                  │  │
│  │  Program Coordinator | Staff | Start: Jun 18 (6 days)          │  │
│  │                                                                 │  │
│  │  ☐ Computing Package        ☐ UVA Email         ☐ Distros      │  │
│  │  Not started                Not started          Waiting        │  │
│  │                                                                 │  │
│  │  [🚀 Start Setup]                                              │  │
│  │                                                                 │  │
│  └───────────────────────────────────────────────────────────────┘  │
│                                                                       │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  │
│  ⏳ Coming Up (2)                                                    │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  │
│                                                                       │
│  • Marcus Reynolds (Faculty) - Aug 20                               │  │
│  • Tara Johnson (Postdoc) - Sep 1                                   │  │
│                                                                       │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  │
│  ✓ Recently Completed (5)                                            │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  │
│                                                                       │
│  • David Kim - All tasks complete (Jun 10)                          │  │
│  • Sarah Thompson - All tasks complete (Jun 8)                      │  │
│  • Rachel Green - All tasks complete (Jun 5)                        │  │
│                                                                       │
│  [View All →]                                                        │
│                                                                       │
└─────────────────────────────────────────────────────────────────────┘
```

### Key Features
- **Task-focused**: Shows only IT-relevant tasks
- **Smart suggestions**: Recommends distro lists based on role
- **Package tracking**: Hardware status and shipment info
- **Urgency indicators**: Due this week, coming up, completed
- **Quick actions**: Save and notify, start setup
- **Notes field**: Track special requests and communications
- **Manager contact**: Quick reference to reach out

---

## 5. Operations Dashboard

```
┌─────────────────────────────────────────────────────────────────────┐
│  The Batten Space                    [🔍 Search]  [Ops Team ▼]      │
├─────────────────────────────────────────────────────────────────────┤
│                                                                       │
│  🏢 Operations Onboarding Tasks                                      │
│                                                                       │
│  ┌───────────────────────────────────────────────────────────────┐  │
│  │  [🎯 My Tasks]  [🗂️ By Category]  [📍 By Location]            │  │
│  └───────────────────────────────────────────────────────────────┘  │
│                                                                       │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  │
│  🎯 Action Required                                                   │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  │
│                                                                       │
│  ┌───────────────────────────────────────────────────────────────┐  │
│  │  Jenn Sublette - Start: Jun 15, 2026                           │  │
│  │  Office: Garrett 305                                            │  │
│  │                                                                 │  │
│  │  ┌─────────────────────────────────────────────────────────┐  │  │
│  │  │ 🏢 Workspace                                             │  │  │
│  │  │                                                           │  │  │
│  │  │ ☑ Office cleaned/furnished                              │  │  │
│  │  │   ✓ Desk, chair, filing cabinet                         │  │  │
│  │  │   ✓ Cleaned 6/10                                        │  │  │
│  │  │   📸 [View Photos]                                       │  │  │
│  │  │                                                           │  │  │
│  │  │ ☑ Name-plate ordered                                    │  │  │
│  │  │   ✓ Order #OP-2026-0421                                 │  │  │
│  │  │   📦 Arriving Jun 14                                     │  │  │
│  │  │                                                           │  │  │
│  │  └─────────────────────────────────────────────────────────┘  │  │
│  │                                                                 │  │
│  │  ┌─────────────────────────────────────────────────────────┐  │  │
│  │  │ 🔑 Access & Keys                                         │  │  │
│  │  │                                                           │  │  │
│  │  │ ☐ Building Access (ACTION NEEDED)                       │  │  │
│  │  │   Buildings: Garrett Hall, Gibson Hall                   │  │  │
│  │  │   Hours: 6 AM - 10 PM                                    │  │  │
│  │  │   [🔒 Submit Access Request]                            │  │  │
│  │  │                                                           │  │  │
│  │  │ ☐ Office Keys                                           │  │  │
│  │  │   Waiting on: Building access approval                   │  │  │
│  │  │   [ ] Contact: UVA Facilities (after approval)          │  │  │
│  │  │                                                           │  │  │
│  │  └─────────────────────────────────────────────────────────┘  │  │
│  │                                                                 │  │
│  │  ┌─────────────────────────────────────────────────────────┐  │  │
│  │  │ 🎯 Programs & Materials                                  │  │  │
│  │  │                                                           │  │  │
│  │  │ ☑ Business cards ordered                                │  │  │
│  │  │   ✓ Design approved 6/8                                 │  │  │
│  │  │   📦 Arriving Jun 13                                     │  │  │
│  │  │                                                           │  │  │
│  │  │ ☐ Dare to Lead scheduled                                │  │  │
│  │  │   Next cohort: Jul 10-12, 2026                          │  │  │
│  │  │   [📅 Register Jenn]                                     │  │  │
│  │  │                                                           │  │  │
│  │  │ ☐ Wayfinder guide updated                               │  │  │
│  │  │   [📝 Add to Directory]                                  │  │  │
│  │  │                                                           │  │  │
│  │  └─────────────────────────────────────────────────────────┘  │  │
│  │                                                                 │  │
│  │  Progress: 4 of 8 complete                                     │  │
│  │  Due: Jun 14 (2 days before start)                             │  │
│  │                                                                 │  │
│  └───────────────────────────────────────────────────────────────┘  │
│                                                                       │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  │
│  ⏳ Upcoming (2)                                                     │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  │
│                                                                       │
│  • Lisa Martinez (Staff) - Start: Jun 18 - Office: Gibson 203       │  │
│  • Marcus Reynolds (Faculty) - Start: Aug 20 - Office: TBD          │  │
│                                                                       │
└─────────────────────────────────────────────────────────────────────┘
```

### Key Features
- **Grouped by category**: Workspace, Access, Programs
- **Dependency tracking**: Shows what's waiting on what
- **Deadline awareness**: Due date based on start date
- **Order tracking**: Links to vendor orders and tracking
- **Photo documentation**: Can upload workspace photos
- **Integration hooks**: Direct links to access request systems
- **Location-aware**: Office/building info prominent

---

## 6. Finance Dashboard

```
┌─────────────────────────────────────────────────────────────────────┐
│  The Batten Space                    [🔍 Search]  [Finance ▼]       │
├─────────────────────────────────────────────────────────────────────┤
│                                                                       │
│  💰 Finance Onboarding Tasks                                         │
│                                                                       │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  │
│  🔥 Pending Setup (2)                                                │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  │
│                                                                       │
│  ┌───────────────────────────────────────────────────────────────┐  │
│  │  Jenn Sublette                                                  │  │
│  │  Assistant Director | Staff | Start: Jun 15, 2026              │  │
│  │  Manager: Amanda Crombie (arc9f)                                │  │
│  │                                                                 │  │
│  │  ┌─────────────────────────────────────────────────────────┐  │  │
│  │  │ 💼 Payroll Setup                                         │  │  │
│  │  │                                                           │  │  │
│  │  │ ☑ Costing string established                            │  │  │
│  │  │   Fund: 3001-4200                                        │  │  │
│  │  │   Program: 6501                                          │  │  │
│  │  │   Approved by: Mark Outten                               │  │  │
│  │  │   ✓ Entered in Workday 6/9                              │  │  │
│  │  │                                                           │  │  │
│  │  └─────────────────────────────────────────────────────────┘  │  │
│  │                                                                 │  │
│  │  ┌─────────────────────────────────────────────────────────┐  │  │
│  │  │ 💳 T&E Card Application                                  │  │  │
│  │  │                                                           │  │  │
│  │  │ ☐ Travel & Expense Card (ACTION NEEDED)                 │  │  │
│  │  │   Amount approved: $5,000 limit                          │  │  │
│  │  │   Use case: Conference travel, office supplies          │  │  │
│  │  │                                                           │  │  │
│  │  │   [📋 Start Application]                                 │  │  │
│  │  │                                                           │  │  │
│  │  │   Required info:                                         │  │  │
│  │  │   ✓ Costing string                                       │  │  │
│  │  │   ✓ Manager approval                                     │  │  │
│  │  │   ⏳ UVA email (waiting on IT)                           │  │  │
│  │  │                                                           │  │  │
│  │  └─────────────────────────────────────────────────────────┘  │  │
│  │                                                                 │  │
│  │  ┌─────────────────────────────────────────────────────────┐  │  │
│  │  │ 🔐 System Access                                         │  │  │
│  │  │                                                           │  │  │
│  │  │ ☐ Finance security roles                                │  │  │
│  │  │   Systems needed:                                        │  │  │
│  │  │   ☑ Workday (Submitter)                                 │  │  │
│  │  │   ☐ Chrome River (Approver - $5k limit)                │  │  │
│  │  │   ☐ PaymentWorks (Vendor setup)                         │  │  │
│  │  │                                                           │  │  │
│  │  │   [🔒 Submit Role Requests]                             │  │  │
│  │  │                                                           │  │  │
│  │  └─────────────────────────────────────────────────────────┘  │  │
│  │                                                                 │  │
│  │  Progress: 1 of 3 complete                                     │  │
│  │  Due: Before start date (Jun 15)                               │  │
│  │                                                                 │  │
│  │  📝 Notes: Check with manager on Chrome River approval limit   │  │
│  │                                                                 │  │
│  └───────────────────────────────────────────────────────────────┘  │
│                                                                       │
│  ┌───────────────────────────────────────────────────────────────┐  │
│  │  Lisa Martinez                                                  │  │
│  │  Program Coordinator | Staff | Start: Jun 18, 2026             │  │
│  │                                                                 │  │
│  │  ☐ Payroll costing   ☐ T&E card   ☐ Security roles            │  │
│  │  Not started         Not started   Not started                 │  │
│  │                                                                 │  │
│  │  [🚀 Begin Setup]                                              │  │
│  │                                                                 │  │
│  └───────────────────────────────────────────────────────────────┘  │
│                                                                       │
└─────────────────────────────────────────────────────────────────────┘
```

### Key Features
- **Grouped by function**: Payroll, T&E cards, system access
- **Dependency indicators**: Shows what's waiting on other departments
- **Approval tracking**: Who approved what and when
- **System-specific**: Lists exact systems and role types needed
- **Pre-requisite checking**: Shows if UVA email is ready before card app
- **Notes for special cases**: Approval limits, special permissions

---

## 7. Marketing & Communications Dashboard

```
┌─────────────────────────────────────────────────────────────────────┐
│  The Batten Space                    [🔍 Search]  [MarComm ▼]       │
├─────────────────────────────────────────────────────────────────────┤
│                                                                       │
│  📢 Marketing & Communications Onboarding                            │
│                                                                       │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  │
│  🎨 Active Welcome Campaigns                                         │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  │
│                                                                       │
│  ┌───────────────────────────────────────────────────────────────┐  │
│  │  Jenn Sublette                                                  │  │
│  │  Assistant Director | Start: Jun 15, 2026                      │  │
│  │                                                                 │  │
│  │  ┌─────────────────────────────────────────────────────────┐  │  │
│  │  │ 🖼️ Welcome Slide                                          │  │  │
│  │  │                                                           │  │  │
│  │  │ ☑ Slide created & displayed                             │  │  │
│  │  │   ✓ Created: Jun 10                                     │  │  │
│  │  │   📺 Displaying: Garrett Lobby, Gibson Lobby            │  │  │
│  │  │   📅 Remove on: Jun 29 (2 weeks after start)            │  │  │
│  │  │                                                           │  │  │
│  │  │   [👁️ Preview Slide]  [📥 Download]  [🔄 Update]        │  │  │
│  │  │                                                           │  │  │
│  │  │   ┌───────────────────────────────────────────────┐     │  │  │
│  │  │   │                                                 │     │  │  │
│  │  │   │   Welcome, Jenn!                               │     │  │  │
│  │  │   │                                                 │     │  │  │
│  │  │   │   [Photo]                                       │     │  │  │
│  │  │   │                                                 │     │  │  │
│  │  │   │   Jenn Sublette                                │     │  │  │
│  │  │   │   Assistant Director of Marketing              │     │  │  │
│  │  │   │                                                 │     │  │  │
│  │  │   └───────────────────────────────────────────────┘     │  │  │
│  │  │                                                           │  │  │
│  │  └─────────────────────────────────────────────────────────┘  │  │
│  │                                                                 │  │
│  │  ┌─────────────────────────────────────────────────────────┐  │  │
│  │  │ 📇 Directory Updates                                     │  │  │
│  │  │                                                           │  │  │
│  │  │ ☑ Website directory updated                             │  │  │
│  │  │   ✓ Published to batten.virginia.edu/people             │  │  │
│  │  │   Profile includes: Bio, photo, contact info            │  │  │
│  │  │   [🔗 View Live Profile]                                │  │  │
│  │  │                                                           │  │  │
│  │  │ ☐ Additional channels (Optional)                        │  │  │
│  │  │   ☐ LinkedIn company page                               │  │  │
│  │  │   ☐ Internal newsletter announcement                    │  │  │
│  │  │   ☐ Social media welcome post                           │  │  │
│  │  │                                                           │  │  │
│  │  └─────────────────────────────────────────────────────────┘  │  │
│  │                                                                 │  │
│  │  Progress: 2 of 2 required (3 optional)                       │  │
│  │                                                                 │  │
│  │  🔔 Reminder: Remove welcome slide on Jun 29                   │  │
│  │                                                                 │  │
│  └───────────────────────────────────────────────────────────────┘  │
│                                                                       │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  │
│  ⏳ Upcoming (2)                                                     │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  │
│                                                                       │
│  • Lisa Martinez (Program Coordinator) - Start: Jun 18              │  │
│  • Marcus Reynolds (Associate Professor) - Start: Aug 20            │  │
│                                                                       │
└─────────────────────────────────────────────────────────────────────┘
```

### Key Features
- **Visual preview**: See the welcome slide design
- **Schedule reminders**: Auto-remind to remove slide after 2 weeks
- **Multi-channel tracking**: Website, social, newsletter options
- **Link to live content**: View published directory entry
- **Template system**: Reuse slide designs with new info
- **Optional enhancements**: Suggested but not required items

---

## 8. Mobile View (Example: Manager on Phone)

```
┌──────────────────────┐
│  ☰  Batten Space  🔔 │
├──────────────────────┤
│                      │
│  My Team Onboardings │
│                      │
│  ┌──────────────────┐│
│  │ 🔔 Action Needed ││
│  │                  ││
│  │ Jenn Sublette    ││
│  │ Due: 3 days      ││
│  │                  ││
│  │ 3 tasks →        ││
│  └──────────────────┘│
│                      │
│  ┌──────────────────┐│
│  │ In Progress      ││
│  │                  ││
│  │ Jenn Sublette    ││
│  │ Start: Jun 15    ││
│  │                  ││
│  │ ●●○○○○○○○○○     ││
│  │ 75% complete     ││
│  │                  ││
│  │ View details →   ││
│  └──────────────────┘│
│                      │
│  ┌──────────────────┐│
│  │ Upcoming         ││
│  │                  ││
│  │ Marcus Reynolds  ││
│  │ Start: Aug 20    ││
│  │                  ││
│  │ 69 days away     ││
│  └──────────────────┘│
│                      │
│  [+ New Hire]        │
│                      │
└──────────────────────┘
```

### Key Features
- **Touch-optimized**: Large tap targets
- **Priority-based**: Most urgent at top
- **Swipe actions**: Swipe card to mark complete
- **Progressive disclosure**: Tap to see details
- **Offline capable**: Cache for offline viewing

---

## Design System

### Colors
- **Primary**: UVA Blue (#232D4B)
- **Accent**: UVA Orange (#E57200)
- **Success**: Green (#2ECC71)
- **Warning**: Yellow (#F39C12)
- **Danger**: Red (#E74C3C)
- **In Progress**: Blue (#3498DB)
- **Complete**: Gray (#95A5A6)

### Typography
- **Headings**: Freight Sans Pro (UVA standard)
- **Body**: Source Sans Pro
- **Monospace**: Source Code Pro (for IDs/codes)

### Components
- **Progress Bars**: Segmented (one segment per phase)
- **Status Badges**: Pill-shaped with icon + text
- **Cards**: Elevated with shadow, rounded corners
- **Buttons**: Primary (filled), Secondary (outline), Ghost (text only)
- **Form Inputs**: Consistent height (48px touch target)

### Accessibility
- **WCAG 2.1 AA compliant**: All color contrasts meet standards
- **Keyboard navigation**: Full support
- **Screen reader**: Semantic HTML, ARIA labels
- **Focus indicators**: Visible on all interactive elements
- **Error states**: Clear, descriptive error messages

---

## Next Steps

1. **Validate with stakeholders**: Show these mockups to actual users
2. **Identify missing features**: What did we overlook?
3. **Prioritize for MVP**: Which screens are must-have vs. nice-to-have?
4. **Create interactive prototype**: Clickable version for user testing
5. **Build component library**: Reusable UI components in code

---

**Note**: These are wireframe mockups focused on functionality and information architecture. Final visual design will incorporate full UVA/Batten branding, photography, and polished UI elements per the [fbs-brand-kit](file-path) skill guidelines.
