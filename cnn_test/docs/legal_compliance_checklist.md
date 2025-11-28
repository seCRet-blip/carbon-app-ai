# Legal Implications & Compliance Checklist
## Carbon Credit Eligibility AI System

**Document Version:** 1.0  
**Date:** November 28, 2025  
**Jurisdiction:** New Zealand (Applicable Internationally)  
**Review Frequency:** Quarterly or upon regulatory change

---

## Purpose

This checklist provides a comprehensive overview of legal and compliance considerations for deploying the Carbon Credit Eligibility AI system. It should be reviewed with legal counsel before deployment and updated regularly to reflect changing regulations.

>  **DISCLAIMER:** This document is for informational purposes only and does not constitute legal advice. Consult with qualified legal counsel for specific legal guidance.

---

## 1. Data Protection & Privacy Compliance

### 1.1 New Zealand Privacy Act 2020

| Requirement | Status | Evidence/Notes | Action Required |
|-------------|--------|----------------|-----------------|
| **Privacy Principles Compliance** | | | |
| └─ Principle 1: Purpose of collection | ☐ | Specify purpose in privacy notice | Draft privacy notice |
| └─ Principle 2: Source of personal information | ☐ | Document data sources | Complete data inventory |
| └─ Principle 3: Collection of information | ☐ | Only collect necessary data | Review data collection |
| └─ Principle 4: Manner of collection | ☐ | Lawful and fair collection | Validate collection methods |
| └─ Principle 5: Storage and security | ☐ | Implement security measures | Security audit required |
| └─ Principle 6: Access to information | ☐ | Process for access requests | Create request procedure |
| └─ Principle 7: Correction of information | ☐ | Process for corrections | Create correction procedure |
| └─ Principle 8: Accuracy | ☐ | Data accuracy checks | Implement validation |
| └─ Principle 9: Retention | ☐ | Define retention periods | Create retention policy |
| └─ Principle 10: Use/disclosure limits | ☐ | Limit use to stated purpose | Document usage boundaries |
| └─ Principle 11: Disclosure | ☐ | Rules for third-party sharing | Draft sharing agreements |
| └─ Principle 12: Unique identifiers | ☐ | Appropriate use of identifiers | Review identifier usage |
| └─ Principle 13: Use for marketing | ☐ | Opt-in for marketing use | Implement consent system |
| **Privacy Officer** | ☐ | Designate responsible person | Appoint privacy officer |
| **Privacy Impact Assessment** | ☐ | Complete PIA for AI system | Schedule PIA |
| **Data Breach Notification** | ☐ | 72-hour notification process | Create breach procedure |
| **Cross-border Data Transfer** | ☐ | Adequate protection for transfers | Review transfer mechanisms |

**Priority Actions:**
1. [ ] Appoint Privacy Officer
2. [ ] Conduct Privacy Impact Assessment
3. [ ] Draft comprehensive privacy notice
4. [ ] Implement data subject rights processes
5. [ ] Create data breach response plan

---

### 1.2 GDPR Compliance (If Operating in EU/UK)

| Requirement | Status | Evidence/Notes | Action Required |
|-------------|--------|----------------|-----------------|
| **Legal Basis for Processing** | ☐ | Legitimate interest/consent/contract | Document legal basis |
| **Data Subject Rights** | | | |
| └─ Right to access | ☐ | 30-day response SLA | Implement request system |
| └─ Right to rectification | ☐ | Correction process | Create correction workflow |
| └─ Right to erasure | ☐ | Deletion capability | Implement deletion |
| └─ Right to data portability | ☐ | Export in machine-readable format | Build export function |
| └─ Right to object | ☐ | Opt-out mechanisms | Create opt-out process |
| └─ Right to restrict processing | ☐ | Processing controls | Implement restrictions |
| **Automated Decision Making (Art. 22)** | ☐ | Human review for significant decisions | Implement HITL |
| **DPIA (Data Protection Impact Assessment)** | ☐ | Required for high-risk processing | Complete DPIA |
| **Data Processing Agreement (DPA)** | ☐ | For third-party processors | Draft DPA template |
| **EU Representative** | ☐ | If no EU establishment | Appoint representative |
| **Records of Processing Activities** | ☐ | Maintain processing records | Create record system |

**Priority Actions:**
1. [ ] Confirm legal basis for processing
2. [ ] Complete GDPR-compliant DPIA
3. [ ] Implement all data subject rights
4. [ ] Ensure human review for automated decisions
5. [ ] Appoint EU representative (if needed)

---

## 2. AI & Algorithmic Accountability

### 2.1 Algorithmic Transparency

| Requirement | Status | Evidence/Notes | Action Required |
|-------------|--------|----------------|-----------------|
| **Disclosure of AI Use** | ☐ | Inform users AI is being used | Add disclosure notices |
| **Explainability** | ☐ | Ability to explain decisions | Implement explainability tools |
| **Model Documentation** | ☐ | Model cards/datasheets | Create model documentation |
| **Decision Rationale** | ☐ | Provide reasoning for predictions | Add explanation features |
| **Human Review Option** | ☐ | Allow human override of AI | Implement override capability |
| **Appeal Process** | ☐ | Contest AI decisions | Create appeals procedure |

**Priority Actions:**
1. [ ] Create clear AI disclosure notices
2. [ ] Develop explanation capabilities
3. [ ] Document model architecture and limitations
4. [ ] Implement human override system
5. [ ] Establish appeals process

---

### 2.2 AI Ethics & Fairness

| Requirement | Status | Evidence/Notes | Action Required |
|-------------|--------|----------------|-----------------|
| **Bias Assessment** | ☐ | Test for discriminatory bias | Conduct bias audit |
| **Fairness Metrics** | ☐ | Equal performance across groups | Measure fairness |
| **Non-Discrimination** | ☐ | No protected class discrimination | Legal review |
| **Ethical Review Board** | ☐ | Independent ethics review | Establish ethics committee |
| **Stakeholder Consultation** | ☐ | Input from affected parties | Conduct consultations |
| **Harmful Use Prevention** | ☐ | Terms of use prohibiting misuse | Draft acceptable use policy |

**Priority Actions:**
1. [ ] Conduct comprehensive bias audit
2. [ ] Establish AI ethics committee
3. [ ] Engage stakeholders for feedback
4. [ ] Create fairness monitoring dashboard
5. [ ] Draft ethical AI use policy

---

### 2.3 Emerging AI Regulations

| Regulation | Status | Applicability | Action Required |
|------------|--------|---------------|-----------------|
| **EU AI Act** | ☐ | If operating in EU | Classify risk level, prepare compliance |
| **NZ Algorithmic Charter** | ☐ | Voluntary commitment | Consider signing charter |
| **ISO/IEC 42001 (AI Management)** | ☐ | International standard | Consider certification |
| **IEEE Standards for AI** | ☐ | Industry best practices | Review relevant standards |

**Priority Actions:**
1. [ ] Monitor EU AI Act development and classify system
2. [ ] Review NZ Algorithmic Charter for voluntary compliance
3. [ ] Assess value of ISO/IEC 42001 certification

---

## 3. Carbon Credit Regulatory Compliance

### 3.1 New Zealand Emissions Trading Scheme (NZ ETS)

| Requirement | Status | Evidence/Notes | Action Required |
|-------------|--------|----------------|-----------------|
| **ETS Registration** | ☐ | Registration as participant/advisor | Complete registration |
| **Forestry Right Requirements** | ☐ | Valid forestry rights for land | Verify requirements |
| **Approved Land Types** | ☐ | Eligible under ETS rules | Document eligible types |
| **NZU (Carbon Unit) Issuance** | ☐ | Compliance with issuance rules | Review issuance process |
| **Verification Requirements** | ☐ | Third-party verification needed | Identify verifiers |
| **Reporting Obligations** | ☐ | Annual reporting to EPA | Create reporting process |
| **Record Keeping** | ☐ | 7-year retention requirement | Implement retention system |
| **Permanence Requirements** | ☐ | 100-year commitment for forests | Verify compliance |

**Priority Actions:**
1. [ ] Register with NZ ETS (if required)
2. [ ] Document alignment with ETS eligibility criteria
3. [ ] Establish relationship with accredited verifiers
4. [ ] Implement 7-year record retention system
5. [ ] Create annual reporting templates

---

### 3.2 International Carbon Standards

| Standard | Status | Applicability | Action Required |
|----------|--------|---------------|-----------------|
| **Verified Carbon Standard (VCS)** | ☐ | If seeking international credits | Review VCS requirements |
| **Gold Standard** | ☐ | Premium carbon credits | Assess alignment |
| **Climate Action Reserve** | ☐ | North American markets | Review if expanding |
| **ISO 14064 (GHG Accounting)** | ☐ | International GHG standard | Consider certification |
| **ISO 14065 (Verification Bodies)** | ☐ | Verification standards | Ensure verifier compliance |

**Priority Actions:**
1. [ ] Identify target carbon credit markets
2. [ ] Review applicable international standards
3. [ ] Assess certification requirements
4. [ ] Plan for multi-standard compliance if needed

---

## 4. Intellectual Property

### 4.1 Model & Software IP

| Requirement | Status | Evidence/Notes | Action Required |
|-------------|--------|----------------|-----------------|
| **Model Ownership** | ☐ | Clear IP ownership documented | Draft IP assignment agreements |
| **Training Data Licenses** | ☐ | Rights to use training data | Audit data licenses |
| **Open Source Compliance** | ☐ | License compliance (PyTorch, etc.) | Review all dependencies |
| **Patents** | ☐ | Consider patent protection | Consult patent attorney |
| **Trade Secrets** | ☐ | Protect proprietary algorithms | Implement confidentiality measures |
| **Copyright** | ☐ | Software copyright registration | Register copyrights |

**Priority Actions:**
1. [ ] Document complete IP ownership chain
2. [ ] Audit all training data for licensing
3. [ ] Review open-source license compliance
4. [ ] Consult IP attorney for protection strategy
5. [ ] Implement trade secret protections

---

### 4.2 Client IP & Usage Rights

| Requirement | Status | Evidence/Notes | Action Required |
|-------------|--------|----------------|-----------------|
| **Client Data Ownership** | ☐ | Clarify data ownership | Add to terms of service |
| **License Grants** | ☐ | Define usage rights | Draft license terms |
| **Derivative Works** | ☐ | Rights to AI-generated outputs | Clarify in agreements |
| **Confidentiality** | ☐ | Protect client proprietary data | NDA templates |

**Priority Actions:**
1. [ ] Clarify data ownership in client agreements
2. [ ] Define clear license terms for AI outputs
3. [ ] Implement robust confidentiality measures

---

## 5. Liability & Insurance

### 5.1 Liability Framework

| Requirement | Status | Evidence/Notes | Action Required |
|-------------|--------|----------------|-----------------|
| **Terms of Service** | ☐ | Comprehensive ToS drafted | Legal review of ToS |
| **Liability Limitations** | ☐ | Reasonable limitations included | Ensure enforceability |
| **Indemnification Clauses** | ☐ | Mutual indemnification | Balance obligations |
| **Warranty Disclaimers** | ☐ | Appropriate disclaimers | Draft disclaimers |
| **Force Majeure** | ☐ | Unforeseeable event clause | Include in contracts |
| **Dispute Resolution** | ☐ | Arbitration/mediation clauses | Select mechanisms |
| **Governing Law** | ☐ | Specify applicable jurisdiction | Choose jurisdiction |

**Priority Actions:**
1. [ ] Draft comprehensive Terms of Service
2. [ ] Legal review of all liability clauses
3. [ ] Ensure enforceability in target jurisdictions
4. [ ] Include clear warranty disclaimers

---

### 5.2 Insurance Coverage

| Coverage Type | Status | Coverage Amount | Action Required |
|---------------|--------|-----------------|-----------------|
| **Professional Indemnity** | ☐ | $[X] million | Obtain quotes |
| **Cyber Liability** | ☐ | $[X] million | Obtain quotes |
| **Errors & Omissions (E&O)** | ☐ | $[X] million | Obtain quotes |
| **Directors & Officers (D&O)** | ☐ | $[X] million | Obtain quotes |
| **General Liability** | ☐ | $[X] million | Obtain quotes |
| **Data Breach Insurance** | ☐ | $[X] million | Obtain quotes |

**Priority Actions:**
1. [ ] Conduct risk assessment for insurance needs
2. [ ] Obtain quotes from multiple insurers
3. [ ] Review policy exclusions carefully
4. [ ] Ensure AI-specific coverage included
5. [ ] Establish claims procedures

---

## 6. Contractual Obligations

### 6.1 Client Agreements

| Component | Status | Notes | Action Required |
|-----------|--------|-------|-----------------|
| **Service Level Agreements (SLAs)** | ☐ | Define performance guarantees | Draft SLAs |
| **Scope of Services** | ☐ | Clear service definition | Document scope |
| **Fees & Payment Terms** | ☐ | Transparent pricing | Create pricing structure |
| **Termination Clauses** | ☐ | Exit procedures defined | Draft termination terms |
| **Data Handling Terms** | ☐ | Data use and retention | Include data clauses |
| **Confidentiality** | ☐ | NDA provisions | Draft confidentiality terms |
| **Acceptance Criteria** | ☐ | Define success metrics | Establish criteria |

**Priority Actions:**
1. [ ] Create standard client agreement template
2. [ ] Define clear SLAs with measurable metrics
3. [ ] Legal review of all contract terms
4. [ ] Ensure data handling terms align with privacy laws

---

### 6.2 Third-Party Agreements

| Agreement Type | Status | Parties | Action Required |
|----------------|--------|---------|-----------------|
| **Cloud Service Agreement** | ☐ | Azure/AWS/GCP | Review terms |
| **Data Processing Agreements** | ☐ | Data processors | Execute DPAs |
| **API License Agreements** | ☐ | Third-party APIs | Review licenses |
| **Subcontractor Agreements** | ☐ | Service providers | Draft agreements |
| **Data Sharing Agreements** | ☐ | Data partners | Establish terms |
| **Verification Partner Agreements** | ☐ | Carbon verifiers | Negotiate terms |

**Priority Actions:**
1. [ ] Inventory all third-party dependencies
2. [ ] Review and negotiate cloud service terms
3. [ ] Execute Data Processing Agreements
4. [ ] Ensure all agreements protect IP and data

---

## 7. Employment & Contractor Law

### 7.1 Staff Obligations

| Requirement | Status | Evidence/Notes | Action Required |
|-------------|--------|----------------|-----------------|
| **Employment Contracts** | ☐ | Comprehensive contracts | Legal review |
| **IP Assignment Clauses** | ☐ | Work product ownership | Include in contracts |
| **Confidentiality Agreements** | ☐ | Protect trade secrets | Execute NDAs |
| **Non-Compete Clauses** | ☐ | Reasonable restrictions | Ensure enforceability |
| **Code of Conduct** | ☐ | Ethical standards | Draft and distribute |
| **Training Requirements** | ☐ | Compliance training | Implement training program |

**Priority Actions:**
1. [ ] Review/update all employment contracts
2. [ ] Ensure IP assignment clauses in place
3. [ ] Implement mandatory compliance training
4. [ ] Distribute and acknowledge code of conduct

---

## 8. Security & Cybersecurity Compliance

### 8.1 Information Security Standards

| Standard | Status | Applicability | Action Required |
|----------|--------|---------------|-----------------|
| **ISO 27001** | ☐ | Information security management | Consider certification |
| **SOC 2 Type II** | ☐ | Service org controls | Plan for audit |
| **NIST Cybersecurity Framework** | ☐ | Cybersecurity best practices | Assess alignment |
| **Essential 8 (NZ CERT)** | ☐ | NZ cyber security baseline | Implement controls |
| **PCI DSS** | ☐ | If handling payment data | Assess applicability |

**Priority Actions:**
1. [ ] Implement Essential 8 security controls
2. [ ] Conduct gap analysis for ISO 27001
3. [ ] Plan for SOC 2 audit (if required by clients)
4. [ ] Align with NIST Cybersecurity Framework

---

### 8.2 Incident Response

| Requirement | Status | Evidence/Notes | Action Required |
|-------------|--------|----------------|-----------------|
| **Incident Response Plan** | ☐ | Documented procedures | Create IRP |
| **Breach Notification Process** | ☐ | 72-hour timeline | Establish process |
| **CERT NZ Relationship** | ☐ | Reporting channel established | Register with CERT |
| **Cyber Insurance Claims** | ☐ | Claims procedures documented | Create procedure |
| **Forensic Capabilities** | ☐ | Evidence preservation | Establish procedures |

**Priority Actions:**
1. [ ] Develop comprehensive incident response plan
2. [ ] Test breach notification procedures
3. [ ] Establish reporting relationship with CERT NZ
4. [ ] Train team on incident response

---

## 9. Consumer Protection & Advertising

### 9.1 Fair Trading Compliance

| Requirement | Status | Evidence/Notes | Action Required |
|-------------|--------|----------------|-----------------|
| **Fair Trading Act 1986 (NZ)** | ☐ | No misleading representations | Review marketing |
| **Accuracy in Advertising** | ☐ | Truthful performance claims | Substantiate claims |
| **Consumer Guarantees** | ☐ | Service quality guarantees | Define guarantees |
| **Unfair Contract Terms** | ☐ | Avoid unconscionable terms | Legal review |
| **Cooling-Off Periods** | ☐ | If applicable | Determine applicability |

**Priority Actions:**
1. [ ] Review all marketing materials for accuracy
2. [ ] Ensure performance claims are substantiated
3. [ ] Legal review of consumer-facing terms
4. [ ] Implement consumer protection measures

---

## 10. Financial & Tax Compliance

### 10.1 Financial Regulations

| Requirement | Status | Evidence/Notes | Action Required |
|-------------|--------|----------------|-----------------|
| **GST Registration** | ☐ | If revenue >$60k NZD | Register for GST |
| **Tax Compliance** | ☐ | Corporate tax obligations | Engage accountant |
| **Anti-Money Laundering (AML)** | ☐ | If applicable to services | Assess applicability |
| **Financial Reporting** | ☐ | Annual financial statements | Establish process |
| **Revenue Recognition** | ☐ | Appropriate accounting method | Consult accountant |

**Priority Actions:**
1. [ ] Register for GST (if required)
2. [ ] Engage qualified accountant/auditor
3. [ ] Assess AML obligations
4. [ ] Establish financial reporting processes

---

## 11. Industry-Specific Regulations

### 11.1 Environmental & Forestry Regulations

| Regulation | Status | Applicability | Action Required |
|------------|--------|---------------|-----------------|
| **Resource Management Act** | ☐ | Land use and development | Review requirements |
| **Forests Act 1949** | ☐ | Forestry activities | Assess applicability |
| **Climate Change Response Act** | ☐ | ETS and carbon credits | Ensure compliance |
| **Conservation Act** | ☐ | Protected land | Verify exclusions |
| **Native Plant & Animal Protection** | ☐ | Indigenous species | Review obligations |

**Priority Actions:**
1. [ ] Review all applicable environmental regulations
2. [ ] Ensure AI assessments align with legal definitions
3. [ ] Consult environmental law specialist
4. [ ] Document regulatory alignment

---

## 12. Audit & Compliance Monitoring

### 12.1 Compliance Program

| Component | Status | Frequency | Action Required |
|-----------|--------|-----------|-----------------|
| **Compliance Officer** | ☐ | Designated role | Appoint officer |
| **Compliance Training** | ☐ | Annual | Develop training program |
| **Internal Audits** | ☐ | Quarterly | Schedule audits |
| **External Audits** | ☐ | Annual | Engage auditors |
| **Regulatory Change Monitoring** | ☐ | Ongoing | Establish monitoring system |
| **Compliance Reporting** | ☐ | Quarterly to board | Create reporting template |

**Priority Actions:**
1. [ ] Appoint Chief Compliance Officer
2. [ ] Develop comprehensive compliance training
3. [ ] Schedule regular internal audits
4. [ ] Implement regulatory monitoring system
5. [ ] Create compliance dashboard for leadership

---

### 12.2 Documentation & Record Keeping

| Record Type | Retention Period | Storage Method | Action Required |
|-------------|------------------|----------------|-----------------|
| **Model Training Records** | 7 years | Secure cloud storage | Implement retention |
| **Prediction Audit Logs** | 7 years | Secure database | Implement logging |
| **Client Agreements** | 7 years post-termination | Secure document mgmt | Establish system |
| **Privacy Requests** | 2 years | Secure database | Implement tracking |
| **Incident Reports** | 10 years | Secure archive | Create archive |
| **Financial Records** | 7 years | Secure storage | Follow accounting standards |
| **Compliance Audits** | 5 years | Secure archive | Establish procedure |

**Priority Actions:**
1. [ ] Implement comprehensive audit logging
2. [ ] Establish secure document management system
3. [ ] Create retention schedule for all record types
4. [ ] Implement automated retention policies
5. [ ] Plan for secure disposal of expired records

---

## 13. International Expansion Considerations

### 13.1 Multi-Jurisdiction Compliance

| Jurisdiction | Status | Key Regulations | Action Required |
|--------------|--------|-----------------|-----------------|
| **Australia** | ☐ | Privacy Act, ACCC rules | Research requirements |
| **European Union** | ☐ | GDPR, EU AI Act | Assess feasibility |
| **United Kingdom** | ☐ | UK GDPR, ICO guidelines | Review requirements |
| **United States** | ☐ | State-specific laws (CCPA, etc.) | Complex compliance analysis |
| **Canada** | ☐ | PIPEDA, provincial laws | Review requirements |

**Priority Actions:**
1. [ ] Prioritize target international markets
2. [ ] Conduct jurisdiction-specific legal research
3. [ ] Engage local legal counsel in target markets
4. [ ] Assess data localization requirements
5. [ ] Plan phased international rollout

---

## 14. Governance & Corporate Structure

### 14.1 Corporate Governance

| Requirement | Status | Evidence/Notes | Action Required |
|-------------|--------|----------------|-----------------|
| **Board of Directors** | ☐ | Appropriate expertise | Establish board |
| **Advisory Board** | ☐ | Technical/legal advisors | Recruit advisors |
| **Corporate Policies** | ☐ | Comprehensive policies | Draft policies |
| **Conflicts of Interest** | ☐ | Disclosure procedures | Establish procedures |
| **Whistleblower Protection** | ☐ | Anonymous reporting | Implement system |
| **ESG Reporting** | ☐ | Environmental, social, governance | Plan reporting |

**Priority Actions:**
1. [ ] Establish board with appropriate expertise
2. [ ] Recruit advisory board (legal, technical, environmental)
3. [ ] Draft comprehensive corporate policies
4. [ ] Implement whistleblower protection system

---

## 15. Implementation Checklist Summary

### Critical Priority (Complete Before Launch)

- [ ] **Privacy:** Complete Privacy Impact Assessment
- [ ] **Privacy:** Appoint Privacy Officer
- [ ] **Privacy:** Draft privacy notices and consent forms
- [ ] **Privacy:** Implement data subject rights processes
- [ ] **AI Ethics:** Conduct bias audit
- [ ] **AI Transparency:** Implement explainability features
- [ ] **AI Transparency:** Add AI disclosure notices
- [ ] **Carbon Compliance:** Verify alignment with NZ ETS requirements
- [ ] **Carbon Compliance:** Establish verifier relationships
- [ ] **Contracts:** Draft and review Terms of Service
- [ ] **Contracts:** Create standard client agreement
- [ ] **Liability:** Obtain professional indemnity insurance
- [ ] **Liability:** Obtain cyber liability insurance
- [ ] **Security:** Implement Essential 8 controls
- [ ] **Security:** Create incident response plan
- [ ] **IP:** Document IP ownership chain
- [ ] **IP:** Review open-source license compliance
- [ ] **Employment:** Ensure IP assignment in employee contracts
- [ ] **Compliance:** Appoint Compliance Officer
- [ ] **Compliance:** Implement audit logging
- [ ] **Financial:** Register for GST (if applicable)

### High Priority (Complete Within 3 Months)

- [ ] **Privacy:** Establish 7-year data retention system
- [ ] **Privacy:** Execute Data Processing Agreements with vendors
- [ ] **AI Ethics:** Establish AI ethics committee
- [ ] **AI Accountability:** Implement appeal process for AI decisions
- [ ] **Carbon Compliance:** Create annual reporting templates
- [ ] **Contracts:** Review and execute cloud service agreements
- [ ] **Security:** Plan for SOC 2 audit
- [ ] **Security:** Register with CERT NZ
- [ ] **IP:** Consult IP attorney for protection strategy
- [ ] **Governance:** Establish advisory board
- [ ] **Compliance:** Develop compliance training program
- [ ] **Compliance:** Schedule first internal audit
- [ ] **Marketing:** Review all advertising for accuracy

### Medium Priority (Complete Within 6 Months)

- [ ] **Privacy:** Consider GDPR compliance (if expanding to EU)
- [ ] **AI Standards:** Review ISO/IEC 42001 for certification
- [ ] **Carbon Compliance:** Assess international carbon standards
- [ ] **Security:** Assess ISO 27001 certification value
- [ ] **IP:** Consider patent protection for novel algorithms
- [ ] **Governance:** Draft comprehensive corporate policies
- [ ] **International:** Research requirements for target markets
- [ ] **Compliance:** Establish regulatory monitoring system

---

## 16. Legal Counsel & Expert Contacts

| Specialty | Contact | Purpose | Status |
|-----------|---------|---------|--------|
| **Privacy & Data Protection Lawyer** | [Name, Firm] | Privacy compliance | ☐ Not yet engaged |
| **AI & Technology Lawyer** | [Name, Firm] | AI regulations, IP | ☐ Not yet engaged |
| **Environmental Lawyer** | [Name, Firm] | Carbon credit compliance | ☐ Not yet engaged |
| **Corporate/Commercial Lawyer** | [Name, Firm] | Contracts, corporate structure | ☐ Not yet engaged |
| **Employment Lawyer** | [Name, Firm] | Employment contracts | ☐ Not yet engaged |
| **Tax Accountant/Advisor** | [Name, Firm] | Tax compliance | ☐ Not yet engaged |
| **Certified Carbon Verifier** | [Name, Organization] | Third-party verification | ☐ Not yet engaged |
| **Information Security Auditor** | [Name, Firm] | Security audits | ☐ Not yet engaged |

**Priority Actions:**
1. [ ] Engage privacy & data protection specialist
2. [ ] Engage AI & technology lawyer
3. [ ] Engage environmental lawyer for carbon compliance
4. [ ] Establish relationship with certified carbon verifiers
5. [ ] Engage tax accountant

---

## 17. Regulatory Authority Contacts

| Authority | Purpose | Registration Status | Contact Info |
|-----------|---------|-------------------|--------------|
| **Environmental Protection Authority (EPA)** | NZ ETS registration & reporting | ☐ Not registered | www.epa.govt.nz |
| **Office of the Privacy Commissioner** | Privacy compliance | ☐ Not registered | www.privacy.org.nz |
| **CERT NZ** | Cybersecurity incidents | ☐ Not registered | www.cert.govt.nz |
| **Commerce Commission** | Fair trading compliance | ☐ No registration required | www.comcom.govt.nz |
| **Inland Revenue** | Tax obligations | ☐ Not registered | www.ird.govt.nz |
| **Companies Office** | Corporate registration | ☐ Status: [TBD] | www.companies.govt.nz |

---

## 18. Review & Sign-Off

### Document Review
- [ ] Reviewed by Legal Counsel: _________________ Date: _______
- [ ] Reviewed by Compliance Officer: _____________ Date: _______
- [ ] Reviewed by Privacy Officer: ________________ Date: _______
- [ ] Reviewed by Technical Lead: ________________ Date: _______

### Management Sign-Off
- [ ] CEO Approval: _____________________________ Date: _______
- [ ] CTO Approval: _____________________________ Date: _______
- [ ] CFO Approval: _____________________________ Date: _______

### Next Review Date: ________________

---

## 19. Version History

| Version | Date | Changes | Author |
|---------|------|---------|--------|
| 1.0 | 2025-11-28 | Initial document creation | [Name] |
|  |  |  |  |

---

## 20. Notes & Amendments

[Space for ongoing notes, amendments, and updates]

---

**END OF LEGAL COMPLIANCE CHECKLIST**

> This is a living document. Update regularly as regulations change and the business evolves. When in doubt, consult qualified legal counsel.
