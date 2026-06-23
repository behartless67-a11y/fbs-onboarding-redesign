# Quick Start Guide - What to Do NOW

**Last Updated:** 2026-06-12

---

## 🎯 TODAY - Next 2 Hours

### Action 1: Email James Cathro (5 minutes)

Copy/paste this:

```
To: James Cathro
Cc: Mark Outten
Subject: Onboarding Redesign - Complete Plan Ready

Hey James,

I saw Mark's email about fixing the onboarding process. I've already built 
the initial portal (thebattenspace.org/onboarding), and I've put together 
a complete plan to expand it into the full workflow system you need.

I have:
✓ Quick wins (2-4 weeks) - fixes immediate issues Mark mentioned
✓ Long-term roadmap (3-7 months) - full 5-phase workflow
✓ Mockups for all user roles
✓ Technical architecture and cost breakdown

The real cost is just ~$100/month for infrastructure (everything else is 
internal resources we already have). We'll save $10-18k/year in staff time.

Can we schedule 30 minutes this week to review? Happy to walk through the 
plan and align on priorities.

Documents are ready whenever you want them.

Thanks,
Ben
```

---

## 🔧 THIS WEEK - Quick Win #1 (2-4 hours)

### Fix: Form Not Reaching Operations Team

**What:** Add Operations team to email notifications when form is submitted

**Where:** Your existing form submission handler

**Steps:**

#### 1. Find Your Form Handler
Look for the file that processes form submissions. Probably something like:
- `app/api/onboarding/submit/route.ts` or
- `pages/api/onboarding/submit.js` or
- `lib/onboarding.ts`

#### 2. Add Operations Email
Find where you send confirmation emails. Add this:

```typescript
// After your existing email sends...

// NEW: Notify Operations team
await sendEmail({
  to: 'sean.michael@virginia.edu', // Or ops-team distro
  subject: `New Hire Onboarding: ${formData.employeeName}`,
  template: 'ops-notification',
  data: {
    employeeName: formData.employeeName,
    title: formData.title,
    department: formData.department,
    startDate: formData.startDate,
    manager: formData.managerName,
    managerEmail: formData.managerEmail,
    
    // What Operations needs to know
    officeNeeded: true,
    keysNeeded: true,
    businessCardsNeeded: true,
    buildingAccess: ['Garrett Hall', 'Gibson Hall'],
    
    // Link to form submission
    submissionUrl: `https://thebattenspace.org/onboarding/submissions/${submissionId}`
  }
});
```

#### 3. Create Email Template (if needed)

If you don't have templates set up, just send a simple HTML email:

```typescript
await sendEmail({
  to: 'sean.michael@virginia.edu',
  subject: `New Hire Onboarding: ${formData.employeeName}`,
  html: `
    <h2>New Hire Onboarding Submitted</h2>
    
    <p><strong>A new onboarding form has been submitted.</strong></p>
    
    <h3>Employee Information</h3>
    <ul>
      <li><strong>Name:</strong> ${formData.employeeName}</li>
      <li><strong>Title:</strong> ${formData.title}</li>
      <li><strong>Department:</strong> ${formData.department}</li>
      <li><strong>Start Date:</strong> ${formData.startDate}</li>
      <li><strong>Manager:</strong> ${formData.managerName} (${formData.managerEmail})</li>
    </ul>
    
    <h3>Operations Tasks Needed</h3>
    <ul>
      <li>☐ Assign office space</li>
      <li>☐ Order business cards</li>
      <li>☐ Arrange building access (Garrett Hall, Gibson Hall)</li>
      <li>☐ Schedule key pickup</li>
      <li>☐ Add to Dare to Lead program</li>
      <li>☐ Order name-plate</li>
      <li>☐ Update wayfinder guide</li>
    </ul>
    
    <p><strong>Manager Contact:</strong> ${formData.managerEmail}</p>
    
    <p style="color: #666; font-size: 12px;">
      This email was automatically sent from the Batten Onboarding system.
    </p>
  `
});
```

#### 4. Test It
1. Fill out a test form submission
2. Check that Operations receives the email
3. Verify all info is correct
4. Check with Sean Michael: "Hey, did you get that test email? Does it have everything you need?"

#### 5. Deploy
```bash
# Commit changes
git add .
git commit -m "feat: Add Operations team notification to onboarding form"

# Push to staging first
git push origin staging

# Test on staging
# Then push to production
git push origin main
```

**Time:** 2-4 hours including testing

---

## 📧 NEXT FEW DAYS - Set Up Canvas Access

### Action: Get Canvas API Credentials

**Email UVA IT or your Canvas admin:**

```
Subject: Canvas API Access for Batten Onboarding Automation

Hi,

We're automating our new hire onboarding process at the Batten School 
and need to programmatically enroll new employees in our Canvas onboarding 
course.

Can we get:
1. Canvas API token/credentials
2. Course ID for our onboarding course
3. Documentation on the enrollment API

This will replace our current manual enrollment process that's been 
causing issues.

Thanks,
Ben Hartless
Batten IT
bh4hb@virginia.edu
```

Once you have credentials, Quick Win #2 is ready to implement (4-6 hours).

---

## 📅 NEXT WEEK - Meeting with James

### Prepare to Discuss

**Share in advance:**
- [onboarding_redesign_plan.md](./onboarding_redesign_plan.md)
- [quick_wins.md](./quick_wins.md)
- [cost_breakdown.md](./cost_breakdown.md)

**Agenda for 30-minute meeting:**
1. Walk through current issues (5 min)
2. Show quick wins plan (10 min)
3. Preview long-term vision (5 min)
4. Discuss priorities and timeline (5 min)
5. Agree on next steps (5 min)

**Questions to Ask James:**
- What's the most urgent pain point to fix first?
- Do you want Monday.com integration or separate system?
- Who should be in the stakeholder review meeting?
- What's your target timeline for MVP?
- Do you have budget for $100/month infrastructure?

---

## 🎯 WEEK 2-4 - Implement Quick Wins

Based on James' priorities, implement in this order:

### Priority 1 (Week 1)
- [x] Connect form to Operations ← YOU CAN DO THIS TODAY
- [ ] Canvas auto-enrollment (needs API access first)

### Priority 2 (Week 2)
- [ ] Manager dashboard (read-only view)
- [ ] Start date reminders

### Priority 3 (Week 3-4)
- [ ] Success page with checklist
- [ ] Daily digest emails

---

## ✅ Success Criteria

You'll know Quick Wins are working when:

1. **Sean Michael confirms** - "Yes, I'm getting the form notifications now"
2. **No more Canvas enrollment complaints** - Managers stop reporting it
3. **Managers say** - "I can finally see where my onboarding is"
4. **Fewer last-minute scrambles** - Reminders keep everyone on track

---

## 🚨 If You Get Stuck

**Technical issues:**
- Check existing Batten Space codebase for email patterns
- Look at how you already send manager/new hire emails
- Test in staging first, always

**Political issues:**
- Loop in Mark Outten (he's supportive based on email)
- James is driving this, defer to his priorities
- Document everything so Ian can see progress

**Priority conflicts:**
- Talk to Mark: "I need 50% time on this for 3 months"
- Show the ROI: saving $10-18k/year in staff time
- Quick wins buy you credibility for bigger project

---

## 📞 Who to Contact

- **James Cathro** - Project lead, priorities, coordination
- **Mark Outten** - IT approval, resource allocation
- **Sean Michael** - Operations needs, testing Quick Win #1
- **Beth Hill** - HR data feed (later)
- **Canvas admin** - API access

---

## 🎉 Quick Win Timeline

```
Week 1:
├─ Today: Email James
├─ Today: Implement Quick Win #1 (2-4 hours)
├─ This week: Test with Operations
└─ This week: Request Canvas API access

Week 2:
├─ Meeting with James
├─ Implement Canvas enrollment
└─ Start manager dashboard

Week 3-4:
├─ Finish remaining quick wins
├─ Gather feedback
└─ Plan MVP kickoff

Total: 18-30 hours over 3-4 weeks
Cost: $0 out-of-pocket
```

---

**YOU CAN START RIGHT NOW** with Quick Win #1. It only takes 2-4 hours and immediately fixes the Operations team issue Mark mentioned. No approval needed - it's just adding an email notification to your existing form.

Get that deployed this week, and you'll have instant credibility that you can deliver on the bigger vision.

🚀 Go!
