# Quick Wins - Onboarding System

**Date:** 2026-06-12  
**Goal:** Immediate improvements while planning the full redesign

---

## Context

Based on Mark Outten's email, the current system has broken down and needs immediate fixes. Rather than waiting months for the full rebuild, we can implement these quick wins to provide value NOW while planning the larger solution.

**Timeline:** Implement these in the next 2-4 weeks

---

## Quick Win #1: Connect Form to Operations Team

### Problem
Form submissions only go to IT. Operations team (Sean Michael's team) doesn't get notified about keys, office setup, etc.

### Solution
Add Operations email notification when form is submitted.

### Implementation
```typescript
// In your existing form submission handler
async function handleFormSubmission(data: OnboardingFormData) {
  // Existing: Create ticket
  await createTicket(data);
  
  // Existing: Email to hiring manager
  await sendEmail({
    to: data.managerEmail,
    subject: 'Onboarding Form Submitted',
    template: 'manager-confirmation',
    data
  });
  
  // Existing: Email to new hire
  await sendEmail({
    to: data.employeeEmail,
    subject: 'Welcome to Batten School',
    template: 'new-hire-welcome',
    data
  });
  
  // NEW: Email to Operations team
  await sendEmail({
    to: 'sean.michael@virginia.edu', // Or ops-team@virginia.edu
    subject: `New Hire: ${data.employeeName} - Start ${data.startDate}`,
    template: 'ops-notification',
    data: {
      ...data,
      officeNeeded: true,
      keysNeeded: true,
      businessCardsNeeded: true,
      accessBuildings: ['Garrett Hall', 'Gibson Hall']
    }
  });
}
```

### Effort
⏱️ **2-4 hours**

### Value
✅ Operations team gets immediate visibility  
✅ Prevents keys/office setup from falling through cracks  
✅ Reduces manual forwarding of emails

---

## Quick Win #2: Auto-Enroll in Canvas Onboarding Course

### Problem
New hires not being enrolled in Canvas onboarding course (managers reporting this issue).

### Solution
Automated enrollment via Canvas API when form is submitted.

### Implementation

#### Step 1: Get Canvas API Token
Contact UVA IT to get API credentials for Canvas LMS.

#### Step 2: Create Canvas Service
```typescript
// src/services/canvas.service.ts
import axios from 'axios';

const CANVAS_API_BASE = 'https://canvas.virginia.edu/api/v1';
const CANVAS_API_TOKEN = process.env.CANVAS_API_TOKEN;
const ONBOARDING_COURSE_ID = process.env.CANVAS_ONBOARDING_COURSE_ID; // Get from Canvas

export async function enrollInOnboardingCourse(
  email: string,
  name: string
): Promise<void> {
  try {
    // 1. Find or create user in Canvas
    const user = await findOrCreateCanvasUser(email, name);
    
    // 2. Enroll in onboarding course
    await axios.post(
      `${CANVAS_API_BASE}/courses/${ONBOARDING_COURSE_ID}/enrollments`,
      {
        enrollment: {
          user_id: user.id,
          type: 'StudentEnrollment',
          enrollment_state: 'active',
          notify: true // Send Canvas notification
        }
      },
      {
        headers: {
          'Authorization': `Bearer ${CANVAS_API_TOKEN}`
        }
      }
    );
    
    console.log(`Enrolled ${email} in Canvas onboarding course`);
  } catch (error) {
    console.error('Canvas enrollment failed:', error);
    // Log but don't fail the whole onboarding process
    // Send notification to admin to enroll manually
  }
}
```

#### Step 3: Call from Form Handler
```typescript
async function handleFormSubmission(data: OnboardingFormData) {
  // ... existing code ...
  
  // NEW: Auto-enroll in Canvas
  await enrollInOnboardingCourse(data.employeeEmail, data.employeeName);
}
```

### Effort
⏱️ **4-8 hours** (includes Canvas API setup)

### Value
✅ Fixes reported issue immediately  
✅ New hires get onboarding materials on Day 1  
✅ Reduces manual work for whoever was doing this manually

---

## Quick Win #3: Manager Dashboard (Read-Only)

### Problem
Managers can't see status of their team's onboardings.

### Solution
Simple dashboard showing onboardings for their direct reports.

### Implementation

#### Step 1: Add Dashboard Route
```typescript
// app/dashboard/manager/[managerId]/page.tsx
import { getOnboardingsForManager } from '@/lib/onboarding';

export default async function ManagerDashboard({ 
  params 
}: { 
  params: { managerId: string } 
}) {
  const onboardings = await getOnboardingsForManager(params.managerId);
  
  return (
    <div className="container mx-auto p-6">
      <h1 className="text-3xl font-bold mb-6">My Team Onboardings</h1>
      
      {onboardings.map(onboarding => (
        <div key={onboarding.id} className="bg-white shadow rounded-lg p-6 mb-4">
          <h2 className="text-xl font-semibold">{onboarding.employeeName}</h2>
          <p className="text-gray-600">{onboarding.title}</p>
          <p className="text-sm text-gray-500">Start Date: {onboarding.startDate}</p>
          
          <div className="mt-4">
            <h3 className="font-medium mb-2">Submitted Information:</h3>
            <ul className="text-sm space-y-1">
              <li>✓ Form submitted: {onboarding.submittedDate}</li>
              <li>✓ IT notified</li>
              <li>✓ Operations notified</li>
              <li>✓ Welcome email sent</li>
            </ul>
          </div>
          
          <div className="mt-4 p-4 bg-blue-50 rounded">
            <p className="text-sm text-blue-800">
              <strong>What's Next:</strong> IT will contact you to coordinate 
              computer delivery. Operations will reach out about office assignment 
              and keys.
            </p>
          </div>
        </div>
      ))}
      
      {onboardings.length === 0 && (
        <p className="text-gray-600">No active onboardings for your team.</p>
      )}
    </div>
  );
}
```

#### Step 2: Add Database Query
```typescript
// lib/onboarding.ts
export async function getOnboardingsForManager(managerId: string) {
  return await prisma.onboardings.findMany({
    where: {
      managerId: managerId,
      status: 'active'
    },
    orderBy: {
      startDate: 'asc'
    }
  });
}
```

#### Step 3: Add Link from Navigation
```typescript
// In main nav, check if user is a manager
{session.user.roles.includes('manager') && (
  <Link href={`/dashboard/manager/${session.user.computingId}`}>
    My Team Onboardings
  </Link>
)}
```

### Effort
⏱️ **4-6 hours**

### Value
✅ Managers can see their team's onboardings  
✅ Reduces "where are we?" emails  
✅ Simple read-only view (no complex workflow yet)

---

## Quick Win #4: Start Date Reminders

### Problem
Onboardings slip through cracks, not ready by start date.

### Solution
Automated email reminders to relevant parties.

### Implementation

#### Step 1: Create Reminder Service
```typescript
// src/services/reminders.service.ts
export async function sendStartDateReminders() {
  const today = new Date();
  const oneWeekFromNow = addDays(today, 7);
  const threeDaysFromNow = addDays(today, 3);
  const tomorrow = addDays(today, 1);
  
  // Get onboardings starting soon
  const upcomingOnboardings = await prisma.onboardings.findMany({
    where: {
      startDate: {
        in: [oneWeekFromNow, threeDaysFromNow, tomorrow]
      },
      status: 'active'
    }
  });
  
  for (const onboarding of upcomingOnboardings) {
    const daysUntil = differenceInDays(onboarding.startDate, today);
    
    // Send to manager
    await sendEmail({
      to: `${onboarding.managerId}@virginia.edu`,
      subject: `Reminder: ${onboarding.employeeName} starts in ${daysUntil} days`,
      template: 'manager-reminder',
      data: { onboarding, daysUntil }
    });
    
    // Send to IT (if computer not marked as delivered)
    await sendEmail({
      to: 'battensupport@virginia.edu',
      subject: `Reminder: ${onboarding.employeeName} needs computer by ${onboarding.startDate}`,
      template: 'it-reminder',
      data: { onboarding, daysUntil }
    });
    
    // Send to Operations (if keys not marked as issued)
    await sendEmail({
      to: 'sean.michael@virginia.edu',
      subject: `Reminder: ${onboarding.employeeName} needs office/keys by ${onboarding.startDate}`,
      template: 'ops-reminder',
      data: { onboarding, daysUntil }
    });
  }
}
```

#### Step 2: Set Up Daily Cron Job
```typescript
// Using Vercel Cron or Azure Functions Timer
// cron/reminders.ts
export default async function handler(req: Request) {
  // Verify cron secret
  if (req.headers.get('authorization') !== `Bearer ${process.env.CRON_SECRET}`) {
    return new Response('Unauthorized', { status: 401 });
  }
  
  await sendStartDateReminders();
  
  return new Response('Reminders sent', { status: 200 });
}

// vercel.json
{
  "crons": [{
    "path": "/api/cron/reminders",
    "schedule": "0 8 * * *" // 8 AM daily
  }]
}
```

### Effort
⏱️ **3-5 hours**

### Value
✅ Proactive reminders prevent last-minute scrambles  
✅ Everyone knows what's coming up  
✅ Reduces "oh no, they start tomorrow!" situations

---

## Quick Win #5: Submission Confirmation Page with Checklist

### Problem
After submitting form, manager doesn't know what happens next.

### Solution
Show clear "What Happens Next" checklist after submission.

### Implementation

```typescript
// app/onboarding/success/page.tsx
export default function OnboardingSuccess({ 
  searchParams 
}: { 
  searchParams: { name: string; startDate: string } 
}) {
  return (
    <div className="container mx-auto max-w-2xl p-6">
      <div className="bg-green-50 border-2 border-green-500 rounded-lg p-6 mb-6">
        <h1 className="text-2xl font-bold text-green-800 mb-2">
          ✓ Onboarding Form Submitted
        </h1>
        <p className="text-green-700">
          We've received the onboarding request for {searchParams.name} 
          (start date: {searchParams.startDate}).
        </p>
      </div>
      
      <div className="bg-white shadow rounded-lg p-6">
        <h2 className="text-xl font-semibold mb-4">What Happens Next</h2>
        
        <div className="space-y-4">
          <div className="flex items-start">
            <div className="flex-shrink-0 w-8 h-8 bg-blue-100 rounded-full flex items-center justify-center mr-3">
              <span className="text-blue-800 font-bold">1</span>
            </div>
            <div>
              <h3 className="font-medium">IT Will Contact You (1-2 days)</h3>
              <p className="text-sm text-gray-600">
                Batten IT will reach out to coordinate computer delivery and 
                account setup. They'll need to know preferred delivery date/time.
              </p>
            </div>
          </div>
          
          <div className="flex items-start">
            <div className="flex-shrink-0 w-8 h-8 bg-blue-100 rounded-full flex items-center justify-center mr-3">
              <span className="text-blue-800 font-bold">2</span>
            </div>
            <div>
              <h3 className="font-medium">Operations Will Coordinate Space (1 week before start)</h3>
              <p className="text-sm text-gray-600">
                Operations team will assign office space and schedule key pickup. 
                You'll receive an email with office location and instructions.
              </p>
            </div>
          </div>
          
          <div className="flex items-start">
            <div className="flex-shrink-0 w-8 h-8 bg-blue-100 rounded-full flex items-center justify-center mr-3">
              <span className="text-blue-800 font-bold">3</span>
            </div>
            <div>
              <h3 className="font-medium">New Hire Receives Welcome Email</h3>
              <p className="text-sm text-gray-600">
                {searchParams.name} has been sent a welcome email with information 
                about IT setup, parking, and first-day logistics.
              </p>
            </div>
          </div>
          
          <div className="flex items-start">
            <div className="flex-shrink-0 w-8 h-8 bg-blue-100 rounded-full flex items-center justify-center mr-3">
              <span className="text-blue-800 font-bold">4</span>
            </div>
            <div>
              <h3 className="font-medium">Canvas Course Enrollment</h3>
              <p className="text-sm text-gray-600">
                {searchParams.name} has been enrolled in the Batten Onboarding 
                course in Canvas, where they can complete pre-start orientation 
                materials.
              </p>
            </div>
          </div>
        </div>
        
        <div className="mt-6 p-4 bg-gray-50 rounded">
          <h3 className="font-medium mb-2">Need Help?</h3>
          <p className="text-sm text-gray-600">
            Questions about the onboarding process? Contact{' '}
            <a href="mailto:battensupport@virginia.edu" className="text-blue-600 hover:underline">
              battensupport@virginia.edu
            </a>
          </p>
        </div>
      </div>
      
      <div className="mt-6 text-center">
        <a 
          href="/dashboard/manager" 
          className="text-blue-600 hover:underline"
        >
          View My Team Onboardings →
        </a>
      </div>
    </div>
  );
}
```

### Effort
⏱️ **2-3 hours**

### Value
✅ Sets clear expectations for managers  
✅ Reduces "what now?" questions  
✅ Shows professional, organized process

---

## Quick Win #6: Email Digest for IT/Ops Teams

### Problem
IT and Ops teams get individual emails for each onboarding, inbox gets cluttered.

### Solution
Daily digest email with all pending tasks.

### Implementation

```typescript
// src/services/digest.service.ts
export async function sendDailyDigest() {
  const today = new Date();
  const twoWeeksFromNow = addDays(today, 14);
  
  // Get upcoming onboardings
  const upcoming = await prisma.onboardings.findMany({
    where: {
      startDate: {
        gte: today,
        lte: twoWeeksFromNow
      },
      status: 'active'
    },
    orderBy: {
      startDate: 'asc'
    }
  });
  
  if (upcoming.length === 0) return;
  
  // Send to IT team
  await sendEmail({
    to: 'battensupport@virginia.edu',
    subject: `Daily Onboarding Digest - ${upcoming.length} upcoming starts`,
    template: 'it-digest',
    data: { onboardings: upcoming, today }
  });
  
  // Send to Operations team
  await sendEmail({
    to: 'sean.michael@virginia.edu',
    subject: `Daily Onboarding Digest - ${upcoming.length} upcoming starts`,
    template: 'ops-digest',
    data: { onboardings: upcoming, today }
  });
}

// Email template: it-digest.html
<h2>Batten Onboarding Digest - {{formatDate today}}</h2>
<p>You have {{onboardings.length}} upcoming onboardings in the next 2 weeks:</p>

<table>
  <thead>
    <tr>
      <th>Name</th>
      <th>Title</th>
      <th>Start Date</th>
      <th>Days Until</th>
      <th>Status</th>
    </tr>
  </thead>
  <tbody>
    {{#each onboardings}}
    <tr>
      <td>{{this.employeeName}}</td>
      <td>{{this.title}}</td>
      <td>{{formatDate this.startDate}}</td>
      <td>{{daysUntil this.startDate}}</td>
      <td>
        {{#if this.computerDelivered}}✓{{else}}⏳{{/if}} Computer
        {{#if this.emailCreated}}✓{{else}}⏳{{/if}} Email
      </td>
    </tr>
    {{/each}}
  </tbody>
</table>
```

### Effort
⏱️ **3-4 hours**

### Value
✅ One email instead of many  
✅ Easy to scan upcoming work  
✅ Reduces email fatigue

---

## Quick Win Summary

| Quick Win | Effort | Value | Priority |
|-----------|--------|-------|----------|
| 1. Connect Form to Ops | 2-4 hrs | High | 🔥 **Critical** |
| 2. Canvas Auto-Enrollment | 4-8 hrs | High | 🔥 **Critical** |
| 3. Manager Dashboard | 4-6 hrs | Medium | 🎯 Important |
| 4. Start Date Reminders | 3-5 hrs | High | 🎯 Important |
| 5. Success Page Checklist | 2-3 hrs | Medium | ⭐ Nice-to-have |
| 6. Daily Digest Emails | 3-4 hrs | Medium | ⭐ Nice-to-have |
| **Total** | **18-30 hrs** | | **2-4 weeks** |

---

## Implementation Plan

### Week 1
- ✅ Quick Win #1: Connect Form to Ops (Critical - fixes reported issue)
- ✅ Quick Win #2: Canvas Auto-Enrollment (Critical - fixes reported issue)

### Week 2
- ✅ Quick Win #3: Manager Dashboard (Provides visibility Mark requested)
- ✅ Quick Win #4: Start Date Reminders (Prevents last-minute scrambles)

### Week 3
- ✅ Quick Win #5: Success Page (Improves manager experience)
- ✅ Quick Win #6: Daily Digest (Reduces email clutter)

### Week 4
- Testing and refinement
- Gather feedback from managers, IT, Ops teams
- Document any issues for full redesign

---

## Success Metrics for Quick Wins

### Track These
1. **Number of Canvas enrollment errors**: Should drop to 0
2. **Manager "where's my onboarding" emails**: Should reduce by 50%+
3. **Operations team feedback**: Do they feel more included?
4. **IT team feedback**: Do reminders help them prepare?
5. **Time from form submission to computer delivery**: Baseline measurement

### How to Measure
- **Weekly check-in** with Mark Outten
- **Monthly survey** to managers who submitted forms
- **Anecdotal feedback** from IT and Ops teams
- **Form submission → start date tracking** in database

---

## Next Steps After Quick Wins

Once these quick wins are deployed:

1. **Gather feedback** (2-3 weeks)
2. **Document pain points** that quick wins don't solve
3. **Validate full redesign plan** with stakeholders
4. **Get approval** from leadership (Ian via Mark)
5. **Begin MVP development** of full workflow system

The quick wins buy us time to plan the full solution properly while delivering immediate value.

---

**Note:** These quick wins are designed to be **non-breaking** and **additive**. They don't require major architectural changes to your existing portal. We're just adding notifications, dashboards, and automation on top of what already works.
