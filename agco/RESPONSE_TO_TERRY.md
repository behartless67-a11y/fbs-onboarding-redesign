# Draft Response to Terry's AWS Architecture Email

**From:** Ben Hartless (bh4hb@virginia.edu)  
**To:** Terry Johnson (trj2j@virginia.edu)  
**Cc:** Mark Outten (wmo4b@virginia.edu), Molly Lipscomb (ml4db@virginia.edu)  
**Subject:** RE: AWS Account request - Architecture feedback + docs

---

Terry,

This is a **much better architecture** than the Streamlit prototype we initially reviewed. The Docker + A/B testing design is cleaner, more cost-effective, and properly structured for research. I've updated the architecture doc and IRB checklist to reflect your proposal — see attached.

## What I Like

✅ **Treatment/control separation** via containers — clean isolation, easy to compare outcomes  
✅ **Cost optimization** (auto-stop EC2 outside work hours) — cuts compute by ~60%, big win  
✅ **Cloudflare Zero Trust** handling auth externally — apps stay stateless, no PII leakage  
✅ **Multimodal RAG via pre-generated descriptions** — avoids live image-to-text (lower risk, lower cost)  
✅ **Offline pivot as contingency** — smart to have Plan B if connectivity is poor  
✅ **Docker Compose not K8s** — right call for 17 users, avoid overengineering

## Questions / Suggestions

### 1. Cloudflare Zero Trust Cost
**Problem:** At $7/seat × 50 users (17 workers + staff + buffer) = **$350/month** = 60% of your total budget.

**Alternative:** Use **AWS Cognito** ($5/month for email magic links) + **Cloudflare Free** (DNS + basic DDoS only). You lose the opaque ID injection feature, but we can handle that in the app layer:
```python
# After Cognito JWT validation:
enumerator_id = jwt_claims['custom:enumerator_id']  # Set during user provisioning
study_id = request.headers.get('X-Study-ID')  # Worker manually enters farmer code
```

This saves **$345/month** ($8,280 over 24 months). Cloudflare Zero Trust is overkill for 17 users unless DDoS is a real threat — is it?

**Your call:** If partner org has security concerns (prior attacks, sensitive political context), keep Cloudflare. Otherwise, Cognito is sufficient.

---

### 2. Multimodal RAG: GPT-4-Vision or Open-Weight?
You said "maybe pre-generate detailed image summaries" but didn't specify which model.

**Option A: GPT-4-Vision** (my recommendation)
- Cost: ~$0.10/image × 500 images = **$50 one-time**
- Quality: Best-in-class, minimal hallucination
- Workflow: Python script, 1-2 hours to process entire corpus
- Example description:
  > "Four-panel diagram showing bagrada bug life cycle. Panel 1: Adult, shield-shaped, black/orange, 5-7mm. Panel 2: Egg cluster, white, barrel-shaped, 1mm, on cabbage leaf underside. Panel 3: Five nymph stages, orange to black gradient. Panel 4: Damage symptoms: circular holes, yellowing on crucifers."

**Option B: LLaVA 13B** (open-weight, free)
- Cost: $0 (but requires GPU for preprocessing — use your dev machine or a G5 instance for 2 hours = ~$2)
- Quality: Good but more verbose, may need human editing
- Workflow: Slower (5-10 images/min vs GPT-4V's 60/min)

**My vote:** GPT-4-Vision. $50 is negligible compared to 24 months of savings from your auto-stop design, and description quality is critical (bad descriptions = bad advice = IRB problems).

---

### 3. Control Condition: What Exactly Do They Get?
You said "control version of the application" but didn't specify the UX. I assumed **BM25 search with top-3 snippets** (no LLM, no natural language generation). Is that your intent?

**Critical for RCT:** The control needs to be *good enough to use* but *clearly different from treatment*. If control is too frustrating (e.g., raw JSON dumps), workers will abandon it and you lose the comparison.

**Proposed Control UX:**
```
User searches: "bagrada bugs"

Results:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📄 IPM Guide 2024, Page 17
"Bagrada bugs can be controlled through integrated pest 
management. Practices include crop rotation, intercropping 
with marigolds, and early removal of host plants..."
[View full page]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📄 IPM Guide 2024, Page 18  
"Botanical pesticides such as neem oil are effective 
against many sucking insects including aphids and 
small bugs. Apply at dawn or dusk..."
[View full page]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📄 FAO Climate-Smart Agriculture, Page 42
"Early sowing helps plants establish before pest 
pressure peaks in mid-season..."
[View full page]
```

Worker reads, synthesizes, advises farmer. No AI, but not unusable.

**Confirm:** Is this the control you had in mind, or something else?

---

### 4. "Horrifying Possibility" (Offline Tablets)
You're right to plan for this, but let's not prematurely optimize.

**My suggestion:**
1. **Deploy cloud version first** (July pilot)
2. **Measure timeout rate** in Week 1 (if >20% of queries timeout, connectivity is a blocker)
3. **If timeouts are a problem:** Evaluate offline pivot in August (you'll have data to justify the $8K tablet deployment)
4. **If timeouts are rare (<5%):** Stick with cloud (simpler, cheaper)

**For IRB submission (June 15):** Mention offline pivot as a *contingency* in the protocol, but don't commit to it yet. This gives you flexibility without overcommitting to a second development effort.

---

### 5. Load Testing: "All Extension Workers Hit System at Once"
Love this approach — it's the right stress test. But let's formalize it:

**Load Test Plan (June 12, before IRB submission):**
- **Tool:** Locust (open-source, Python-based)
- **Scenario:** 17 concurrent users, each submits 10 queries (170 total queries in ~10 minutes)
- **Success Criteria:**
  - p95 latency <3s (treatment)
  - Error rate <5%
  - CPU <80% (leaves headroom for peak usage)
- **If fails:** Upgrade to g5.2xlarge (+$50/month, but worth it for user experience)

I'll write the Locust script if you send me a few example queries from the golden Q&A set.

---

### 6. VRAM Uncertainty: "Not sure how much VRAM needed"
Let me de-risk this for you:

**g5.xlarge (24GB VRAM) can handle:**
- Llama-3.1-8B (Q4_K_M): ~5GB model + 4GB context + 2GB overhead = **11GB total** ✅
- ChromaDB embeddings (in-memory): ~2GB for 50K chunks ✅
- Image cache (500 images, 500KB each): ~250MB ✅
- **Total: ~13GB used, 11GB free** — plenty of headroom

**You're safe with g5.xlarge.** Only upgrade if:
- You switch to a 13B+ model (Phi-3-Medium, LLaVA 13B for live image-to-text)
- You expand corpus to 200+ PDFs (ChromaDB grows)

---

## What I've Done

I revised the **Architecture Document** and **IRB Readiness Checklist** to reflect your Docker design. Key changes:

### Architecture Doc (Sections 1-5):
- Replaced Streamlit with Docker + FastAPI
- Added treatment/control container specs
- Added multimodal RAG strategy (pre-generated descriptions)
- Revised cost estimate: **$213/month** (assuming Cognito, not Cloudflare Zero Trust)
- Added offline tablet contingency plan (Appendix)
- Updated security section (JWT validation, IAM roles, no hardcoded secrets)

### Checklist (Sections 1-10):
- Added items for Docker image builds (treatment + control)
- Added multimodal preprocessing step (image descriptions)
- Added load testing with specific success criteria
- Revised infrastructure items (Cognito instead of generic "auth proxy")
- Added auto-start/stop Lambda function deployment
- Clarified RCT-specific IRB requirements (treatment vs control consent disclosure)

**Both docs are attached.** Review and let me know if I misunderstood anything.

---

## Action Items (This Week)

**For Terry:**
1. **Decide: Cognito or Cloudflare Zero Trust?** (Cognito saves $345/month, but less DDoS protection)
2. **Confirm control condition UX** (BM25 snippets as I described, or something else?)
3. **Choose image description method** (GPT-4-Vision for $50, or LLaVA for free?)
4. **Send me 10 example queries** (I'll write the Locust load test script)

**For Mark:**
1. **Submit AWS sub-account request** (ServiceNow form, due May 15)
2. **Verify af-south-1 region available** (check in Batten's Enterprise Cloud account)

**For Molly:**
1. **Identify in-country partner** (due May 15 — this is blocking everything else)
2. **Provide grant fund code** (for AWS costs, ~$5K over 24 months)

---

## My Recommendation

**Go with your Docker design.** It's the right architecture for this project — better than the Streamlit prototype in every way. The only tweaks I'd suggest:

1. **Use Cognito instead of Cloudflare Zero Trust** (unless you have specific DDoS concerns)
2. **Use GPT-4-Vision for image descriptions** ($50 one-time is worth the quality)
3. **Pilot cloud version first**, defer offline tablets until you have data showing connectivity is a blocker

With these adjustments, your 24-month cost is **~$5,100** (vs the $6,400 I estimated in the original doc). That's a **$1,300 savings** from the auto-stop design alone — well done.

Let me know your thoughts. Happy to hop on a call this week if you want to walk through the docs together.

**Next Team Meeting:** Friday May 12, 2pm ET (Zoom link TBD)

Best,  
Ben

---

**Attachments:**
- ARCHITECTURE.md (revised 2026-05-11)
- IRB_READINESS_CHECKLIST.md (revised 2026-05-11)
