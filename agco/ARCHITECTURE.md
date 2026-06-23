# AGCO (Agricultural Compendium) - Architecture Document

**Project:** Agricultural chatbot for extension workers in Lesotho  
**Principal Investigator:** Molly Lipscomb (ml4db)  
**Technical Lead:** Terry Johnson (trj2j)  
**IT Support:** Mark Outten (wmo4b), Ben Hartless (bh4hb)  
**Date:** May 11, 2026  
**Status:** Pre-IRB Architecture Proposal  
**Revision:** 1.1 (updated to reflect Docker + A/B testing design)

## Executive Summary

AGCO is a RAG-based (Retrieval-Augmented Generation) chatbot that provides agricultural extension guidance to field workers in Lesotho. The system uses open-weight LLMs deployed on UVA AWS infrastructure to answer questions grounded in a corpus of agricultural extension documents, including multimodal content (text + diagrams). This is a **randomized controlled trial (RCT)** with treatment (LLM-enhanced) and control (baseline) conditions. Architecture addresses compliance requirements under UVA policy, US export control, and Lesotho's Data Protection Act (2021).

**Key Design Principles:**
- **Research-first:** A/B testing with treatment/control groups, structured logging for evaluation
- **Privacy-first:** Pseudonymous identifiers only (enumerator ID + farmer study ID), no PII collection
- **Cost-sustainable:** Stop EC2 instances outside work hours (~$100-150/month), open-weight models
- **Latency-optimized:** Cape Town (af-south-1) deployment for <100ms RTT to Lesotho
- **Grounded responses:** Refuse to answer when source documents don't support the query
- **Offline-ready:** May pivot to tablet-based deployment with local LLMs if connectivity is poor

---

## 1. System Architecture

### 1.1 High-Level Components (Cloud Deployment)

```
┌─────────────────────────────────────────────────┐
│  Extension Workers (Lesotho) - 17 total         │
│  ┌─────────────┐            ┌─────────────┐     │
│  │ Treatment   │            │  Control    │     │
│  │ Group (~9)  │            │  Group (~8) │     │
│  │ Tablets     │            │  Tablets    │     │
│  └──────┬──────┘            └──────┬──────┘     │
│         │ HTTPS                    │ HTTPS      │
└─────────┼──────────────────────────┼────────────┘
          │                          │
          ▼                          ▼
┌─────────────────────────────────────────────────────────┐
│           Cloudflare Zero Trust                         │
│  (Authentication, DDoS protection, opaque ID injection) │
└─────────────────┬───────────────────────────────────────┘
                  │
          ┌───────┴────────┐
          │                │
          ▼                ▼
┌──────────────────┐  ┌──────────────────┐
│  Treatment       │  │  Control         │
│  Container       │  │  Container       │
│  (LLM-enhanced)  │  │  (Baseline)      │
├──────────────────┤  ├──────────────────┤
│ - FastAPI/Flask  │  │ - FastAPI/Flask  │
│ - RAG (hybrid)   │  │ - Simple search  │
│ - llama.cpp      │  │ - No LLM         │
│ - ChromaDB       │  │ - BM25 only      │
└────────┬─────────┘  └────────┬─────────┘
         │                     │
         │   Structured logs (JSON/JSONL)
         └──────────┬──────────┘
                    ▼
         ┌─────────────────────┐
         │  S3 Bucket          │
         │  (Encrypted logs)   │
         │  us-east-1          │
         └─────────────────────┘

EC2 Instance (G5/G6, 24GB VRAM)
AWS af-south-1 (Cape Town)
Docker Compose orchestration
```

### 1.2 Deployment Topology

**Primary Compute (AWS af-south-1, Cape Town):**
- **EC2 Instance:** `g5.xlarge` or `g6.xlarge` (24GB VRAM, NVIDIA GPU)
  - Treatment container: RAG app + llama.cpp + ChromaDB
  - Control container: Baseline search app (BM25 only, no LLM)
- **Orchestration:** Docker Compose (not Kubernetes — overkill for 17 users)
- **Elastic IP:** Static IP for DNS mapping
- **Operating Hours:** 8am-6pm Lesotho time (UTC+2), stopped outside work hours
  - ~10 hours/day × 20 workdays/month = 200 compute hours/month
  - Cost: ~$0.60/hour = **~$120/month** (vs. $450 if always-on)

**Data Storage (AWS us-east-1):**
- **S3 Bucket:** Encrypted (SSE-KMS), block public access, restricted IAM
  - Logs: JSON/JSONL format (interactions, retrieval events, exit surveys)
  - Exports: Weekly automated exports for analysis
  - Lifecycle: Hot (90 days) → Archive (2 years) → Delete
- **No CloudWatch Logs** (cost optimization — S3 sufficient)
- **No DynamoDB** (consent + user data in JSONL files in S3)

**Authentication (Cloudflare Zero Trust):**
- Handles auth outside application layer
- Injects opaque identifiers into request headers:
  - `X-Enumerator-ID`: UUID for extension worker
  - `X-Study-ID`: UUID for farmer/client
- App never sees real names, emails, or other PII
- Apps are stateless — no session management required

**Why af-south-1?**
- Lesotho → Cape Town: ~50ms RTT (vs. 250-300ms to us-east-1)
- Data processing geographically closer to data subjects
- Still within UVA Enterprise Cloud governance

### 1.3 Offline Tablet Deployment (Contingency)

**Trigger:** If partner requests offline capability due to poor rural connectivity

```
┌────────────────────────────────────┐
│  Android Tablet (Offline)          │
│  ┌──────────────────────────────┐  │
│  │  APK with embedded models:   │  │
│  │  - Tiny LLM (1-3B, quantized)│  │
│  │  - ChromaDB Lite             │  │
│  │  - Local PDF corpus          │  │
│  └──────────────┬───────────────┘  │
│                 │                   │
│  ┌──────────────▼───────────────┐  │
│  │  Local JSONL Log Storage     │  │
│  └──────────────┬───────────────┘  │
│                 │                   │
│  ┌──────────────▼───────────────┐  │
│  │  "Send Data" Button          │  │
│  │  (uploads when WiFi avail)   │  │
│  └──────────────┬───────────────┘  │
└─────────────────┼───────────────────┘
                  │ WiFi/4G (when available)
                  ▼
         ┌─────────────────────┐
         │  S3 Bucket          │
         │  (Centralized logs) │
         └─────────────────────┘
```

**Offline Architecture Notes:**
- Model: Phi-3-mini (3.8B, 2GB quantized) or TinyLlama (1.1B)
- Storage: ~500MB corpus + 100MB model + 50MB app = 650MB total
- Data sync: Push logs to S3 when WiFi available (e.g., end of day at office)
- Compliance: Logs stored on device temporarily, encrypted at rest (Android Keystore)
- IRB consideration: Data on tablets = different risk profile, needs explicit consent disclosure

**Decision Point:** Pilot cloud deployment first (June-July). If >20% of queries timeout due to connectivity, evaluate offline pivot (August).

---

## 2. Data Flow & Privacy

### 2.1 User Journey (Cloud Deployment)

**1. First Visit:**
- Worker navigates to app URL (e.g., `agco-treatment.batten.virginia.edu` or `agco-control.batten.virginia.edu`)
- Cloudflare Zero Trust challenges for auth:
  - Email-based magic link (for non-UVA workers)
  - OR NetBadge (for UVA staff during pilot testing)
- **Consent screen** (mandatory, before app access):
  - Discloses: AI processing, A/B testing (treatment vs control), cross-border data flow, retention period
  - Available in English and Sesotho
  - Records consent to S3 as JSONL entry:
    ```json
    {
      "event": "consent",
      "timestamp": "2026-07-15T08:32:14Z",
      "enumerator_id": "uuid-worker-123",
      "consent_version": "1.0",
      "language": "sesotho",
      "ip_hash": "sha256-of-ip"
    }
    ```
- Cloudflare injects `X-Enumerator-ID` into all subsequent requests

**2. Chat Session (Treatment Group):**
- Worker asks question on behalf of farmer
- App logs query event:
  ```json
  {
    "event": "query",
    "timestamp": "2026-07-15T09:15:22Z",
    "enumerator_id": "uuid-worker-123",
    "study_id": "uuid-farmer-456",
    "query_hash": "sha256-of-query",
    "query_length": 42,
    "language_detected": "en"
  }
  ```
- App performs hybrid retrieval (semantic + BM25 + literal)
- Logs retrieval event:
  ```json
  {
    "event": "retrieval",
    "timestamp": "2026-07-15T09:15:23Z",
    "enumerator_id": "uuid-worker-123",
    "study_id": "uuid-farmer-456",
    "query_hash": "sha256-of-query",
    "top_chunks": [
      {"source": "ipm_guide_2024.pdf", "page": 17, "score": 0.89},
      {"source": "ipm_guide_2024.pdf", "page": 18, "score": 0.84}
    ],
    "retrieval_latency_ms": 850
  }
  ```
- App sends context + query to llama.cpp → LLM generates response
- Logs response event:
  ```json
  {
    "event": "response",
    "timestamp": "2026-07-15T09:15:26Z",
    "enumerator_id": "uuid-worker-123",
    "study_id": "uuid-farmer-456",
    "query_hash": "sha256-of-query",
    "response_hash": "sha256-of-response",
    "response_length": 142,
    "citations": [3, 7],
    "refusal": false,
    "model_latency_ms": 2800
  }
  ```
- Response streamed back to worker's tablet

**3. Chat Session (Control Group):**
- Same logging structure, but:
  - No LLM (BM25 search only)
  - Returns top 3 relevant document snippets with page numbers
  - No citations, no natural language generation
  - Worker reads snippets and advises farmer directly

**4. Exit Survey (End of Day):**
- Worker completes optional survey: "How helpful was the tool today?" (1-5 scale)
- Logs survey response:
  ```json
  {
    "event": "exit_survey",
    "timestamp": "2026-07-15T17:45:00Z",
    "enumerator_id": "uuid-worker-123",
    "helpfulness_rating": 4,
    "queries_today": 12
  }
  ```

### 2.2 What Gets Logged?

| Data Element | Storage Location | Retention | Purpose | PII? |
|--------------|------------------|-----------|---------|------|
| **Enumerator ID** | S3 (JSONL) | 2 years | Link queries to worker (pseudonymous) | No |
| **Study ID** | S3 (JSONL) | 2 years | Link queries to farmer (pseudonymous) | No |
| **Query hash** | S3 (JSONL) | 2 years | Deduplication, usage metrics | No |
| **Full query text** | S3 (separate file) | 2 years | Research evaluation | Maybe* |
| **Full response text** | S3 (separate file) | 2 years | Quality assessment | No |
| **Retrieval chunks** | S3 (JSONL) | 2 years | Citation accuracy analysis | No |
| **Latency metrics** | S3 (JSONL) | 2 years | Performance monitoring | No |
| **Exit survey responses** | S3 (JSONL) | 2 years | RCT outcome measurement | No |
| **IP address** | Not logged (only hash for abuse detection) | N/A | Privacy | No |
| **Session recordings** | Not logged | N/A | Privacy | N/A |

*Full query text may contain incidental mentions of names ("My neighbor John has aphids"), but enumerators are trained to use generic language ("A farmer has aphids"). PII detection filter flags suspicious patterns.

### 2.3 PII Protection

**No Direct PII Collection:**
- Enumerator IDs and Study IDs are UUIDs assigned at onboarding (external to this system)
- Mapping table (UUID → Real Name) stored separately by partner org, never shared with UVA
- Apps never prompt for names, emails, phone numbers, addresses

**PII Detection in Queries (Planned):**
- Pre-processing filter checks for:
  - Personal names (pattern: "I am [Name]", "My name is", "John's farm")
  - Phone numbers (Lesotho format: +266 XXXX XXXX)
  - GPS coordinates (pattern: -29.XX, 28.XX)
  - Village names (from pre-populated list of study sites)
- If detected: Warning shown to enumerator: "Your question may contain personal information. Rephrase to remove names or locations."
- If enumerator proceeds: Query logged but flagged with `"pii_warning": true` for manual review

**Right to Deletion:**
- Email: agco-support@virginia.edu with Enumerator ID
- Manual process (until scale justifies automation):
  1. Verify requestor is legitimate (partner org confirms)
  2. Run script to delete all S3 objects where `enumerator_id` matches
  3. Confirm deletion, send receipt to requestor
- SLA: 7 business days (Lesotho DPA requires "without undue delay")

**Data Exports for Analysis:**
- Weekly: Automated export of logs to UVA Dataverse (restricted access)
- De-identified further for publication: Strip enumerator IDs, round timestamps to day-level

---

## 3. Treatment vs. Control Architecture

### 3.1 Treatment Container (LLM-Enhanced)

**Components:**
- **Web Framework:** FastAPI (async, faster than Flask for LLM streaming)
- **Retrieval Engine:** Hybrid (semantic + BM25 + literal), same as prototype
- **Vector DB:** ChromaDB (persistent volume)
- **LLM Server:** llama.cpp with OpenAI-compatible API
- **Model:** TBD (Mistral-7B-Instruct or Llama-3.1-8B, Q4_K_M quantization)
- **Multimodal RAG:** Pre-generated image descriptions (see Section 3.3)

**User Experience:**
- Chat interface (similar to prototype)
- Natural language responses with inline citations (e.g., [3][7])
- Displays source images inline when cited (cached from corpus)
- Refusal when context doesn't support answer

**Dockerfile (Simplified):**
```dockerfile
FROM nvidia/cuda:12.2.0-runtime-ubuntu22.04
RUN apt-get update && apt-get install -y python3.11 python3-pip
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY app/ /app
COPY index/ /index
COPY corpus/ /corpus
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### 3.2 Control Container (Baseline Search)

**Components:**
- **Web Framework:** FastAPI (same as treatment, for consistency)
- **Search Engine:** BM25 only (rank_bm25 library)
- **No LLM:** Just returns top 3 document snippets
- **No Vector DB:** Text corpus loaded into memory at startup

**User Experience:**
- Search interface (not chat — single query box)
- Returns list of 3 relevant passages with metadata:
  ```
  1. IPM Guide 2024, page 17:
     "Bagrada bugs can be controlled through integrated pest management. 
      Practices include crop rotation, intercropping with marigolds..."
     
  2. IPM Guide 2024, page 18:
     "Botanical pesticides such as neem oil are effective against many 
      sucking insects including aphids and small bugs..."
  
  3. FAO Climate-Smart Agriculture, page 42:
     "Early sowing helps plants establish before pest pressure peaks..."
  ```
- Worker reads passages, synthesizes advice for farmer (tests if LLM adds value)

**Why This Control?**
- Tests the hypothesis: "Does LLM synthesis improve extension worker effectiveness vs. raw document search?"
- If control group performs equally well → LLM not worth the cost/complexity
- If treatment group outperforms → LLM provides value

### 3.3 Multimodal RAG Strategy

**Problem:**
Source PDFs contain diagrams (pest identification, irrigation systems, crop spacing) that are critical for advice.

**Option A: Live Image-to-Text (Rejected for Now):**
- Pros: Most accurate, can handle new images
- Cons: Requires second model (e.g., LLaVA 7B) or larger instance, adds latency, higher hallucination risk

**Option B: Pre-Generated Image Descriptions (Chosen):**
1. **Offline Preprocessing (One-Time):**
   - Extract all images from PDFs using PyMuPDF
   - Use powerful vision-language model (e.g., GPT-4-Vision, Claude 3.5 Sonnet, or open-weight LLaVA 13B)
   - Generate detailed descriptions:
     ```json
     {
       "image_id": "ipm_guide_2024_p17_fig3.png",
       "caption": "Diagram showing bagrada bug life cycle",
       "detailed_description": "Four-panel illustration. Panel 1: Adult bagrada bug, 
         shield-shaped, black and orange markings, 5-7mm length. Panel 2: Egg cluster 
         on underside of cabbage leaf, white, barrel-shaped, 1mm diameter. Panel 3: 
         Five nymph stages, progressively larger, orange to black color gradient. 
         Panel 4: Damage symptoms on crucifer leaves, small circular holes, yellowing."
     }
     ```
   - Store descriptions in ChromaDB alongside text chunks
   - Store original images in `/corpus/images/` for display

2. **During Inference (Real-Time):**
   - Retrieval returns text chunks (including image descriptions)
   - LLM references "text about the picture" to generate response
   - If LLM cites chunk containing image description, app displays original image inline
   - Example response:
     ```
     Bagrada bugs have orange and black markings and are 5-7mm long [3]. 
     You can identify them by the shield shape and the small circular holes 
     they leave on cabbage and other crucifers [3].
     
     [Image: bagrada_bug_lifecycle.png]
     ```

**Benefits:**
- Lower VRAM requirement (no vision model needed at inference)
- Faster response (no image processing delay)
- Lower hallucination risk (powerful offline model, human-verified descriptions)
- Embeddings capture both text and visual semantics

**Cost:**
- One-time preprocessing: ~$50 (500 images × $0.10 per GPT-4-Vision call)
- Or use open-weight LLaVA 13B (free, but slower and requires GPU for offline processing)

**Human Review Loop:**
- Research assistant spot-checks 10% of descriptions for accuracy
- Corrections fed back into corpus before indexing

---

## 4. Model Selection & Inference

### 4.1 Hardware Constraints

**EC2 Instance Options (AWS af-south-1):**

| Instance Type | GPU | VRAM | vCPU | RAM | On-Demand ($/hr) | Use Case |
|---------------|-----|------|------|-----|------------------|----------|
| **g5.xlarge** | A10G | 24GB | 4 | 16GB | $1.01 | 7-8B models, good price/performance |
| **g5.2xlarge** | A10G | 24GB | 8 | 32GB | $1.21 | Same GPU, more CPU for preprocessing |
| **g6.xlarge** | L4 | 24GB | 4 | 16GB | $0.90 | Newer, more efficient (if available in af-south-1) |
| **g5.4xlarge** | A10G | 24GB | 16 | 64GB | $1.63 | Overkill unless multimodal pivot |

**Recommendation:** Start with **g5.xlarge** ($1.01/hr × 200 hrs/month = $202/month). If latency >3s, upgrade to g5.2xlarge.

### 4.2 Model Candidates

**Constraints:**
- Must fit in 24GB VRAM (Q4_K_M quantization → ~4.5GB for 7B model)
- Must support 8K+ context window (RAG context + conversation history)
- Must have strong instruction-following (agricultural Q&A requires nuance)
- License must permit commercial research use + export to Lesotho

**Top Candidates:**

| Model | Size | Context | License | Pros | Cons |
|-------|------|---------|---------|------|------|
| **Mistral-7B-Instruct-v0.3** | 7B | 32K | Apache 2.0 | Strong reasoning, multilingual, large context | May be overly verbose |
| **Llama-3.1-8B-Instruct** | 8B | 128K | Meta Community | Best-in-class 8B, huge context | Slightly larger (5GB quantized) |
| **Phi-3-Medium** | 14B | 128K | MIT | Strong factual accuracy | Requires g5.2xlarge (9GB quantized) |
| **Qwen2.5-7B-Instruct** | 7B | 128K | Apache 2.0 | Strong multilingual (good for future Sesotho) | Less tested in production |

**Evaluation Plan:**
1. Create golden Q&A set (50 agricultural questions, expert-validated answers)
2. Benchmark all 4 models on:
   - **Citation accuracy:** Do cited chunks support the claim? (automated check)
   - **Refusal rate:** Does it refuse when context is insufficient? (10-20% target)
   - **BLEU/ROUGE vs. gold answers:** Rough proxy for correctness
   - **Latency:** p95 response time on g5.xlarge
3. Select winner by **June 3, 2026**

**Preliminary Recommendation:** **Llama-3.1-8B-Instruct** (best balance of quality, context, and license freedom).

### 4.3 Quantization Strategy

**Why Quantize?**
- FP16 model: 7B × 2 bytes = 14GB VRAM (+ 4GB for context + activations = 18GB)
- Q4_K_M (4-bit): 7B × 0.5 bytes = 3.5GB VRAM (+ 4GB overhead = 7.5GB total)
- Leaves 16GB free for larger batches, longer context, or future model upgrades

**Quantization Method:**
- Use llama.cpp's built-in quantizer
- Format: GGUF (llama.cpp native)
- Method: Q4_K_M (4-bit, medium quality — best speed/quality tradeoff)
- Quality loss: Typically <2% on benchmarks vs FP16

**Command (Example):**
```bash
./llama.cpp/quantize \
  models/Llama-3.1-8B-Instruct-fp16.gguf \
  models/Llama-3.1-8B-Instruct-Q4_K_M.gguf \
  Q4_K_M
```

---

## 5. Cost Analysis

### 5.1 Cloud Deployment (Treatment + Control)

**Monthly Costs (July 2026 - July 2028):**

| Item | Calculation | Cost/Month |
|------|-------------|------------|
| **EC2 g5.xlarge** | $1.01/hr × 10 hrs/day × 20 days | $202 |
| **Elastic IP** | $3.60/month (when instance stopped) | $4 |
| **S3 Storage** | ~10GB logs/month × $0.023/GB | $0.23 |
| **S3 PUT requests** | ~1M events × $0.005/1K requests | $5 |
| **Data transfer (af-south-1 → us-east-1)** | ~5GB/month × $0.09/GB | $0.45 |
| **Cloudflare Zero Trust** | 50 seats (17 workers + staff) × $7/seat | $350 |
| **Total** | | **$561/month** |

**WAIT — Cloudflare too expensive. Alternative auth options:**

| Auth Option | Cost/Month | Pros | Cons |
|-------------|------------|------|------|
| **Cloudflare Zero Trust** | $350 | Easy, DDoS protection, opaque ID injection | High cost for 17 users |
| **Auth0 (Essential)** | $35 | Professional, SAML/OAuth | Overkill for this scale |
| **DIY (FastAPI + JWT)** | $0 | Full control, no vendor lock-in | More dev work, no DDoS protection |
| **AWS Cognito** | ~$5 | AWS-native, integrates with IAM | UX less polished than Auth0 |

**Revised Recommendation:** Use **AWS Cognito** for auth (email magic links) + **Cloudflare Free** (DNS + basic DDoS only).

**Revised Monthly Cost:**
- EC2: $202
- S3: $6
- Cognito: $5
- Data transfer: $0.45
- **Total: ~$213/month**

**24-Month Total:** $213 × 24 = **$5,112**

### 5.2 One-Time Costs

| Item | Cost | Notes |
|------|------|-------|
| **Image description preprocessing** | $50 | GPT-4-Vision for 500 images (or free if using LLaVA locally) |
| **Sesotho translation** | $500 | Consent form + UI strings |
| **Golden Q&A set (expert time)** | $1,000 | Agricultural expert, 10 hours @ $100/hr |
| **Load testing tools** | $0 | Locust (open-source) |
| **Total** | **$1,550** |

### 5.3 Offline Tablet Deployment (Contingency)

**If pivot to offline tablets is required:**

| Item | Cost | Notes |
|------|------|-------|
| **Android app development** | $5,000 | 2 weeks dev time @ $2,500/week |
| **Tiny LLM packaging** | $0 | Phi-3-mini (3.8B) is MIT licensed |
| **17 tablets (if not provided)** | $3,400 | $200/tablet (Samsung Galaxy Tab A8) |
| **MDM (Mobile Device Management)** | $100/month | Remote app updates, device tracking |
| **S3 storage (unchanged)** | $6/month | Centralized log collection |
| **Total (one-time)** | **$8,400** | |
| **Total (monthly)** | **$106** | |

**Decision:** Only pursue if cloud deployment fails pilot (July 2026).

---

## 6. Security & Access Control

### 6.1 Authentication Flow (AWS Cognito)

```
1. Worker navigates to app URL
   ↓
2. App checks for JWT in cookie
   ↓
3. If no JWT: Redirect to Cognito hosted UI
   ↓
4. Cognito prompts for email (magic link)
   ↓
5. Worker clicks link in email → Cognito validates
   ↓
6. Cognito issues JWT, redirects back to app
   ↓
7. App validates JWT signature, extracts claims:
   {
     "sub": "uuid-cognito-user-id",
     "email": "worker@partner-org.ls",
     "custom:enumerator_id": "uuid-worker-123",
     "custom:group": "treatment"
   }
   ↓
8. App uses custom:enumerator_id for all logging
   ↓
9. App routes to treatment or control container based on custom:group
```

**JWT Validation:**
- App downloads Cognito public keys at startup (JWKS endpoint)
- Validates signature, expiration, issuer on every request
- No shared secrets (all cryptographic validation)

**User Provisioning:**
- Partner org provides list: `[{email, enumerator_id, group}, ...]`
- UVA admin bulk-creates Cognito users via AWS CLI
- Workers receive invitation email with magic link

### 6.2 Network Security

**VPC Configuration:**
- Private subnet: EC2 instances (no direct internet access)
- Public subnet: Application Load Balancer (ALB) only
- Security groups:
  - ALB: Inbound HTTPS (443) from internet, outbound to EC2 (8000)
  - EC2: Inbound port 8000 from ALB only, outbound HTTPS to S3/internet
- No SSH access (use AWS Systems Manager Session Manager for emergency access)

**TLS Configuration:**
- ALB terminates TLS (ACM-managed certificate, auto-renewal)
- Certificate: `*.batten.virginia.edu` (wildcard for treatment/control subdomains)
- Protocols: TLS 1.2+ only, disable weak ciphers (ECDHE-RSA-AES128-GCM-SHA256 minimum)

**Secrets Management:**
- No hardcoded secrets in code or Dockerfiles
- AWS Systems Manager Parameter Store:
  - `/agco/treatment/llm-api-key` → random 32-char token
  - `/agco/s3/log-bucket` → bucket name
- Containers read parameters at startup via IAM role (no credentials in env vars)

### 6.3 Data Protection

**Encryption at Rest:**
- S3: SSE-KMS with UVA-managed key
- EC2 EBS volumes: Encrypted with default AWS-managed key
- Offline tablets (if deployed): Android Keystore, user passcode required

**Encryption in Transit:**
- Browser ↔ ALB: TLS 1.3
- ALB ↔ EC2: Unencrypted (within VPC, acceptable per UVA policy)
- EC2 ↔ S3: TLS 1.2+ (AWS SDK default)

**Access Control (IAM Roles):**
- EC2 instance role:
  - `s3:PutObject` on log bucket only (no read, no delete)
  - `ssm:GetParameter` on `/agco/*` parameters only
  - No other permissions (principle of least privilege)
- Admin role (for UVA IT):
  - `s3:GetObject`, `s3:DeleteObject` on log bucket (for deletion requests)
  - `ec2:*`, `ecs:*` for deployment management
  - `logs:*` for debugging

**Audit Logging:**
- AWS CloudTrail: Logs all API calls (S3 access, parameter reads, EC2 changes)
- Retention: 7 years (UVA policy)
- Alerts: Email to Mark/Ben if unexpected access patterns (e.g., S3 bucket made public)

---

## 7. Compliance Checklist

### 7.1 Lesotho Data Protection Act (2021)

| Requirement | Implementation | Status |
|-------------|----------------|--------|
| **Lawful basis** | Research (DPA Section 9) + Consent (Section 8) | ✅ Consent form |
| **Data minimization** | Pseudonymous IDs only, no PII collection | ✅ By design |
| **Purpose limitation** | Data used only for research, not repurposed | ✅ Stated in consent |
| **Storage limitation** | 2 years → delete (automated S3 lifecycle) | ✅ Configured |
| **Right to access** | Email request → manual export of user's logs | 🔄 Process documented |
| **Right to erasure** | Email request → S3 deletion script | 🔄 Script to implement |
| **Cross-border transfer** | Adequate safeguards (AWS SOC 2, DUA with partner) | ✅ DUA in progress |
| **Data breach notification** | 72 hours to Lesotho Data Protection Office | ✅ Incident plan (Sec 7.4) |
| **Data Protection Officer** | Molly Lipscomb (PI) designated as contact | ✅ Listed in consent |

### 7.2 UVA Policies

| Policy | Requirement | Implementation |
|--------|-------------|----------------|
| **IRM-003 (Sensitive Data)** | Encryption at rest & in transit | ✅ S3 SSE-KMS, TLS 1.2+ |
| **IRM-004 (Research Data)** | Secure storage, access logging, retention limits | ✅ S3 + CloudTrail + lifecycle |
| **IRM-001 (Accessibility)** | WCAG 2.1 AA compliance | 🔄 UI audit pending |
| **Export Control (EAR)** | Verify no ITAR/EAR restrictions on models | ✅ Llama/Mistral are open-weight, Apache/Meta licenses |

### 7.3 IRB Submission

**Required Documents:**
1. Protocol narrative (Molly)
2. Informed consent form (English + Sesotho) (Molly)
3. Data Use Agreement with partner org (Molly + partner)
4. This architecture document (Ben)
5. Data Protection Impact Assessment (Molly + UVA Compliance)
6. Model evaluation report (Terry)
7. Security assessment (Mark/Ben)
8. Recruitment materials (Molly)

**Key IRB Talking Points:**
- **Minimal risk:** Workers are trained professionals, chatbot is decision-support (not autonomous)
- **Pseudonymity:** No PII collected, enumerator IDs are opaque
- **Withdrawal:** Workers can stop using tool anytime, data deletion available
- **RCT ethics:** Random assignment to treatment/control is standard for research, both groups get access to source documents
- **Data security:** Encryption, access controls, audit logging per UVA standards
- **Cross-border:** DUA addresses Lesotho DPA requirements, AWS SOC 2 certified

---

## 8. Operational Plan

### 8.1 Deployment Process

**Phase 1: Infrastructure Setup (Post-IRB Approval, Week 1)**
1. Create sub-account under Batten's AWS Enterprise Cloud (Mark)
2. Enable af-south-1 region
3. Provision VPC, subnets, security groups, ALB
4. Create S3 bucket, configure encryption + lifecycle policy
5. Set up Cognito user pool, configure email magic links
6. Request TLS cert from ACM for `*.batten.virginia.edu`

**Phase 2: Application Deployment (Week 1-2)**
1. Build Docker images (treatment + control) (Terry)
2. Push to AWS ECR (Elastic Container Registry)
3. Launch EC2 g5.xlarge instance
4. Install Docker + Docker Compose
5. Create docker-compose.yml:
   ```yaml
   version: '3.8'
   services:
     treatment:
       image: <account-id>.dkr.ecr.af-south-1.amazonaws.com/agco-treatment:latest
       ports:
         - "8000:8000"
       volumes:
         - /opt/agco/index:/index
         - /opt/agco/corpus:/corpus
       environment:
         S3_BUCKET: ${S3_BUCKET}
         LLM_API_KEY: ${LLM_API_KEY}
       deploy:
         resources:
           reservations:
             devices:
               - driver: nvidia
                 count: 1
                 capabilities: [gpu]
     
     control:
       image: <account-id>.dkr.ecr.af-south-1.amazonaws.com/agco-control:latest
       ports:
         - "8001:8000"
       volumes:
         - /opt/agco/corpus:/corpus
       environment:
         S3_BUCKET: ${S3_BUCKET}
   ```
6. Start containers: `docker-compose up -d`
7. Configure ALB target groups (treatment:8000, control:8001)
8. Route based on path: `/treatment/*` → port 8000, `/control/*` → port 8001

**Phase 3: Data Pipeline (Week 2)**
1. Build corpus index (run ingest.py with multimodal preprocessing) (Terry)
2. Test S3 logging (generate test events, verify in bucket)
3. Set up automated export script (cron job, weekly)

**Phase 4: Testing (Week 2-3)**
1. Smoke test: 2 test accounts (one treatment, one control)
2. Load test: Locust with 17 concurrent users, 10 queries/user
3. Golden Q&A evaluation: Run automated metrics
4. Accessibility audit: WAVE, axe DevTools, manual screen reader test
5. Security scan: OWASP ZAP, AWS Inspector

**Phase 5: Pilot Launch (Week 3)**
1. Provision 17 Cognito accounts (partner org provides emails)
2. Send invitation emails
3. 1-hour training Zoom (Molly): How to use tool, interpret citations, report issues
4. Monitor daily for first week (Terry/Mark)

### 8.2 Instance Scheduling

**Goal:** Run EC2 only during Lesotho work hours (8am-6pm, UTC+2), save ~60% on compute.

**Implementation:**
- AWS EventBridge rules:
  - Rule 1: Trigger Lambda at 06:00 UTC (8am Lesotho) → `ec2:StartInstances`
  - Rule 2: Trigger Lambda at 16:00 UTC (6pm Lesotho) → `ec2:StopInstances`
- Lambda function:
  ```python
  import boto3
  ec2 = boto3.client('ec2', region_name='af-south-1')
  
  def lambda_handler(event, context):
      action = event['action']  # 'start' or 'stop'
      instance_id = 'i-0123456789abcdef0'
      
      if action == 'start':
          ec2.start_instances(InstanceIds=[instance_id])
      elif action == 'stop':
          ec2.stop_instances(InstanceIds=[instance_id])
      
      return {'statusCode': 200}
  ```
- Docker Compose configured with `restart: unless-stopped` (containers auto-start when instance starts)

**Manual Override:**
- On-call person can manually start instance via AWS console if workers need access outside hours
- Consider: Public holidays, special events (adjust EventBridge schedule as needed)

### 8.3 Monitoring & Alerts

**CloudWatch Metrics (Published by App):**
- `agco.query.count` (per minute)
- `agco.query.latency` (p50, p95, p99)
- `agco.retrieval.latency`
- `agco.llm.latency`
- `agco.error.count`
- `agco.refusal.count`

**CloudWatch Alarms:**
- Error rate >5% for 5 minutes → Email Mark/Ben
- p95 latency >5s for 5 minutes → Email Terry
- Instance CPU >80% for 10 minutes → Email Mark (may need bigger instance)
- Disk usage >90% → Email Ben

**Manual Checks (Weekly):**
- Review S3 logs for PII warnings (flagged queries)
- Check for abuse patterns (same enumerator, >50 queries/day)
- Review exit survey responses (detect usability issues)

### 8.4 Incident Response Plan

**Scenario 1: Application Down (No Response)**
1. Check EC2 instance state (is it running?)
2. SSH via Session Manager: `docker ps` (are containers running?)
3. Check logs: `docker logs agco-treatment`
4. If OOM (out of memory): Restart container or upgrade instance
5. If model server crashed: Check llama.cpp logs, may need model reload
6. If persistent: Rollback to previous Docker image

**Scenario 2: Data Breach (S3 Bucket Exposed)**
1. Immediately block public access (S3 console: "Block all public access")
2. Review CloudTrail logs (who changed bucket policy? when?)
3. Notify UVA InfoSec: security@virginia.edu
4. Assess: Was data downloaded? (S3 access logs → who, what, when)
5. If PII exposed: Notify Lesotho Data Protection Office within 72 hours (email dpo@lesotho.gov.ls or equivalent)
6. If confirmed breach: Notify affected enumerators via partner org
7. Post-mortem: Update IAM policies to prevent recurrence

**Scenario 3: Bad Advice Reported**
1. Enumerator reports: "The bot told me to use pesticide X, but that's not recommended for crop Y"
2. Log incident in spreadsheet: Date, Enumerator ID, Query, Response, Issue
3. Terry investigates: Check retrieval chunks (did context support the advice?)
4. If retrieval error: Add negative example to golden set, retrain (if using fine-tuning)
5. If model hallucination: Add stricter refusal prompt, consider switching models
6. If corpus error: Correct source PDF, rebuild index
7. Notify enumerator of resolution, offer to delete incorrect interaction from logs

**Scenario 4: High Costs (AWS Bill >$500)**
1. Check Cost Explorer: What service? (likely EC2 if instance left running)
2. Verify EventBridge schedule (is auto-stop working?)
3. Check for unexpected traffic (DDoS? Abuse?)
4. If legit usage: Evaluate if budget increase is justified
5. If abuse: Block offending IPs, review auth logs

---

## 9. Open Questions & Decisions Needed

### 9.1 For Terry (Technical)

1. **Model selection:** Which model performs best on golden Q&A set? (Due: June 3)
2. **Multimodal preprocessing:** Will you use GPT-4-Vision ($50) or open-weight LLaVA (free)? (Due: May 24)
3. **Control condition:** Should control use BM25 only, or BM25 + semantic (no LLM)? (Discuss: May 15)
4. **Golden Q&A set:** Can you recruit an agricultural extension expert to validate answers? (Due: May 31)
5. **Offline pivot:** What's the latency threshold to trigger tablet deployment? (Suggest: >20% queries timeout)

### 9.2 For Molly (Research)

1. **In-country partner:** Who is the Lesotho organization? Contact person? (Due: May 15)
2. **Enumerator/farmer ID mapping:** Who maintains the UUID → Real Name mapping? (Partner org?)
3. **Treatment assignment:** Random or stratified by geography/experience? (Affects Cognito provisioning)
4. **RCT duration:** How long will study run? (Affects cost, data retention)
5. **Success metrics:** What defines "LLM-enhanced is better"? (Queries/day? Farmer satisfaction? Yield?)
6. **Publication plan:** Will corpus be public? (Affects copyright clearance)

### 9.3 For Mark/Ben (Infrastructure)

1. **AWS sub-account:** Can this be set up by May 17? (Critical path for infrastructure)
2. **af-south-1 availability:** Is this region already enabled in Batten's Enterprise Cloud? (Check ASAP)
3. **Budget approval:** Who signs off on $5K for 24 months? Grant code? (Due: May 15)
4. **Backup strategy:** Daily EBS snapshots, or just Git + S3 logs? (Decision: May 20)
5. **On-call rotation:** Mark primary, Ben backup? What's the SLA? (Decision: May 20)

### 9.4 For UVA Compliance

1. **Export control:** Does AWS Cape Town trigger any EAR/ITAR concerns? (Check: May 17)
2. **Data Use Agreement:** UVA template exists for international research data sharing? (Check: May 17)
3. **Incident response:** If data breach, who at UVA coordinates with Lesotho authorities? (Clarify: May 20)
4. **IRB timeline:** Can expedited review shorten approval time? (Ask: May 15)

---

## 10. Success Criteria

### 10.1 Pilot Success (July 2026, First Month)

- [ ] All 17 workers successfully log in
- [ ] >80% of workers submit ≥5 queries in first week
- [ ] <5% error rate (5XX responses, crashes, timeouts)
- [ ] p95 latency <3s (treatment group)
- [ ] 0 security incidents (no breaches, no abuse)
- [ ] Human review: >90% of treatment responses are "acceptable or better"
- [ ] Exit survey: Average helpfulness rating ≥3.5/5

### 10.2 6-Month Success (January 2027)

- [ ] ≥12 active workers (query ≥1×/month) in each group
- [ ] Treatment group: ≥300 queries/month
- [ ] Control group: ≥200 queries/month (if less, control is too frustrating to use → bad baseline)
- [ ] Refusal rate 10-20% (treatment group — not too aggressive, not too lenient)
- [ ] Citation accuracy >85% on monthly golden set runs
- [ ] Cost within budget: <$250/month (allows 15% buffer)

### 10.3 24-Month Success (July 2028, End of Study)

- [ ] RCT analysis complete: Treatment effect statistically significant (or null result is publishable)
- [ ] Paper submitted to peer-reviewed journal (e.g., Nature Food, PNAS, World Development)
- [ ] Corpus + code published to UVA Dataverse (if no copyright restrictions)
- [ ] Sustainability plan decided:
  - **Option A:** Partner org takes over (trained, runbooks provided)
  - **Option B:** UVA maintains (new funding secured)
  - **Option C:** Archive and sunset (data preserved, service shut down)

---

## Appendix A: Example Consent Form (English)

**AGCO Agricultural Chatbot - Informed Consent**

**Study Title:** Evaluating AI Tools for Agricultural Extension in Lesotho  
**Principal Investigator:** Dr. Molly Lipscomb, University of Virginia  
**IRB Protocol #:** [TBD]

**Purpose:**  
You are being asked to participate in a research study. We are testing whether an AI-powered chatbot can help extension workers provide better advice to farmers. This study compares two versions of the tool:
- **Treatment group:** AI chatbot that answers questions using agricultural documents
- **Control group:** Search tool that shows you relevant document passages (no AI)

You will be randomly assigned to one of these groups. Both tools use the same source documents from the Lesotho Ministry of Agriculture and international organizations.

**What will happen:**
- You will use the assigned tool when advising farmers (as often as you like)
- The system will record:
  - Your questions and the tool's responses (but not your name)
  - Which documents were used
  - How long it took to get an answer
  - Your daily feedback about how helpful the tool was
- You will be identified only by a code number (your real name is not recorded)

**Time commitment:**  
There is no required time commitment. Use the tool as much or as little as you find helpful during your normal extension work. The study will run for 2 years (July 2026 - July 2028).

**Risks:**
- **AI errors:** The AI version may occasionally give incorrect or incomplete advice. Do not rely solely on the tool for critical farming decisions. Always use your professional judgment and consult with supervisors when uncertain.
- **Data storage:** Your interactions will be stored on secure servers in South Africa and the United States. While we use strong security measures (encryption, access controls), no system is 100% secure.
- **Privacy:** Your name will not be recorded, but someone with access to both the study data and the code-number list (kept by [Partner Org]) could potentially identify your interactions.

**Benefits:**
- You will have 24/7 access to agricultural information to help farmers
- Your participation helps improve AI tools for extension workers worldwide
- No direct payment, but the tool is provided free of charge

**Privacy & data protection:**
- Your name will not be recorded in the study data
- Your interactions will be identified only by a code number
- Data will be stored securely for up to 2 years, then deleted
- Research results may be published, but you will not be identifiable
- Your data may be stored on servers in the United States (UVA uses Amazon Web Services, which has international security certifications)

**Your rights:**
- **Voluntary:** Participation is completely voluntary. You can stop using the tool at any time without penalty.
- **Withdrawal:** You can withdraw from the study at any time by emailing agco-support@virginia.edu
- **Data deletion:** You can request deletion of your data by emailing agco-support@virginia.edu with your code number. We will delete your data within 7 business days.
- **Questions:** Contact Dr. Molly Lipscomb at molly.lipscomb@virginia.edu or [Partner Org contact]

**IRB contact:**  
If you have questions about your rights as a research participant, contact the University of Virginia IRB at irb-hsr@virginia.edu or +1-434-924-5999.

**Statement of consent:**  
By clicking "I Agree" below, you confirm that:
- You have read and understood this form (or it was read to you)
- Your questions have been answered
- You agree to participate in this study
- You understand that your participation is voluntary and you can withdraw at any time

[ ] **I Agree** — I consent to participate in this study  
[ ] **I Do Not Agree** — I do not wish to participate (you will not be able to access the tool)

---

## Appendix B: Docker Compose Configuration

*This will be finalized during deployment. Placeholder shown for architecture clarity.*

```yaml
version: '3.8'

services:
  treatment:
    image: ${ECR_REGISTRY}/agco-treatment:${VERSION}
    container_name: agco-treatment
    restart: unless-stopped
    ports:
      - "8000:8000"
    volumes:
      - /opt/agco/index:/index:ro
      - /opt/agco/corpus:/corpus:ro
    environment:
      - S3_BUCKET=${S3_BUCKET}
      - LLM_API_KEY=${LLM_API_KEY}
      - COGNITO_USER_POOL_ID=${COGNITO_USER_POOL_ID}
      - COGNITO_REGION=af-south-1
      - LOG_LEVEL=INFO
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: 1
              capabilities: [gpu]
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3

  control:
    image: ${ECR_REGISTRY}/agco-control:${VERSION}
    container_name: agco-control
    restart: unless-stopped
    ports:
      - "8001:8000"
    volumes:
      - /opt/agco/corpus:/corpus:ro
    environment:
      - S3_BUCKET=${S3_BUCKET}
      - COGNITO_USER_POOL_ID=${COGNITO_USER_POOL_ID}
      - COGNITO_REGION=af-south-1
      - LOG_LEVEL=INFO
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
```

---

## Appendix C: System Health Metrics (Planned)

**Key Performance Indicators (Daily Dashboard):**
- **Uptime:** % of time both containers respond within 3s
- **Active Users:** Unique enumerator IDs seen in last 24 hours
- **Query Volume:** Total queries per day (treatment + control)
- **Treatment Metrics:**
  - Refusal rate: % of queries where LLM says "I can't find this in the documents"
  - Citation coverage: % of response sentences with citations
  - Average latency: p50, p95, p99
- **Control Metrics:**
  - Average latency: p50, p95, p99
  - Click-through rate: % of queries where user clicks a result snippet
- **Error Rate:** % of requests returning 5XX or timing out
- **Cost:** AWS spend to date vs. budget

**CloudWatch Dashboard URL:** (TBD after deployment)

---

## Document Revision History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 0.1 | 2026-05-08 | Ben Hartless | Initial draft (Streamlit-based architecture) |
| 1.0 | 2026-05-11 | Ben Hartless | Major revision: Docker + A/B testing, multimodal RAG, cost optimization, offline pivot |

---

**Status:** Ready for team review (May 12 meeting)

**Next Steps:**
1. Review with Terry, Molly, Mark (week of May 12)
2. Finalize model selection + golden Q&A set (Terry, by May 31)
3. Resolve open questions (Section 9)
4. Submit to IRB with this document as appendix (Molly, by June 15)
5. Provision AWS infrastructure (Mark/Ben, upon IRB approval)
6. Deploy + pilot with 17 workers (July 1)
