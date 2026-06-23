# AGCO IRB Submission - Readiness Checklist

**Project:** Agricultural Chatbot for Lesotho Extension Workers (RCT with Treatment/Control)  
**PI:** Molly Lipscomb (ml4db@virginia.edu)  
**Technical Lead:** Terry Johnson (trj2j@virginia.edu)  
**Target IRB Submission Date:** June 15, 2026  
**Revision:** 1.1 (updated for Docker + A/B testing architecture)

---

## How to Use This Checklist

- **Owner column** indicates who is responsible for completing the item
- **Status** should be updated as: `⬜ Not Started` → `🔄 In Progress` → `✅ Complete` → `🚫 Blocked`
- **Blocker notes** explain any dependencies or issues
- Review this checklist weekly at team meetings (Fridays, 2pm ET)

---

## Section 1: Legal & Compliance Foundation

| # | Item | Owner | Status | Due | Notes |
|---|------|-------|--------|-----|-------|
| 1.1 | **In-country partner identified** | Molly | ⬜ | May 15 | Who is the Lesotho organization partnering on this project? Name + contact person |
| 1.2 | **Enumerator/farmer ID assignment process defined** | Molly + Partner | ⬜ | May 20 | Who creates UUIDs? Who maintains UUID→Name mapping? (Not shared with UVA) |
| 1.3 | **Data Use Agreement (DUA) drafted** | Molly + UVA Research Compliance | ⬜ | May 31 | Template: https://research.virginia.edu/research-data-support/templates |
| 1.4 | **DUA signed by partner org** | Molly | ⬜ | June 7 | Requires legal review on both sides (allow 2-3 weeks) |
| 1.5 | **Lesotho Data Protection Act review** | Molly + UVA General Counsel | ⬜ | May 24 | Confirm adequate safeguards for cross-border data flow (US storage) |
| 1.6 | **UVA Export Control clearance** | Molly | ⬜ | May 24 | Email export@virginia.edu: "Open-weight LLMs (Llama/Mistral) deployed to AWS Cape Town for research in Lesotho" |
| 1.7 | **IRB protocol number obtained** | Molly | ⬜ | May 15 | New protocol or amendment to existing? If new, submit concept for pre-review |
| 1.8 | **Grant fund code for AWS costs** | Molly | ⬜ | May 15 | ~$5,100 over 24 months (see Architecture Doc Section 5) |
| 1.9 | **AWS sub-account request form submitted** | Mark | ⬜ | May 15 | Mark to complete ServiceNow form, attach fund code from 1.8 |

**Blocker Alert:** Items 1.1-1.4 are **critical path**. If partner org not identified by May 15, entire timeline slips.

---

## Section 2: AWS Infrastructure (Pre-IRB)

| # | Item | Owner | Status | Due | Notes |
|---|------|-------|--------|-----|-------|
| 2.1 | **AWS sub-account created** | ITS (via Mark) | ⬜ | May 20 | Depends on 1.9, typically 3-5 days turnaround |
| 2.2 | **AWS af-south-1 region enabled** | Mark | ⬜ | May 20 | Verify in AWS console: EC2 → Launch Instance → Region dropdown |
| 2.3 | **VPC + subnets created (af-south-1)** | Ben | ⬜ | May 24 | VPC: 10.0.0.0/16. Public subnet: 10.0.1.0/24. Private subnet: 10.0.2.0/24 |
| 2.4 | **Security groups configured** | Ben | ⬜ | May 24 | ALB-SG: 443 from 0.0.0.0/0. EC2-SG: 8000-8001 from ALB-SG only |
| 2.5 | **Application Load Balancer (ALB) created** | Ben | ⬜ | May 27 | Public subnets, internet-facing, target groups for :8000 (treatment), :8001 (control) |
| 2.6 | **TLS certificate requested (ACM)** | Ben | ⬜ | May 24 | Domain: *.batten.virginia.edu (wildcard for agco-treatment/agco-control subdomains) |
| 2.7 | **S3 bucket created (us-east-1)** | Ben | ⬜ | May 24 | Name: uva-batten-agco-logs. Enable: SSE-KMS, block public access, versioning |
| 2.8 | **S3 lifecycle policy configured** | Ben | ⬜ | May 24 | Hot: 90 days (Standard). Archive: 2 years (Glacier). Then: Delete |
| 2.9 | **IAM role created (EC2 instance)** | Ben | ⬜ | May 27 | Permissions: s3:PutObject (log bucket only), ssm:GetParameter (/agco/* only) |
| 2.10 | **CloudTrail enabled (S3 audit logs)** | Ben | ⬜ | May 27 | Log all S3 API calls, 7-year retention |
| 2.11 | **AWS Cognito user pool created** | Ben | ⬜ | May 31 | Region: af-south-1. Auth flow: Email magic links. Custom attributes: enumerator_id, group (treatment/control) |
| 2.12 | **EventBridge schedule created (auto-start/stop EC2)** | Ben | ⬜ | June 7 | Start: 06:00 UTC (8am Lesotho). Stop: 16:00 UTC (6pm Lesotho). Target: Lambda function |

**Dependency:** Items 2.3-2.12 blocked until 2.1 complete (AWS account ready).

---

## Section 3: Application Development (Treatment + Control)

| # | Item | Owner | Status | Due | Notes |
|---|------|-------|--------|-----|-------|
| 3.1 | **Create golden Q&A evaluation set** | Terry | ⬜ | May 31 | 50 agricultural questions + expert-validated answers. Store in Git: `/eval/golden_qa.jsonl` |
| 3.2 | **Recruit agricultural expert for validation** | Molly | ⬜ | May 24 | Partner org staff or external consultant? Budget: ~$1,000 (10 hours) |
| 3.3 | **Finalize PDF corpus** | Terry | ⬜ | May 27 | List all source documents (core + optional), verify copyright clearance |
| 3.4 | **Run multimodal preprocessing (image descriptions)** | Terry | ⬜ | June 3 | Extract images, generate descriptions (GPT-4-Vision or LLaVA), human review 10% |
| 3.5 | **Build ChromaDB index (with image descriptions)** | Terry | ⬜ | June 3 | Run ingest.py, tag as corpus-v1.0-2026-06, commit to Git |
| 3.6 | **Benchmark 4 candidate models** | Terry | ⬜ | June 3 | Mistral/Llama/Phi/Qwen on golden set. Measure: citation accuracy, refusal rate, latency |
| 3.7 | **Select final model** | Terry | ⬜ | June 3 | Document decision in `/eval/model_selection.md` |
| 3.8 | **Build treatment Docker image** | Terry | ⬜ | June 7 | FastAPI + llama.cpp + ChromaDB. Push to AWS ECR |
| 3.9 | **Build control Docker image** | Terry | ⬜ | June 7 | FastAPI + BM25 only (no LLM, no vector DB). Push to AWS ECR |
| 3.10 | **Implement PII detection filter** | Terry | ⬜ | June 7 | Regex: names, phone (+266), GPS coords. Warn user, flag in logs if proceed |
| 3.11 | **Implement S3 logging (JSONL)** | Terry | ⬜ | June 7 | Events: consent, query, retrieval, response, exit_survey. Async writes (no blocking) |
| 3.12 | **Implement JWT validation (Cognito)** | Terry | ⬜ | June 7 | Download JWKS, validate signature/expiration on every request |
| 3.13 | **Implement health check endpoints** | Terry | ⬜ | June 7 | `/health` returns 200 if app + model server responsive |
| 3.14 | **Add consent screen UI (English + Sesotho)** | Terry | ⬜ | June 10 | Show on first visit, record to S3, set cookie to skip on return |

**Model Selection (3.7) blocks Docker build (3.8).** If model selection delayed, adjust timeline.

---

## Section 4: Consent & User Experience

| # | Item | Owner | Status | Due | Notes |
|---|------|-------|--------|-----|-------|
| 4.1 | **Draft consent form (English)** | Molly | ⬜ | May 24 | Use template in Architecture Doc Appendix A, customize for RCT (treatment vs control) |
| 4.2 | **Translate consent form to Sesotho** | Molly | ⬜ | May 31 | Professional translator (NOT machine translation). Cost: ~$300. Store: `/docs/consent_sesotho.md` |
| 4.3 | **Draft UI strings for translation** | Terry | ⬜ | May 27 | Extract all user-facing text: buttons, error messages, help text. Store: `/i18n/en.json` |
| 4.4 | **Translate UI strings to Sesotho** | Molly | ⬜ | June 3 | Same translator as 4.2. Store: `/i18n/st.json`. Cost: ~$200 |
| 4.5 | **Add language toggle to UI** | Terry | ⬜ | June 7 | Dropdown: English / Sesotho. Store preference in cookie |
| 4.6 | **Add disclaimer banner (treatment group)** | Terry | ⬜ | June 7 | "This is AI-generated advice. Always use your professional judgment." Persistent at top of chat |
| 4.7 | **Add exit survey (end-of-day prompt)** | Terry | ⬜ | June 7 | "How helpful was the tool today?" (1-5 scale). Optional, can dismiss. Log to S3 |
| 4.8 | **Accessibility audit (WCAG 2.1 AA)** | Ben | ⬜ | June 10 | Test: WAVE, axe DevTools, screen reader (NVDA), keyboard nav, color contrast |
| 4.9 | **User testing (2-3 extension workers)** | Molly | ⬜ | June 12 | Remote Zoom, observe interaction, collect feedback. Iterate on UX if major issues |

**Translation Coordination:** Molly to hire translator by May 20 to hit deadlines 4.2 + 4.4.

---

## Section 5: Security Hardening

| # | Item | Owner | Status | Due | Notes |
|---|------|-------|--------|-----|-------|
| 5.1 | **Generate LLM API key (random 32-char)** | Terry | ⬜ | May 31 | Store in AWS Systems Manager Parameter Store: `/agco/treatment/llm-api-key` |
| 5.2 | **Configure IAM role (no hardcoded secrets)** | Ben | ⬜ | May 31 | Apps read from Parameter Store via IAM role (no env vars with secrets) |
| 5.3 | **Disable SSH (use Session Manager)** | Ben | ⬜ | June 3 | Remove SSH key from EC2, configure SSM agent for emergency access |
| 5.4 | **Configure TLS 1.2+ only (ALB)** | Ben | ⬜ | June 3 | Security policy: ELBSecurityPolicy-TLS-1-2-2017-01 (disable TLS 1.0/1.1) |
| 5.5 | **Enable S3 bucket encryption (SSE-KMS)** | Ben | ⬜ | May 27 | Use UVA-managed KMS key (or AWS-managed if UVA key not available) |
| 5.6 | **Block S3 public access (bucket policy)** | Ben | ⬜ | May 27 | Enable all 4 "Block Public Access" settings at bucket level |
| 5.7 | **Test data deletion workflow** | Terry + Ben | ⬜ | June 10 | Create test enumerator_id, log queries, run deletion script, verify all S3 objects purged |
| 5.8 | **Security scan (OWASP ZAP)** | Ben | ⬜ | June 10 | Automated scan for XSS, SQL injection, CSRF, etc. Fix critical/high findings |
| 5.9 | **AWS Inspector scan (EC2)** | Ben | ⬜ | June 10 | Scan for vulnerable packages, unpatched OS. Fix critical/high findings |
| 5.10 | **Set up CloudWatch alarms** | Ben | ⬜ | June 7 | Error rate >5%, p95 latency >5s, CPU >80%, disk >90%. Email: Mark/Ben |

**Security Review Meeting:** Mark + Ben + Terry (June 5) to review scan results before IRB submission.

---

## Section 6: Data Governance & Logging

| # | Item | Owner | Status | Due | Notes |
|---|------|-------|--------|-----|-------|
| 6.1 | **Define logging schema (JSON format)** | Terry | ⬜ | May 27 | Document in `/docs/logging_schema.md` with example events |
| 6.2 | **Implement event logging (6 event types)** | Terry | ⬜ | June 3 | consent, query, retrieval, response, exit_survey, error. Async S3 writes |
| 6.3 | **Hash user queries before S3 write** | Terry | ⬜ | June 3 | Store SHA-256 hash in hot logs (deduplication), full text in separate file (for research) |
| 6.4 | **Set up weekly export script** | Terry | ⬜ | June 7 | Cron job (Sundays): Copy last 7 days from S3 → UVA Dataverse (restricted access) |
| 6.5 | **Test S3 lifecycle policy** | Ben | ⬜ | June 7 | Upload test object, verify transitions: Standard (90d) → Glacier (2y) → Expire |
| 6.6 | **Document data retention in DUA** | Molly | ⬜ | June 7 | Copy retention table from Architecture Doc Section 2.2 into DUA |
| 6.7 | **Write data deletion script** | Terry | ⬜ | June 7 | Input: enumerator_id. Action: Delete all S3 objects matching. Store: `/scripts/delete_user_data.py` |
| 6.8 | **Test manual data access request** | Terry | ⬜ | June 10 | Create test ID, log queries, retrieve all records, export as JSON |

**Privacy Lead Review:** Molly to review logging implementation (June 5) before IRB submission.

---

## Section 7: Operational Readiness

| # | Item | Owner | Status | Due | Notes |
|---|------|-------|--------|-----|-------|
| 7.1 | **Write deployment runbook** | Terry + Ben | ⬜ | June 10 | Step-by-step: launch EC2, pull Docker images, start containers, configure ALB. Store: `/docs/deployment.md` |
| 7.2 | **Write incident response plan** | Mark + Ben | ⬜ | June 10 | Covers: app down, data breach, bad advice, high costs. Store: `/docs/incident_response.md` |
| 7.3 | **Create docker-compose.yml** | Terry | ⬜ | June 7 | See Architecture Doc Appendix B for template |
| 7.4 | **Create Lambda function (auto-start/stop EC2)** | Ben | ⬜ | June 7 | Python script triggered by EventBridge, store in `/infra/lambda/` |
| 7.5 | **Test auto-start/stop (dry run)** | Ben | ⬜ | June 10 | Manually trigger Lambda, verify EC2 starts/stops, containers auto-restart |
| 7.6 | **Load test (17 concurrent users)** | Terry + Ben | ⬜ | June 12 | Locust: 17 workers × 10 queries each. Measure: p95 latency, error rate, CPU usage |
| 7.7 | **Run golden Q&A evaluation (baseline)** | Terry | ⬜ | June 12 | Automated metrics: citation accuracy, refusal rate, BLEU vs gold. Store results: `/eval/baseline_results.json` |
| 7.8 | **Document on-call rotation** | Mark | ⬜ | June 10 | Primary: Mark. Backup: Ben. Escalation: Terry. SLA: 4 hours (best effort) |
| 7.9 | **Train Mark/Ben on llama.cpp basics** | Terry | ⬜ | June 10 | 30-min session: how to restart model server, check logs, reload model |
| 7.10 | **Create monitoring dashboard (CloudWatch)** | Ben | ⬜ | June 10 | Widgets: query volume, latency, error rate, cost. URL shared with team |

**Load Test (7.6) is GO/NO-GO decision point.** If p95 latency >3s, may need to upgrade instance or optimize model.

---

## Section 8: IRB Submission Package

| # | Item | Owner | Status | Due | Notes |
|---|------|-------|--------|-----|-------|
| 8.1 | **IRB protocol narrative** | Molly | ⬜ | June 12 | Describe: RCT design, population (17 workers), data collection (logs), risks/benefits, consent process |
| 8.2 | **Informed consent form (English + Sesotho)** | Molly | ⬜ | June 12 | From items 4.1-4.2 |
| 8.3 | **Architecture document** | Ben | ✅ | May 11 | Attach as appendix to IRB submission (this document, revised 2026-05-11) |
| 8.4 | **Data Use Agreement (signed)** | Molly | ⬜ | June 12 | From item 1.4 |
| 8.5 | **Data Protection Impact Assessment** | Molly + UVA Compliance | ⬜ | June 12 | Required for Lesotho DPA cross-border transfer. Template: https://research.virginia.edu/irb-hsr/dpia |
| 8.6 | **Model evaluation report** | Terry | ⬜ | June 12 | Results from golden Q&A set (item 3.6): citation accuracy, refusal rate, sample responses. 2-page PDF |
| 8.7 | **Security assessment summary** | Mark + Ben | ⬜ | June 12 | 1-page: encryption (TLS, KMS), access controls (IAM), logging (CloudTrail), incident response |
| 8.8 | **Recruitment materials (if applicable)** | Molly | ⬜ | June 12 | If recruiting beyond partner org's existing staff. Otherwise mark N/A |
| 8.9 | **AWS SOC 2 compliance certificate** | Ben | ⬜ | June 10 | Download from AWS Artifact (requires AWS account login). Attach to IRB submission |
| 8.10 | **Submit to IRB via Horizon** | Molly | ⬜ | June 15 | https://research.virginia.edu/irb-hsr/submit-study. Confirm all attachments uploaded |

**Pre-Submission Review:** UVA Research Compliance office offers pre-review (optional, but recommended). Email irb-hsr@virginia.edu by June 8 to request.

---

## Section 9: Post-IRB Approval (Pre-Launch)

*These items can only start after IRB approval. Estimated approval: June 30, 2026.*

| # | Item | Owner | Status | Due | Notes |
|---|------|-------|--------|-----|-------|
| 9.1 | **Launch EC2 g5.xlarge instance** | Ben | ⬜ | July 1 | Region: af-south-1. Attach IAM role, Elastic IP. Install Docker + Docker Compose |
| 9.2 | **Deploy ChromaDB index to EC2** | Terry | ⬜ | July 1 | SCP or S3 sync: `/opt/agco/index/` (corpus-v1.0-2026-06) |
| 9.3 | **Deploy treatment + control containers** | Terry + Ben | ⬜ | July 1 | docker-compose up -d. Verify both containers healthy: curl localhost:8000/health |
| 9.4 | **Configure ALB target groups** | Ben | ⬜ | July 1 | Route: agco-treatment.batten.virginia.edu → :8000, agco-control.batten.virginia.edu → :8001 |
| 9.5 | **Update DNS (Route 53 or Batten DNS)** | Ben | ⬜ | July 1 | Point subdomains to ALB. Verify TLS cert valid |
| 9.6 | **Provision 17 Cognito users** | Ben | ⬜ | July 1 | Bulk upload CSV: email, enumerator_id, group (treatment/control). Partner org provides list |
| 9.7 | **Send invitation emails (magic links)** | Ben | ⬜ | July 1 | Cognito sends automated invites. Subject: "AGCO Agricultural Tool - Get Started" |
| 9.8 | **Smoke test (2 test accounts)** | Terry + Ben | ⬜ | July 1 | 1 treatment, 1 control. Test: login, consent, query, response, exit survey, data deletion |
| 9.9 | **Enable CloudWatch alarms** | Ben | ⬜ | July 1 | Verify PagerDuty/email alerts working (send test alarm) |
| 9.10 | **Training session (17 workers)** | Molly | ⬜ | July 1 | 1-hour Zoom: How to use tool, interpret citations, report issues. Record session for reference |
| 9.11 | **Announce launch (partner org)** | Molly | ⬜ | July 1 | Email + WhatsApp group. Link to training recording |
| 9.12 | **Daily monitoring (week 1)** | Terry + Mark | ⬜ | July 1-7 | Check logs, error rate, user feedback. Daily standup at 9am ET |
| 9.13 | **Week 1 retrospective** | All | ⬜ | July 8 | What worked? What broke? Adjust for wider rollout (if pilot successful) |

**GO/NO-GO Decision (July 8):** If >10% error rate or major usability issues, pause and fix before continuing.

---

## Section 10: Post-Launch (Ongoing Maintenance)

| # | Item | Owner | Frequency | Notes |
|---|------|-------|-----------|-------|
| 10.1 | **Review S3 logs for PII warnings** | Terry | Weekly (Fridays) | Check flagged queries, verify false positives, contact enumerator if real PII detected |
| 10.2 | **Check for abuse patterns** | Terry | Weekly | Flag: enumerator with >50 queries/day, identical queries repeated, unusual hours |
| 10.3 | **Run golden Q&A regression test** | Terry | Monthly (1st of month) | Compare to baseline (item 7.7). Alert if citation accuracy drops >5% |
| 10.4 | **Human evaluation (20 random convos)** | Molly + Ag Expert | Monthly | Rate answer quality (1-5), flag bad advice, identify corpus gaps |
| 10.5 | **Security patch application** | Ben | Monthly (2nd Tuesday) | OS updates (apt upgrade), Python packages (pip upgrade). Test in dev first |
| 10.6 | **Corpus update (new PDFs)** | Terry | Quarterly | Rebuild index, run regression tests, deploy. Git tag: corpus-v1.1-2026-10, etc. |
| 10.7 | **Cost review** | Mark | Quarterly | Verify AWS bill matches estimate (~$213/month). Investigate anomalies |
| 10.8 | **Backup EBS snapshot** | Ben | Weekly (automated) | AWS Data Lifecycle Manager policy: weekly snapshot, 4-week retention |
| 10.9 | **Export logs to Dataverse** | Terry | Weekly (automated) | Cron job: S3 → Dataverse (restricted access), retain for 2 years |
| 10.10 | **User satisfaction survey** | Molly | Every 6 months | NPS score, feature requests, pain points. Qualtrics survey emailed to workers |
| 10.11 | **Model evaluation (compare alternatives)** | Terry | Quarterly | Benchmark new models (e.g., Llama 3.2) on golden set. Consider upgrade if >10% improvement |
| 10.12 | **Sustainability planning meeting** | All | March 2028 | Decide: transition to partner org, UVA maintains, or sunset. Needs 6-month lead time |

---

## Critical Path Summary

**Blocking items for IRB submission (June 15 deadline):**

| Item | Owner | Due | Status |
|------|-------|-----|--------|
| 1.1 In-country partner identified | Molly | May 15 | ⬜ CRITICAL |
| 1.3 Data Use Agreement drafted | Molly | May 31 | ⬜ |
| 1.4 DUA signed | Molly | June 7 | ⬜ |
| 3.1 Golden Q&A set created | Terry | May 31 | ⬜ |
| 3.6 Model benchmarked + selected | Terry | June 3 | ⬜ |
| 4.1 Consent form drafted (English) | Molly | May 24 | ⬜ |
| 4.2 Consent form translated (Sesotho) | Molly | May 31 | ⬜ |
| 8.1-8.10 IRB package complete | Molly | June 12 | ⬜ |

**Red Flags (as of May 11, 2026):**

🚨 **No in-country partner named** → Molly to provide by May 15 or IRB submission will slip  
🚨 **No AWS sub-account yet** → Mark to submit ServiceNow form ASAP (3-5 day turnaround)  
🚨 **No funding source confirmed** → Molly to provide grant code by May 15  

---

## Risk Register

| Risk | Impact | Likelihood | Mitigation |
|------|--------|------------|------------|
| **Partner org delays DUA signature** | High (blocks IRB) | Medium | Start legal review NOW, have backup partner option |
| **af-south-1 not available in UVA account** | Medium (use us-east-1, higher latency) | Low | Mark to verify by May 17 |
| **Model performs poorly on golden set** | Medium (need to re-test, delays deployment) | Medium | Test all 4 models in parallel, select by June 3 |
| **IRB requests major revisions** | High (delays launch 2-4 weeks) | Medium | Pre-consult with IRB informally (Molly, by June 1) |
| **Load test reveals g5.xlarge insufficient** | Medium (need g5.2xlarge, +$50/month) | Low | Budget allows 15% buffer, can absorb cost |
| **Bad advice reported in pilot** | High (reputational, research validity) | Low | Golden set validation, human review loop, prominent disclaimer |
| **Data breach (S3 bucket exposed)** | Critical (legal, reputational) | Very Low | S3 block public access, CloudTrail logging, quarterly audits |
| **Terry unavailable post-launch (injury, family)** | Medium (no one can fix model issues) | Low | Cross-train Mark/Ben on llama.cpp (item 7.9), document everything |
| **Poor rural connectivity forces offline pivot** | High (need tablet deployment, +$8K cost) | Medium | Monitor timeout rate in week 1. If >20%, evaluate offline pivot (August) |
| **Treatment performs WORSE than control** | High (null result, but still publishable) | Medium | Adjust hypothesis: "LLM not cost-justified for this use case" → still valuable finding |

---

## Communication Plan

**Weekly Check-In (Fridays, 2pm ET, starting May 15):**
- **Attendees:** Molly, Terry, Mark, Ben
- **Agenda:** 
  1. Checklist review (5 min per section)
  2. Blocker escalation (10 min)
  3. Next week's priorities (5 min)
- **Duration:** 30 minutes
- **Format:** Zoom + this Google Doc (shared editing)

**Slack/Email:** `agco-lesotho` channel (or email thread if no Slack)

**Escalation Path:**
- **Technical blocker:** Terry → Mark → Ben → UVA ITS (cloudhelp@virginia.edu)
- **Compliance blocker:** Molly → UVA Research Compliance (irb-hsr@virginia.edu)
- **Funding blocker:** Molly → Batten Finance (batten-finance@virginia.edu)
- **Partner org unresponsive:** Molly → [Partner Org Director] → UVA Office of Sponsored Programs

---

## Success Criteria (Recap from Architecture Doc)

**Pilot Success (July 2026, Month 1):**
- [ ] All 17 workers successfully log in
- [ ] >80% submit ≥5 queries in first week
- [ ] <5% error rate (5XX, crashes, timeouts)
- [ ] p95 latency <3s (treatment)
- [ ] 0 security incidents
- [ ] Human review: >90% responses "acceptable or better"
- [ ] Exit survey: ≥3.5/5 average helpfulness

**6-Month Success (January 2027):**
- [ ] ≥12 active workers per group
- [ ] Treatment: ≥300 queries/month
- [ ] Control: ≥200 queries/month
- [ ] Refusal rate: 10-20% (treatment)
- [ ] Citation accuracy: >85%
- [ ] Cost: <$250/month (within budget)

**24-Month Success (July 2028):**
- [ ] RCT analysis complete (treatment effect measured)
- [ ] Paper submitted to peer-reviewed journal
- [ ] Corpus + code published (if no copyright restrictions)
- [ ] Sustainability plan decided

---

## Appendix: Useful Links

**UVA Resources:**
- IRB Submission: https://research.virginia.edu/irb-hsr/submit-study
- DUA Templates: https://research.virginia.edu/research-data-support/templates
- Export Control: export@virginia.edu
- AWS Sub-Account Request: https://virginia.service-now.com/esc?id=sc_cat_item&sys_id=74f59e2f1bafcd5056d1db15ec4bcbd1
- UVA Cloud Help: cloudhelp@virginia.edu
- InfoSec: security@virginia.edu

**AWS Resources:**
- Enterprise Cloud Console: https://console.aws.amazon.com/
- Cost Explorer: https://console.aws.amazon.com/cost-management/
- CloudWatch: https://console.aws.amazon.com/cloudwatch/
- Systems Manager Parameter Store: https://console.aws.amazon.com/systems-manager/parameters/
- AWS Artifact (SOC 2 report): https://console.aws.amazon.com/artifact/

**Technical Docs:**
- llama.cpp: https://github.com/ggerganov/llama.cpp
- ChromaDB: https://docs.trychroma.com/
- FastAPI: https://fastapi.tiangolo.com/
- Docker Compose: https://docs.docker.com/compose/
- Locust (load testing): https://locust.io/

**Legal:**
- Lesotho Data Protection Act: https://www.lesotholii.org/ls/legislation/act/2021/3
- AWS SOC 2: https://aws.amazon.com/compliance/soc-2/
- Meta Llama License: https://ai.meta.com/llama/license/
- Mistral License: https://www.apache.org/licenses/LICENSE-2.0

---

## Checklist Owner

**Primary:** Terry Johnson (trj2j@virginia.edu)  
**Review Cadence:** Weekly (Fridays, 2pm ET)  
**Last Updated:** May 11, 2026 (Revision 1.1)

---

## Meeting Notes

**May 11, 2026 (Email Thread - Terry's Architecture Proposal):**
- Terry proposes Docker + A/B testing (treatment vs control)
- Multimodal RAG via pre-generated image descriptions (not live image-to-text)
- Auto-start/stop EC2 to save ~60% on compute costs
- Contingency plan: Offline tablet deployment if connectivity poor
- Next: Team meeting May 12 to align on this approach vs original Streamlit prototype

**May 12, 2026 (First Team Meeting):**
- _[Notes here]_

**May 19, 2026 (Second Team Meeting):**
- _[Notes here]_

---

**Questions? Blockers? Escalations?**  
📧 Email Ben (bh4hb@virginia.edu) or post in `#agco-lesotho` Slack.  
🔥 For urgent blockers (IRB deadline at risk): Text Mark (540-XXX-XXXX) or Ben (540-460-7676).
