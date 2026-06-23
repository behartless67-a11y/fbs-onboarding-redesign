# CMMC-CCA (Certified CMMC Assessor) Study Guide

**Last Updated:** April 2026  
**Created for:** CCA Level 2 Certification Preparation

---

## Table of Contents
1. [Overview](#overview)
2. [Prerequisites](#prerequisites)
3. [Exam Structure](#exam-structure)
4. [Key Knowledge Domains](#key-knowledge-domains)
5. [NIST SP 800-171 Control Families](#nist-sp-800-171-control-families)
6. [CMMC Assessment Process](#cmmc-assessment-process)
7. [Assessment Roles & Responsibilities](#assessment-roles--responsibilities)
8. [Organizational Scoping](#organizational-scoping)
9. [Common Assessment Scenarios](#common-assessment-scenarios)
10. [Study Resources](#study-resources)
11. [Study Plan](#study-plan)

---

## Overview

### What is CMMC?
The **Cybersecurity Maturity Model Certification (CMMC)** is a DoD framework that verifies defense contractors have adequate cybersecurity practices to protect Controlled Unclassified Information (CUI).

### What is a CCA?
A **Certified CMMC Assessor (CCA)** is a mid-to-advanced level professional authorized to:
- Conduct **Level 2 CMMC assessments** for defense contractors
- Work as part of a **Certified Third-Party Assessment Organization (C3PAO)** team
- Make final compliance determinations
- Assess organizations handling CUI under DoD contracts

---

## Prerequisites

### Required Before Taking CCA Exam:

1. **CCP Certification** (CMMC Certified Professional)
   - Must complete CCP first - it's the foundation level

2. **DoD 8140.03 Work Role 612 Qualification**
   - Security Control Assessor role
   - Intermediate or Advanced proficiency level
   - **OR** hold certifications like:
     - CISA (Certified Information Systems Auditor)
     - CISM (Certified Information Security Manager)
     - Other qualifying security certifications

3. **Tier 3 Security Clearance**
   - Department of Defense Tier 3 Determination required
   - Background investigation completed

4. **Experience & Training**
   - Practical experience with security assessments
   - Understanding of cybersecurity frameworks

---

## Exam Structure

### Format:
- **Total Questions:** Approximately 150-200 questions (varies)
- **Question Types:** Multiple choice, scenario-based
- **Delivery:** Online proctored or in-person testing center
- **Duration:** Typically 3-4 hours
- **Passing Score:** Set by ISACA (not publicly disclosed)

### Content Areas:
- CMMC Model requirements
- Assessment methodology (CAP)
- NIST SP 800-171 security controls
- Organizational scoping
- Documentation and evidence evaluation
- Reporting and compliance determination

---

## Key Knowledge Domains

### 1. CMMC Framework Structure
- **CMMC 2.0 Levels:**
  - **Level 1:** Basic Cyber Hygiene (self-assessment)
  - **Level 2:** Advanced Cyber Hygiene (third-party assessment) ← **CCA Focus**
  - **Level 3:** Expert/Advanced (government assessment)

### 2. Assessment Types
- **Self-Assessment:** Level 1 only
- **C3PAO Assessment:** Level 2 (where CCAs operate)
- **Government-Led Assessment:** Level 3 and select Level 2

### 3. Key Concepts
- **CUI (Controlled Unclassified Information):** Sensitive government data requiring protection
- **OSC (Organizational Seeking Certification):** The contractor being assessed
- **OSA (Organization's System Administrator):** Technical point of contact
- **Assessment Scope:** Boundaries of what's being assessed
- **SSP (System Security Plan):** Documentation of security controls
- **POA&M (Plan of Action & Milestones):** Remediation plan for deficiencies

---

## NIST SP 800-171 Control Families

CMMC Level 2 is based on **NIST SP 800-171 Rev. 3**. You must understand all **17 control families:**

### 1. **Access Control (AC)**
- Limit system access to authorized users
- Control CUI flow
- Implement least privilege
- **Key Controls:** AC-1 through AC-22
- **Examples:**
  - AC-2: Account Management
  - AC-3: Access Enforcement
  - AC-7: Unsuccessful Login Attempts
  - AC-17: Remote Access

### 2. **Awareness and Training (AT)**
- Security awareness programs
- Role-based training
- **Key Controls:** AT-1 through AT-4
- **Examples:**
  - AT-2: Security Awareness Training
  - AT-3: Role-Based Security Training

### 3. **Audit and Accountability (AU)**
- Create, protect, and retain audit logs
- Monitor and review logs
- Alert on suspicious activity
- **Key Controls:** AU-1 through AU-13
- **Examples:**
  - AU-2: Auditable Events
  - AU-3: Content of Audit Records
  - AU-6: Audit Review, Analysis, and Reporting
  - AU-12: Audit Generation

### 4. **Configuration Management (CM)**
- Baseline configurations
- Change control
- Security configuration settings
- **Key Controls:** CM-1 through CM-11
- **Examples:**
  - CM-2: Baseline Configuration
  - CM-3: Configuration Change Control
  - CM-7: Least Functionality
  - CM-8: Information System Component Inventory

### 5. **Identification and Authentication (IA)**
- Identify users, processes, devices
- Authenticate before access
- Multi-factor authentication for privileged accounts
- **Key Controls:** IA-1 through IA-11
- **Examples:**
  - IA-2: Identification and Authentication
  - IA-3: Device Identification and Authentication
  - IA-5: Authenticator Management
  - IA-8: Identification and Authentication (Non-Organizational Users)

### 6. **Incident Response (IR)**
- Incident handling capability
- Reporting procedures
- Testing IR plans
- **Key Controls:** IR-1 through IR-9
- **Examples:**
  - IR-2: Incident Response Training
  - IR-4: Incident Handling
  - IR-5: Incident Monitoring
  - IR-6: Incident Reporting

### 7. **Maintenance (MA)**
- Perform and control maintenance
- Control maintenance tools
- **Key Controls:** MA-1 through MA-6
- **Examples:**
  - MA-2: Controlled Maintenance
  - MA-4: Nonlocal Maintenance
  - MA-5: Maintenance Personnel

### 8. **Media Protection (MP)**
- Protect and sanitize media
- Control physical and digital media
- **Key Controls:** MP-1 through MP-8
- **Examples:**
  - MP-2: Media Access
  - MP-3: Media Marking
  - MP-4: Media Storage
  - MP-6: Media Sanitization

### 9. **Personnel Security (PS)**
- Screen personnel
- Protect during/after employment
- **Key Controls:** PS-1 through PS-8
- **Examples:**
  - PS-3: Personnel Screening
  - PS-4: Personnel Termination
  - PS-6: Access Agreements

### 10. **Physical Protection (PE)**
- Physical access controls
- Monitor and escort visitors
- Protect against physical threats
- **Key Controls:** PE-1 through PE-17
- **Examples:**
  - PE-2: Physical Access Authorizations
  - PE-3: Physical Access Control
  - PE-6: Monitoring Physical Access
  - PE-8: Visitor Access Records

### 11. **Risk Assessment (RA)**
- Conduct vulnerability scans
- Perform risk assessments
- Remediate vulnerabilities
- **Key Controls:** RA-1 through RA-7
- **Examples:**
  - RA-3: Risk Assessment
  - RA-5: Vulnerability Scanning
  - RA-7: Risk Response

### 12. **Security Assessment (CA)**
- Assess security controls
- Remediate deficiencies
- Continuous monitoring
- **Key Controls:** CA-1 through CA-9
- **Examples:**
  - CA-2: Security Assessments
  - CA-3: System Interconnections
  - CA-7: Continuous Monitoring
  - CA-9: Internal System Connections

### 13. **System and Communications Protection (SC)**
- Boundary protection
- Encryption of CUI
- Network segmentation
- **Key Controls:** SC-1 through SC-28
- **Examples:**
  - SC-7: Boundary Protection
  - SC-8: Transmission Confidentiality and Integrity
  - SC-13: Cryptographic Protection
  - SC-28: Protection of Information at Rest

### 14. **System and Information Integrity (SI)**
- Flaw remediation
- Malware protection
- Information input validation
- **Key Controls:** SI-1 through SI-16
- **Examples:**
  - SI-2: Flaw Remediation
  - SI-3: Malicious Code Protection
  - SI-4: Information System Monitoring
  - SI-12: Information Handling and Retention

### 15. **Supply Chain Risk Management (SR)**
- Assess supply chain risks
- Manage external service providers
- **Key Controls:** SR-1 through SR-12
- **Examples:**
  - SR-2: Supply Chain Risk Management Plan
  - SR-3: Supply Chain Controls and Processes
  - SR-11: Component Authenticity

### 16. **Planning (PL)**
- System security plans
- Rules of behavior
- **Key Controls:** PL-1 through PL-10
- **Examples:**
  - PL-2: System Security Plan
  - PL-4: Rules of Behavior
  - PL-10: Baseline Selection

### 17. **Program Management (PM)**
- Security program planning
- Critical infrastructure plan
- **Key Controls:** PM-1 through PM-31
- **Examples:**
  - PM-9: Risk Management Strategy
  - PM-10: Security Authorization Process
  - PM-15: Contacts with Security Groups

---

## CMMC Assessment Process (CAP)

### Phase 1: Plan and Prepare
1. **Initial Engagement**
   - C3PAO and OSC establish agreement
   - Define assessment scope
   - Identify CUI assets and boundaries

2. **Documentation Review**
   - System Security Plan (SSP)
   - Network diagrams
   - Policies and procedures
   - Asset inventory
   - Data flow diagrams

3. **Pre-Assessment Coordination**
   - Schedule assessment activities
   - Identify personnel to interview
   - Request evidence artifacts

### Phase 2: Conduct Assessment
1. **Opening Meeting**
   - Introduce team
   - Confirm scope
   - Review schedule

2. **Evidence Collection**
   - Document review
   - System demonstrations
   - Configuration reviews
   - Personnel interviews
   - Technical testing

3. **Objective Evidence Analysis**
   - Evaluate controls
   - Document findings
   - Identify gaps
   - Verify implementation

### Phase 3: Report Results
1. **Draft Findings**
   - Document control assessment results
   - Identify compliant vs. non-compliant controls
   - Provide evidence references

2. **Closing Meeting**
   - Present preliminary findings
   - Address questions
   - Discuss next steps

3. **Final Report**
   - Complete assessment report
   - Submit to Cyber AB/DoD
   - Issue certification (if passed)
   - Provide POA&M for deficiencies

### Phase 4: Maintain Certification
- Certifications valid for **3 years**
- Continuous monitoring required
- Re-assessment after 3 years or major changes

---

## Assessment Roles & Responsibilities

### CCA (Certified CMMC Assessor)
- Lead assessor or team member
- Conduct Level 2 assessments
- Evaluate evidence
- Make compliance determinations
- Document findings

### LCCA (Lead Certified CMMC Assessor)
- Senior role above CCA
- Team leadership
- Final report approval
- Quality oversight

### C3PAO (Certified Third-Party Assessment Organization)
- Organization employing CCAs
- ISO 17020 accredited
- Conducts CMMC assessments
- Reports to Cyber AB

### CQAP (Certified Quality Assurance Professional)
- Quality assurance oversight
- Reviews assessment processes
- Ensures consistency
- Independent from assessment team

### OSC (Organization Seeking Certification)
- Defense contractor being assessed
- Provides evidence
- Implements controls
- Maintains compliance

---

## Organizational Scoping

### What Gets Assessed?
**Assessment Scope** includes:
- **CUI Environment:** All systems processing, storing, or transmitting CUI
- **Security Protection Assets:** Systems providing security to CUI environment
- **Contractor Risk Managed Assets (CRMA):** External services (cloud, MSPs)

### Scoping Considerations:
1. **Physical Boundaries**
   - Geographic locations
   - Facilities
   - Data centers

2. **Logical Boundaries**
   - Networks
   - Enclaves
   - Cloud environments

3. **Organizational Boundaries**
   - Subsidiaries (may need separate assessments)
   - Business units
   - Divisions

### Scoping Exclusions:
- Systems that never touch CUI
- Physically/logically separated environments
- Non-relevant business operations

### Key Scoping Questions:
- Where is CUI stored?
- How does CUI flow through systems?
- What systems provide security services?
- Are there third-party service providers?
- What network segments contain CUI?

---

## Common Assessment Scenarios

### Scenario 1: Cloud Infrastructure
**Question:** Organization uses AWS for CUI storage. What needs assessment?
**Answer:**
- The cloud configuration (IaaS controls)
- Access controls to cloud resources
- Encryption implementation
- Verify FedRAMP equivalency for CSP
- Organization's responsibility matrix

### Scenario 2: Remote Access
**Question:** Employees access CUI remotely via SSH/VPN. Security concerns?
**Answer:**
- Multi-factor authentication required
- Encrypted connections (FIPS 140-2)
- Session logging and monitoring
- Access control policies
- Device security requirements

### Scenario 3: Subsidiary Organizations
**Question:** Parent company has multiple subsidiaries. One assessment or multiple?
**Answer:**
- Depends on operational independence
- Separate IT systems = separate assessments
- Shared infrastructure may allow combined scope
- Each legal entity may need individual certification

### Scenario 4: Pre-Assessment Documentation
**Question:** What documents must OSC provide before assessment?
**Answer:**
- System Security Plan (SSP)
- Network diagrams
- Asset inventory
- Policies and procedures
- Data flow diagrams
- Previous assessment results (if any)
- POA&M (if addressing prior deficiencies)

### Scenario 5: File-Sharing with CUI
**Question:** Secure file-sharing app handles CUI. Asset classification?
**Answer:**
- **CUI Asset** (directly processes CUI)
- Requires full control assessment
- Encryption at rest and in transit
- Access controls and audit logging
- Part of assessment scope

---

## Study Resources

### Official Documentation (FREE)
1. **NIST SP 800-171 Rev. 3** (MUST READ)
   - https://csrc.nist.gov/pubs/sp/800/171/r3/final
   - PDF download available
   - All 17 control families

2. **NIST SP 800-171A Rev. 3** (Assessment Procedures)
   - https://csrc.nist.gov/pubs/sp/800/171/r3/final
   - Assessment methods for each control
   - Evidence requirements

3. **Cyber AB Resources**
   - Downloads: https://cyberab.org/Resources/Downloads
   - CMMC Assessment Process (CAP) document
   - Code of Professional Conduct
   - C3PAO requirements documents
   - How-to Videos: https://cyberab.org/Resources/How-to-Videos
   - Forums: https://cyberab.org/Resources/Forums

4. **ISACA CMMC Page**
   - https://www.isaca.org/cmmc
   - Official exam authority
   - Registration information

5. **CMMC Model Documentation**
   - CMMC 2.0 Model overview
   - Practice and capability descriptions

### Additional Free Resources
- **DoD CMMC Program Final Rule** (govinfo.gov)
- **FedRAMP resources** for cloud security understanding
- **ISO 17020 basics** for understanding C3PAO accreditation
- **DFARS clauses** related to CMMC

### Study Communities
- Cyber AB Forums (peer discussion)
- LinkedIn CMMC groups
- Reddit r/CMMC community
- Professional security associations

---

## Study Plan

### Phase 1: Foundation (Weeks 1-2)
- [ ] Read CMMC 2.0 Model overview
- [ ] Review CCA role and responsibilities
- [ ] Understand assessment levels and types
- [ ] Study CMMC ecosystem roles
- [ ] Watch Cyber AB how-to videos

### Phase 2: Deep Dive - Controls (Weeks 3-6)
- [ ] Read NIST SP 800-171 Rev. 3 completely
- [ ] Study each of 17 control families in detail
- [ ] Create flashcards for each control
- [ ] Understand control objectives and requirements
- [ ] Review NIST SP 800-171A assessment procedures

### Phase 3: Assessment Process (Weeks 7-8)
- [ ] Study CMMC Assessment Process (CAP) document
- [ ] Understand all assessment phases
- [ ] Learn evidence collection methods
- [ ] Review documentation requirements
- [ ] Practice scoping scenarios

### Phase 4: Professional Standards (Week 9)
- [ ] Read Code of Professional Conduct
- [ ] Understand C3PAO requirements
- [ ] Review quality assurance processes
- [ ] Study ethical considerations
- [ ] Learn reporting requirements

### Phase 5: Practice & Review (Weeks 10-12)
- [ ] Create scenario-based questions
- [ ] Practice scoping exercises
- [ ] Review all control families again
- [ ] Take practice exams (if available)
- [ ] Join study groups
- [ ] Participate in forums
- [ ] Review weak areas

### Phase 6: Final Preparation (Week 13)
- [ ] Complete comprehensive review
- [ ] Focus on frequently tested topics
- [ ] Review assessment methodology
- [ ] Mental preparation
- [ ] Schedule exam

---

## Key Success Tips

### 1. Master the Controls
- Know all 17 families cold
- Understand implementation examples
- Recognize control relationships

### 2. Think Like an Assessor
- How would you verify this control?
- What evidence is needed?
- What questions would you ask?

### 3. Understand Scoping
- Practice determining assessment boundaries
- Learn to identify CUI flows
- Recognize scope inclusions/exclusions

### 4. Know the Process
- Assessment phases must be followed
- Documentation requirements are critical
- Quality assurance is essential

### 5. Professional Ethics
- Code of Professional Conduct is tested
- Objectivity and independence matter
- Reporting accuracy is paramount

### 6. Practical Application
- Think about real-world scenarios
- Consider common implementation challenges
- Understand industry best practices

---

## Quick Reference: Key Terms

| Term | Definition |
|------|------------|
| **CMMC** | Cybersecurity Maturity Model Certification |
| **CUI** | Controlled Unclassified Information |
| **CCA** | Certified CMMC Assessor (Level 2 assessor) |
| **LCCA** | Lead Certified CMMC Assessor |
| **C3PAO** | Certified Third-Party Assessment Organization |
| **OSC** | Organization Seeking Certification |
| **CAP** | CMMC Assessment Process |
| **SSP** | System Security Plan |
| **POA&M** | Plan of Action & Milestones |
| **SPRS** | Supplier Performance Risk System |
| **CRMA** | Contractor Risk Managed Assets |
| **FCI** | Federal Contract Information |
| **DFARS** | Defense Federal Acquisition Regulation Supplement |
| **NIST** | National Institute of Standards and Technology |
| **Cyber AB** | CMMC Accreditation Body |

---

## Assessment Score Calculation

### Scoring Method:
- Each practice/control is assessed: **Met, Not Met, or Not Applicable**
- **Level 2 Requirement:** ALL applicable practices must be "Met"
- **No partial credit:** One failure = level not achieved
- **Documentation required:** Evidence must support all "Met" determinations

### Common Failure Points:
- Incomplete documentation
- Inconsistent implementation
- Missing evidence
- Inadequate policies/procedures
- Configuration weaknesses
- Insufficient monitoring/logging
- Poor access controls
- Lack of formal processes

---

## Final Exam Day Tips

1. **Get good rest** the night before
2. **Arrive early** or log in early for online proctoring
3. **Read each question carefully** - scenario-based questions have details
4. **Eliminate wrong answers** first
5. **Trust your preparation** - don't second-guess too much
6. **Manage your time** - don't spend too long on any one question
7. **Flag questions** for review if unsure
8. **Review flagged questions** before submitting

---

## Next Steps After This Guide

1. **Download NIST SP 800-171 Rev. 3** and start reading
2. **Access Cyber AB downloads** for official documents
3. **Watch Cyber AB videos** for visual learning
4. **Join study forums** for peer support
5. **Create a study schedule** based on the plan above
6. **Track your progress** through each control family
7. **Schedule your exam** when confident in your preparation

---

## Additional Notes

- **Keep up with changes:** CMMC is evolving - stay current with updates
- **Practical experience matters:** Try to get hands-on assessment experience
- **Network with other CCAs:** Learn from those who've passed
- **Don't rush:** Give yourself adequate time to study thoroughly
- **Focus on understanding, not memorization:** Scenarios require application

---

## Resources Checklist

Download/Access these before starting:
- [ ] NIST SP 800-171 Rev. 3 (PDF)
- [ ] NIST SP 800-171A Rev. 3 (PDF)
- [ ] CMMC Assessment Process (CAP) document
- [ ] Code of Professional Conduct
- [ ] C3PAO Authorization Requirements (R2001)
- [ ] CMMC 2.0 Model documentation
- [ ] Cyber AB How-to Videos (bookmark)
- [ ] Join Cyber AB Forums

---

**Good luck with your studies!**

This guide is based on publicly available information as of April 2026. Always refer to official ISACA and Cyber AB sources for the most current exam requirements and content.

---

*For questions or clarifications, consult:*
- ISACA CMMC Support: www.isaca.org/cmmc
- Cyber AB: www.cyberab.org
- NIST: csrc.nist.gov
