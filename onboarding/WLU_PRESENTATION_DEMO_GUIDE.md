# W&L AI Retreat Presentation - Demo Guide

**Presenter:** Ben Hartless, UVA Batten School IT  
**Date:** Tuesday, June 15, 2026, 9:05-10:00 AM  
**Audience:** ~24 W&L IT professionals and leadership

---

## 🎯 Your Story Arc

**"I'm a one-person dev team who can now build what used to require hiring contractors."**

### Opening (2 min)
"Six months ago, Mark Outten sent yet another 'here we are again' email about our broken onboarding process. Instead of scheduling another meeting, I spent my morning with Claude Code creating a complete redesign plan. That's what I want to show you - not the AI hype, but the real work."

---

## 📱 Demo #1: The Onboarding Redesign (TODAY's Work) - 20 min

### Why Start Here
- **Most relevant to the audience** - everyone deals with onboarding
- **Shows the full workflow** - from problem to complete solution
- **Built THIS MORNING** - demonstrates real speed

### The Demo

**1. Show Mark's Email (2 min)**
Pull up the email context:
```
"Here we are again...back to the same discussion. 
The process has become more and more inconsistent over time (again)..."
```

**Point:** "This is the third time we've tried to fix this. Classic IT problem, right?"

**2. Show the Live Portal (3 min)**
- Navigate to https://www.thebattenspace.org/onboarding
- "This is what I built before - basic form, sends emails, creates ticket"
- **Problem:** "But it only goes to IT. Operations team has no visibility. Things fall through cracks."

**3. Show the GitHub Repo (10 min)** ⭐ THIS IS THE MONEY SHOT
Open: https://github.com/behartless67-a11y/fbs-onboarding-redesign

Walk through each document:
- **README.md** - "Complete project overview"
- **onboarding_redesign_plan.md** - "Analysis of current vs. proposed"
- **onboarding_mockups.md** - Scroll through the ASCII wireframes
  - "Look at these UI mockups - manager dashboard, IT dashboard, Operations dashboard"
  - "These took 30 minutes. Would normally take days."
- **technical_architecture.md** - "Complete database schema, API design, deployment plan"
- **cost_breakdown.md** - Show the table:
  - "If we contracted this out: $120k"
  - "Doing it internally with Claude: $600/year"
- **quick_wins.md** - "6 things we can ship THIS WEEK while planning the big rebuild"

**4. The Punchline (2 min)**
- "All of this was created this morning. Started at 9 AM, had comprehensive planning docs by 11:30 AM."
- "That's not 'prompt engineering' - that's actual pair programming with an AI that understands the codebase."

**5. Show the Code (3 min)**
Open the API route file: `app/api/onboarding/submit/route.ts`
- "Here's the actual code that adds Operations team notification"
- Scroll through the email templates
- "Claude wrote the structure, I reviewed and adjusted the business logic"

---

## 💻 Demo #2: Live Coding Session - 15 min

### Why This Matters
Shows the PROCESS, not just the output

### The Demo

**Open your IDE with Claude Code visible**

**Scenario:** "Let's add a feature to send a reminder email 1 week before start date"

**1. Start the conversation (3 min)**
You: "I need to add a reminder system that emails the manager and Operations 1 week before the new hire's start date. Show me how to implement this."

Let Claude Code:
- Search the codebase
- Find the relevant files
- Propose a solution

**2. Review the proposal (2 min)**
- "See how it found the existing email functions?"
- "It's suggesting we use a cron job here - that makes sense"
- "But I want to use Azure Functions instead"

**3. Iterate (5 min)**
You: "Actually, let's use Azure Functions Timer Trigger instead of cron. We're already on Azure."

Watch Claude:
- Adjust the approach
- Generate the Azure Function code
- Update the architecture

**4. The Point (5 min)**
- "This is the real workflow. It's not magic autocomplete."
- "It's a conversation where I make the architecture decisions and Claude handles implementation details."
- "I could code this myself, but this is 5x faster."

---

## 🎨 Demo #3: The Fun One - Music Label Automation - 10 min

### Why Include This
- Shows versatility beyond "typical IT work"
- Demonstrates file processing automation
- Fun / memorable / humanizes you
- Proves this isn't just for web apps

### The Demo

**1. Show the Live Site (2 min)**
Navigate to: https://64westrecords.netlify.app
- "This is my side project - 64 West Records, independent music label"
- "21 albums, 200+ songs, all generated with AI"
- Play 10 seconds of a song

**2. Show the Workflow (3 min)**
Open: /c/Users/Ben/Desktop/AI_Projects/MusicMaker/

- "I use Suno to generate music, but then I need to:"
  - Tag the MP3 files with metadata
  - Embed album artwork
  - Update the website with new tracks
  - Generate artist pages
  - Deploy to Netlify

**3. Show the Automation (3 min)**
Open one of the tagging scripts:
```python
# scripts/tagging/tag_[album].py
```

- "Claude Code generated 102 Python scripts that handle this entire pipeline"
- "Each album gets custom tagging, artwork embedding, and website updates"
- "This would be tedious manual work. Now it's fully automated."

**4. The Point (2 min)**
- "This isn't core to my job, but it shows the versatility"
- "Same AI, same workflow, completely different domain"
- "File processing, metadata management, web deployment - all automated"

---

## 🔧 Demo #4: The IT Dashboard - 10 min

### Why Include This
- Most relevant to the audience's daily work
- Shows integration with multiple systems
- Demonstrates practical IT management

### The Demo

**1. Show Live Dashboard (3 min)**
Navigate to: https://red-moss-09027b10f.6.azurestaticapps.net

- "This is our unified IT dashboard"
- "Pulls from Jamf (Mac management), Intune (Windows), Qualys (security), GitHub, Zendesk, Monday.com"

**2. Show the Integration (3 min)**
- "Before: logging into 6 different systems to check device status"
- "Now: single pane of glass"
- Click through:
  - Device inventory
  - Security vulnerabilities
  - Loaner laptop tracking
  - GitHub repository audit

**3. Show the Code (2 min)**
Open a few API integration files:
- "Claude Code helped build the Azure Functions that pull from each API"
- "TypeScript types for all the data sources"
- "Charts and visualizations"

**4. The Point (2 min)**
- "This dashboard would've been a 3-month project to contract out"
- "Built it in 2 weeks with Claude Code"
- "Now our team has visibility we never had before"

---

## 🎤 Demo #5: The APPExplorer (Bonus if time) - 5 min

### The Quick Version
- "We have 592 student policy project reports in Azure Blob Storage"
- "Needed a searchable interface with secure, network-restricted downloads"
- "Claude Code built the entire thing - frontend, Azure Functions, SAS token auth"
- Navigate to the site briefly
- "Search works, downloads work, IP filtering works"

---

## 💡 Wrap-Up: What Works / What Doesn't - 5 min

### ✅ What Works

**Rapid Prototyping**
- "Planning docs in hours, not weeks"
- "MVPs in days, not months"

**Code Generation**
- "Boilerplate, CRUD operations, API integrations"
- "TypeScript types, validation schemas"

**Documentation**
- "Technical docs, API specs, deployment guides"
- "All the stuff developers hate writing"

**Refactoring**
- "Updating old code to new patterns"
- "Explaining unfamiliar codebases"

**Learning New Tech**
- "Started using Next.js with Claude's help"
- "Azure Functions, TypeScript - all new to me 6 months ago"

### ⚠️ What Doesn't Work (Yet)

**Architecture Decisions**
- "Claude can't decide if you should use MongoDB or PostgreSQL"
- "You still need to understand your requirements"

**Complex Business Logic**
- "Works great for standard patterns"
- "Custom algorithms still need human design"

**Security/Compliance**
- "Claude writes code that works, not code that's secure by default"
- "You still need to review for vulnerabilities"

**Legacy System Integration**
- "Modern APIs: easy"
- "Mainframe COBOL: you're on your own"

**The Truth**
- "It writes good code, but you need to know if it's the RIGHT code"
- "Garbage in, garbage out - if you don't understand the problem, Claude won't fix that"

---

## 📊 The Business Case - 3 min

### Show the Numbers

**Projects Completed in 6 Months:**
1. Batten Space portal (onboarding, calendars, services)
2. IT Dashboard (6-system integration)
3. APPExplorer (secure document repository)
4. Music label automation (102 scripts)
5. Onboarding redesign planning (today)

**Estimated Contractor Cost:** $250k+  
**Actual Cost:** My salary + $1,200/year in infrastructure  
**Time Saved:** ~800 hours of coding  

**ROI Isn't Just Speed**
- "We can now say YES to projects we used to say NO to"
- "Our small team punches above our weight class"
- "That's the transformation - not just doing things faster, but doing MORE things"

---

## 🎯 Closing Message (2 min)

**The Point:**
"I'm not a better developer than I was 6 months ago. I'm a developer with a really good pair programming partner who never gets tired, never takes vacation, and knows every programming language.

The work still requires judgment, architecture decisions, and understanding user needs. But the implementation? That's 5-10x faster.

For a small IT team in higher ed, that's the difference between maintaining what we have and actually innovating."

**The Ask:**
"Questions? Want to see the code for any of these projects? Everything I showed is on GitHub."

---

## 📱 Quick Reference

### URLs to Have Open
1. https://www.thebattenspace.org/onboarding
2. https://github.com/behartless67-a11y/fbs-onboarding-redesign
3. https://64westrecords.netlify.app
4. https://red-moss-09027b10f.6.azurestaticapps.net
5. Your IDE with Claude Code

### Files to Have Ready
- Mark Outten's email
- BattenSpace codebase
- MusicMaker scripts folder
- Cost breakdown screenshot

### Backup Plan
- Screenshots of everything
- Offline copy of GitHub repo
- Screen recording of Claude Code in action

---

## 🎬 Timing Breakdown (50-55 min total)

```
00:00 - 00:02   Opening hook
00:02 - 00:22   Demo #1: Onboarding redesign (today's work)
00:22 - 00:37   Demo #2: Live coding session
00:37 - 00:47   Demo #3: Music label automation
00:47 - 00:52   Demo #4: IT Dashboard (if time)
00:52 - 00:57   What works / What doesn't
00:57 - 01:00   Closing + Q&A setup
```

---

## 🗣️ Speaking Notes

### Tone
- **Conversational** - you're talking to peers, not giving a TED talk
- **Honest** - admit limitations, don't oversell
- **Practical** - focus on real problems and real solutions
- **Humble** - "This isn't magic, it's just really good tooling"

### What NOT to Say
❌ "AI will replace developers"
❌ "You can do this with no coding knowledge"
❌ "It's perfect and never makes mistakes"
❌ "Everyone should drop what they're doing and use this"

### What TO Say
✅ "This makes me more productive as a developer"
✅ "I still need to understand what I'm building"
✅ "It's like having a senior developer on call 24/7"
✅ "Your mileage may vary - but it's worth exploring"

---

## ❓ Anticipated Questions

**Q: "What about accuracy? Does it write buggy code?"**
A: "Yes, sometimes. That's why you review everything. But the bugs are usually obvious and easy to fix. The alternative is writing it all myself, which takes 5x longer."

**Q: "What about security? Can you trust AI-generated code?"**
A: "No more or less than human-written code. We still run security scans, still do code reviews. Claude doesn't introduce NEW vulnerabilities, but it won't prevent them either."

**Q: "What does this cost?"**
A: "Claude Code is $50/month. Infrastructure costs vary by project. For us, about $100-200/month in Azure. Compare that to contractor rates of $100-150/hour."

**Q: "What about training? How long to get productive?"**
A: "I was productive on day one. The learning curve isn't the tool - it's learning how to communicate effectively with it. Takes a few days to get comfortable."

**Q: "Can it work with our legacy systems?"**
A: "If your legacy system has documentation, yes. If it's undocumented COBOL from 1987, probably not. Modern systems: absolutely."

**Q: "What about vendor lock-in to Claude/Anthropic?"**
A: "Fair concern. The code it generates is standard - no proprietary dependencies. If Claude disappeared tomorrow, I'd lose the productivity boost but keep all the code."

**Q: "How do you handle when it's wrong?"**
A: "I ask it to try again with more context, or I fix it myself. It's pair programming - sometimes your partner is wrong and you course-correct."

---

## 🚀 Post-Presentation Follow-Up

### Offer to Share
- GitHub repos (public or fork for them)
- Documentation templates
- Azure deployment configs
- "Happy to answer follow-up questions via email"

### What to Bring
- Business cards
- QR code to your GitHub profile
- QR code to the onboarding planning repo

### Networking
- This is a peer group, not a sales pitch
- Focus on learning from their use cases too
- "What are you all working on? Maybe I can help"

---

**Remember:** You're not selling Claude Code. You're sharing what works for you as a small IT team. Be authentic, be honest, and show the real work.

**Good luck! 🎉**
