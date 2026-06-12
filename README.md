# Batten School Onboarding Redesign - Planning Documents

**Date:** 2026-06-12  
**Status:** Planning Complete - Ready for Stakeholder Review

---

## 📋 Document Overview

This directory contains comprehensive planning documentation for redesigning the Batten School onboarding process.

### Core Documents

1. **[onboarding_redesign_plan.md](./onboarding_redesign_plan.md)** - Master plan
   - Current state analysis
   - Proposed 5-phase workflow
   - Key differences and gaps
   - Stakeholder roles
   - Success metrics

2. **[implementation_options_analysis.md](./implementation_options_analysis.md)** - Detailed comparison
   - Option A: Incremental Enhancement
   - Option B: Full Rebuild (RECOMMENDED)
   - Option C: Hybrid Approach
   - Timeline, budget, and resource estimates
   - Decision matrix

3. **[onboarding_mockups.md](./onboarding_mockups.md)** - UI/UX designs
   - Dashboard wireframes for each role
   - New hire initiation flow
   - Mobile-responsive designs
   - Design system specifications

4. **[technical_architecture.md](./technical_architecture.md)** - Technical specs
   - System architecture
   - Database schema
   - API endpoints
   - Integration points
   - Security model
   - Deployment plan

5. **[quick_wins.md](./quick_wins.md)** - Immediate actions
   - 6 quick wins (18-30 hours total)
   - Implementation plan (2-4 weeks)
   - Non-breaking, additive improvements

---

## 🎯 Key Recommendations

### Short Term (Next 2-4 Weeks)
Implement **Quick Wins** to address immediate pain points:
1. ✅ Connect form to Operations team
2. ✅ Auto-enroll in Canvas onboarding course
3. ✅ Build manager dashboard for visibility
4. ✅ Add start date reminders
5. ✅ Improve success page with clear next steps
6. ✅ Send daily digest emails to IT/Ops teams

### Long Term (3-7 Months)
Build **Modified Option B** (Phased Rebuild):
- **MVP (3 months)**: Core workflow tracking, manual processes
- **Phase 2 (2 months)**: Role-based dashboards, automation
- **Phase 3 (2 months)**: Integrations, polish, reporting

**Budget:** ~$50k MVP, ~$124k total
**Timeline:** MVP in 3 months, full system in 6-7 months

---

## 📊 Context from Email (Mark Outten - Jun 11, 2026)

### Problems Identified
- ❌ Form submissions not reaching Operations team
- ❌ Canvas course enrollment broken
- ❌ Managers have no visibility into onboarding status
- ❌ Small tasks not tracked (keys, cards, access)
- ❌ Process keeps breaking down over time

### Proposed Solutions
- HR data feed for automated start dates
- Monday.com for task tracking (team has accounts)
- Open system where managers can inspect progress
- Every step assigned and tracked
- Weekly reporting to Ian (leadership)

### Key Stakeholders
- **James Cathro** - Leading the redesign
- **Mark Outten** - IT Director
- **Sean Michael** - Operations lead
- **Ben Hartless** - Already built initial portal
- **Beth Hill** - HR liaison

---

## 🏗️ Proposed System Overview

### Current System
- Single form at [thebattenspace.org/onboarding](https://www.thebattenspace.org/onboarding)
- Sends confirmation to manager
- Sends welcome to new hire
- Creates IT ticket
- **Limited** to IT workflow only

### Proposed System
**5-Phase Workflow:**
1. **Pre-boarding** - Approvals (Search, Process, Comp, Hire)
2. **Associate Dean** - Enter basic info
3. **Manager** - Assign buddy, office, checklist
4. **Departments (Parallel)**
   - 4a. IT - Computer, email, distros
   - 4b. MarComm - Welcome slide, directory
   - 4c. Operations - Office, keys, cards, access
   - 4d. Finance - Payroll, T&E card, roles
5. **Manager Final** - Training, security roles

**Key Features:**
- Role-based dashboards for each stakeholder
- Task assignments and tracking
- Progress visibility for managers
- Automated notifications and reminders
- Audit trail of all actions
- Reporting and analytics

---

## 💡 Why Modified Option B?

### Beats Option A (Incremental)
- Clean architecture from start
- Built for the exact workflow needed
- Easier to add features later
- Less technical debt

### Beats Pure Option B (Full Big Bang)
- Faster time to value (MVP in 3 months)
- Lower risk with phased delivery
- Can validate and adjust between phases
- Stakeholders see progress quickly

### Beats Option C (Hybrid)
- One system instead of two
- Simpler architecture
- Lower long-term maintenance
- Clearer direction

---

## 📅 Next Steps

### Immediate (This Week)
- [ ] Review these documents with James Cathro
- [ ] Share with Mark Outten for feedback
- [ ] Present to stakeholder group (Sean Michael, IT, Ops, Finance, MarComm)
- [ ] Decide: Monday.com vs. extend portal?
- [ ] Get Canvas API access
- [ ] Investigate HR data feed with Beth Hill

### Week 2-4 (Quick Wins)
- [ ] Implement Quick Win #1: Ops team notifications
- [ ] Implement Quick Win #2: Canvas auto-enrollment
- [ ] Implement Quick Win #3: Manager dashboard
- [ ] Implement Quick Win #4: Start date reminders
- [ ] Implement Quick Win #5: Success page
- [ ] Implement Quick Win #6: Daily digests

### Month 2-4 (MVP Development)
- [ ] Get leadership approval (present to Ian via Mark)
- [ ] Finalize requirements
- [ ] Build MVP (core workflow tracking)
- [ ] User acceptance testing
- [ ] Launch MVP

### Month 5-7 (Full System)
- [ ] Phase 2: Role-based dashboards
- [ ] Phase 3: Integrations and automation
- [ ] Training and documentation
- [ ] Full rollout

---

## 📂 Document Structure

```
sandbox/
├── README.md (this file)
├── onboarding_redesign_plan.md
├── implementation_options_analysis.md
├── onboarding_mockups.md
├── technical_architecture.md
├── quick_wins.md
└── Onboarding.xlsx (original spreadsheet)
```

---

## ✅ Planning Checklist

### Discovery
- [x] Analyzed current onboarding website
- [x] Reviewed proposed spreadsheet process
- [x] Incorporated email context from Mark Outten
- [x] Identified pain points and gaps

### Design
- [x] Defined 5-phase workflow
- [x] Created wireframes for all user roles
- [x] Designed database schema
- [x] Mapped API endpoints
- [x] Planned integration points

### Strategy
- [x] Compared 3 implementation options
- [x] Recommended Modified Option B
- [x] Estimated timeline and budget
- [x] Identified quick wins
- [x] Created implementation roadmap

### Next
- [ ] Stakeholder review and feedback
- [ ] Leadership approval
- [ ] Begin quick wins implementation
- [ ] Start MVP development

---

## 🤝 How to Use These Documents

### For James Cathro (Project Lead)
Start with `onboarding_redesign_plan.md` for the big picture, then review `quick_wins.md` for immediate actions.

### For Mark Outten (IT Director)
Review `technical_architecture.md` to understand the technical approach, then `implementation_options_analysis.md` for budget/timeline.

### For Sean Michael (Operations)
Check `onboarding_mockups.md` to see the Operations dashboard design and `quick_wins.md` for immediate improvements.

### For Managers
Look at the Manager Dashboard mockup in `onboarding_mockups.md` to see how you'll track your team's onboardings.

### For Leadership (Ian)
Review `onboarding_redesign_plan.md` (executive summary) and the recommendation in `implementation_options_analysis.md`.

---

## 📞 Contact

**Questions about these documents?**
- Ben Hartless - bh4hb@virginia.edu
- Built the initial portal, ready to implement!

---

## 🎉 Summary

We have a **clear path forward**:

1. **Quick wins** (2-4 weeks) - Fix immediate issues
2. **MVP** (3 months) - Core workflow tracking
3. **Full system** (6-7 months) - Complete automation

**Total investment:** ~$124k (or internal development time)
**Expected outcome:** Professional, automated onboarding that prevents things from slipping through the cracks and gives everyone visibility into the process.

Let's do this! 🚀
