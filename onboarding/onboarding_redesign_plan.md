# Batten School Onboarding Process Redesign Plan

**Date:** 2026-06-12  
**Status:** Planning Phase  
**Current Site:** https://www.thebattenspace.org/onboarding

---

## 1. Current State Analysis

### Current Onboarding Form Structure
The existing onboarding site has a **4-step wizard form**:

#### Step 1: New Hire
- New Employee Name*
- Title*
- Employee Type* (dropdown: Faculty, Staff, Wage, Adjunct, Postdoc, Student worker, Contractor)
- Department / Team*
- Start Date*

#### Step 2: Contacts
*(Not yet captured - requires form progression)*

#### Step 3: Workspace & Equipment
*(Not yet captured - requires form progression)*

#### Step 4: Access & Logistics
*(Not yet captured - requires form progression)*

### Current Process Characteristics
- **Single-point submission**: One person submits all information upfront
- **Front-loaded data collection**: All information required before processing begins
- **Limited workflow visibility**: No clear tracking of post-submission tasks
- **Submitter context**: "Submitting as Ben Hartless (bh4hb@virginia.edu)"

---

## 2. Proposed State (From Spreadsheet)

### Phase Structure
The proposed process breaks onboarding into **5 sequential phases** with specific responsible parties and checkpoints:

#### **Phase 1: Pre-boarding**
*Approvals before hire can be processed*
- ✅ Search Approved
- ✅ Process Approved  
- ✅ Comp Approved
- ✅ Hire Approved

#### **Phase 2: Associate Dean for Admin**
*Initial hire data collection*
- Name
- Manager
- Non-UVA email address
- Start Date

#### **Phase 3: Manager**
*Manager-led welcome preparation*
- Assign Batten Buddy
- Office Assignment
- Onboarding Checklist Initiated

#### **Phase 4a: Information Technology**
*IT infrastructure setup*
- Computing Package (hardware)
- UVA Email account creation
- Add to appropriate distribution lists

#### **Phase 4b: Marketing and Communications**
*Public-facing presence*
- Welcome slide displayed
- Directory updated
- Welcome slide removed (after period)

#### **Phase 4c: Operations**
*Physical workspace and logistics*
- Office cleaned/furnished
- Business Cards ordered
- Space Access provisioned
- "Dare to Lead" program scheduled
- Keys issued
- Name-plates created
- Wayfinder guide updated

#### **Phase 4d: Finance**
*Financial systems access*
- Payroll costing established
- T&E card application
- Finance security roles requested

#### **Phase 5: Manager**
*Final manager-led onboarding activities*
- "Ground for Success" completed
- Security roles requested (application-specific)
- Training plan reviewed

### Proposed Process Characteristics
- **Multi-party workflow**: Different teams own different phases
- **Checkpoint-based progression**: Clear approval gates
- **Distributed responsibility**: Each department handles their domain
- **Trackable tasks**: Specific checkboxes for completion

---

## 3. Key Differences

| Aspect | Current System | Proposed System |
|--------|---------------|-----------------|
| **Entry Point** | Single form submission | Pre-boarding approvals first |
| **Data Flow** | All data collected upfront | Data collected as needed by each phase |
| **Responsibility** | One submitter provides everything | Distributed across departments |
| **Tracking** | Limited visibility post-submission | Detailed task tracking per department |
| **Approvals** | Implied/manual | Explicit checkpoints in system |
| **Equipment** | Requested in form | Separate IT package phase |
| **Physical Setup** | Combined section | Dedicated Operations phase |

---

## 4. Critical Gaps & Challenges

### Process Gaps
1. **No approval workflow**: Current system lacks pre-boarding approval tracking
2. **Single point of failure**: All data must come from one submitter who may not have all information
3. **No progress visibility**: After submission, unclear what's happening or what's complete
4. **No role-based access**: Everyone sees the same form, regardless of their role in the process
5. **Manual coordination required**: Teams must manually coordinate outside the system
6. **No notification system**: No automated alerts when tasks are ready or complete

### Technical Challenges
1. **State management**: Need to track progress across 5 phases and 30+ tasks
2. **Role-based UI**: Different interfaces for Admin, Manager, IT, MarComm, Operations, Finance
3. **Notification system**: Email/alert system for task assignments and completions
4. **Data consistency**: Ensuring one source of truth as multiple people update
5. **Access control**: Sensitive information (salary, roles) should be restricted
6. **Historical tracking**: Audit trail of who did what and when

### Integration Needs
1. **UVA HR Systems**: Pull approved hire data rather than manual entry
2. **Active Directory**: Automate email account creation
3. **Distribution Lists**: Automatically manage email group memberships
4. **Card Access System**: Direct integration for building access
5. **Finance Systems**: Workday/banner integration for costing strings
6. **Calendar Systems**: Schedule onboarding events automatically

---

## 5. Stakeholder Roles

Based on the proposed process, key stakeholders include:

- **Associate Dean for Admin**: Initiates process with hire details
- **Hiring Manager**: Assigns buddy, office, initiates checklist, completes training
- **IT Team**: Provisions computing, email, distros
- **Marketing & Communications**: Updates directory, welcome slide, comms materials
- **Operations Team**: Prepares physical space, orders cards, manages keys
- **Finance Team**: Sets up payroll, T&E cards, role access
- **Batten Buddy**: Welcome and orientation support

---

## 6. Implementation Considerations

### Option A: Incremental Enhancement
*Enhance existing form with workflow features*

**Pros:**
- Faster to implement
- Maintains familiar interface
- Lower development cost

**Cons:**
- May not fully address workflow needs
- Harder to add complex role-based features
- Risk of tech debt

### Option B: Full Rebuild
*Build new multi-phase workflow system*

**Pros:**
- Purpose-built for the new process
- Better role-based experience
- Cleaner architecture for future expansion

**Cons:**
- Longer development timeline
- Higher upfront cost
- More disruptive transition

### Option C: Hybrid Approach
*Keep existing form as "quick submit" but build workflow system for tracking*

**Pros:**
- Preserves simple entry point
- Adds robust tracking and collaboration
- Phased rollout possible

**Cons:**
- Two systems to maintain
- Potential data sync issues
- More complex architecture

---

## 7. Questions for Stakeholders

### Process Questions
1. Does **every** hire go through all 5 phases, or do some skip certain steps? (e.g., contractors don't need keys)
2. What triggers the start of Phase 1? Is there a system of record for open searches?
3. Can Phase 4 tasks (IT/MarComm/Ops/Finance) happen in parallel, or must they be sequential?
4. Who is responsible for verifying that **all** tasks in a phase are complete before moving forward?
5. What happens if a hire's start date changes mid-process?

### Access & Security Questions
6. Who should be able to see the full onboarding status? (Just manager? Admin? Everyone involved?)
7. Should hiring managers see compensation/finance details?
8. How long should historical onboarding records be retained?

### Integration Questions
9. What's the source of truth for new hires? (Slate? Workday? PeopleAdmin?)
10. Can we get automated notifications from UVA HR when hires are approved?
11. Do we have API access to building access systems?
12. Can we automate email group management via Microsoft Graph API?

### Email Context (From Mark Outten - Jun 11, 2026)

**Current Pain Points Identified:**
13. **Process has become inconsistent over time** - multiple attempts to fix, keeps breaking down
14. **Form only being used by IT** - Not making its way to Operations team for keys/access
15. **Canvas course enrollment not happening** - Managers report new hires not being added to onboarding course
16. **No visibility for managers** - Can't see where onboarding process stands for their people
17. **Small steps not tracked** - Need every task assigned and visible

**Proposed Solution Elements (from Mark/James):**
- **HR data feed for dates** - Automate start/end date population when contracts signed
- **Monday.com for task tracking** - Team already has accounts
- **Open system** - Managers need full visibility into process status
- **Team effort needed** - IT, Operations, James/Maggie, potentially Beth Hill (HR)
- **Weekly reporting to Ian** - Process will be on leadership agenda

**Key Stakeholders Mentioned:**
- James Cathro (leading the redesign)
- Mark Outten (IT Director)
- Sean Michael and his team (Operations)
- Maggie
- Beth Hill (HR)
- Ian (leadership - weekly check-ins)

---

## 8. Current System Issues (From Email Context)

Based on Mark Outten's email (June 11, 2026), the existing system has these specific failures:

### What's Broken Right Now
1. **Form exists but isolated**: MS Form converted to online portal at thebattenspace.org/onboarding
   - Currently does 3 things:
     - Sends confirmation to hiring manager
     - Sends welcome email to incoming employee about IT needs
     - Creates a ticket with collected information
   
2. **Information not reaching Operations**: Form data stays with IT, doesn't flow to Ops team for keys/access/setup

3. **Canvas course not being populated**: New hires supposed to be enrolled in orientation course, but managers report it's not happening

4. **No visibility**: Managers can't see onboarding progress or status

5. **Small tasks not tracked**: Granular steps (keys, cards, access, etc.) have no tracking

6. **Recurring problem**: This is a "here we are again" situation - been fixed before, breaks down over time

### What They Want Instead
- **HR data feed**: Automatically pull start/end dates when contracts signed (instead of manual entry)
- **Monday.com for tasks**: Use existing tool team already has access to
- **Manager visibility**: "Open system" where managers can inspect full process
- **Every step assigned and tracked**: Maximum insight into granular progress
- **Weekly leadership reporting**: Ian wants updates each week

### Your Current Progress (Ben)
- ✅ Built online portal to replace MS Form
- ✅ Automated confirmation to hiring manager
- ✅ Automated welcome email to new hire
- ✅ Ticket creation with form data
- ⏳ Need to expand beyond IT-only workflow

## 9. Next Steps

### Immediate Actions (Week 1-2)
- [ ] **Coordinate with James Cathro** - He's leading this, will schedule meetings
- [ ] **Connect portal to Operations** - Make form data flow to Sean Michael's team
- [ ] **Monday.com vs. Portal decision** - Evaluate whether to build in Monday.com or extend your portal
- [ ] **HR data feed investigation** - Work with Beth Hill on auto-populating start dates
- [ ] **Fix Canvas course enrollment** - Automate new hire enrollment
- [ ] **Manager dashboard design** - Build visibility for hiring managers

### Planning Phase Tasks (Week 3-4)
- [x] Define which option (A/B/C) best fits needs and resources
- [x] Create mockups for each role's interface
- [ ] Draft technical architecture
- [ ] Create detailed user stories for each role
- [ ] Estimate development timeline and resources
- [ ] Identify quick wins vs. long-term improvements
- [ ] Design notification/email templates

### Before Development (Week 5+)
- [ ] Get leadership approval on scope and approach (present to Ian via Mark)
- [ ] Confirm budget and timeline expectations
- [ ] Establish success metrics
- [ ] Plan pilot group for initial rollout
- [ ] Prepare training materials and documentation

---

## 9. Success Metrics

How will we know the new process is working?

- **Time to onboard**: Days from hire approval to fully operational
- **Task completion rate**: % of checklist items completed on time
- **Stakeholder satisfaction**: Survey scores from hiring managers and new hires
- **Error reduction**: Fewer missing items or last-minute scrambles
- **Visibility**: Can admin/managers answer "what's the status?" at any time
- **Compliance**: 100% completion of required tasks (e.g., security training)

---

## 10. Risk Mitigation

| Risk | Impact | Likelihood | Mitigation |
|------|--------|------------|------------|
| Stakeholder adoption resistance | High | Medium | Early involvement, phased rollout, training |
| Integration complexity | High | High | Start with manual workflows, add automation incrementally |
| Data quality issues | Medium | Medium | Validation rules, required fields, data import tools |
| Timeline overruns | Medium | High | Start with MVP, add features iteratively |
| UVA IT policy conflicts | High | Low | Early consultation with ITS, compliance review |

---

## Appendix: Sample Onboarding Record from Spreadsheet

**Example:** Jenn Sublette  
- **ID:** 1
- **Approvals:** Search ✓, Process ✓, Comp ✓, Hire ✓
- **Manager:** Amanda Crombie
- **Email:** jennifer.sublette@gmail.com (external)
- **Start Date:** 2026-06-15
- **Batten Buddy:** Anne Carter Mulligan
- **Status Tracking:**
  - ✅ Onboarding Checklist Initiated
  - ✅ Computing Package assigned
  - ✅ UVA Email (jas4f@virginia.edu)
  - ✅ Business Cards ordered
  - ✅ Space Access provisioned
  - ✅ Keys issued
  - ✅ Name-plates created
  - ✅ Wayfinder guide updated
  - ⏳ Other items pending

This shows the level of detail tracking needed in the new system.
