# References & Resources
## Carbon Credit Eligibility AI Documentation

**Date:** November 28, 2025  
**Deployment Scope:** New Zealand Only  
**Purpose:** Comprehensive reference list for validation report, risk mitigation strategy, and legal compliance checklist

---

## 1. Legal & Regulatory References

### 1.1 New Zealand Privacy & Data Protection

**New Zealand Privacy Act 2020**
- Official Legislation: https://www.legislation.govt.nz/act/public/2020/0031/latest/LMS23223.html
- Office of the Privacy Commissioner: https://www.privacy.org.nz/
- Privacy Principles Guide: https://www.privacy.org.nz/privacy-act-2020/privacy-principles/
- Privacy Impact Assessment Guide: https://www.privacy.org.nz/assets/New-order/Privacy-Act-2020/Guides/PIA-guide-final.pdf

**Data Breach Notification**
- Notifiable Privacy Breaches: https://www.privacy.org.nz/privacy-act-2020/notifiable-privacy-breaches/

### 1.2 International Privacy Regulations (Reference Only - Not Applicable for NZ-Only Deployment)

> **Note:** These regulations are included for reference only. As this AI system operates exclusively within New Zealand, compliance with international privacy regulations is not required unless expanding internationally in the future.

**GDPR (General Data Protection Regulation)** - *Reference only*
- Official EU Regulation: https://gdpr.eu/
- GDPR Full Text: https://eur-lex.europa.eu/eli/reg/2016/679/oj
- ICO (UK) GDPR Guidance: https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/
- Article 22 (Automated Decision Making): https://gdpr.eu/article-22-automated-individual-decision-making/

**CCPA (California Consumer Privacy Act)** - *Reference only*
- Official Text: https://oag.ca.gov/privacy/ccpa
- CCPA Regulations: https://www.oag.ca.gov/privacy/ccpa

**PIPEDA (Canada)** - *Reference only*
- Privacy Commissioner of Canada: https://www.priv.gc.ca/en/privacy-topics/privacy-laws-in-canada/the-personal-information-protection-and-electronic-documents-act-pipeda/

### 1.3 AI Regulations & Guidelines

**New Zealand Algorithm Charter** - *Primary reference*
- Official Charter: https://data.govt.nz/toolkit/data-ethics/government-algorithm-transparency-and-accountability/
- Stats NZ Algorithm Assessment: https://data.govt.nz/assets/data-ethics/algorithm/Algorithm-assessment_Final.pdf

**EU AI Act** - *Reference only (not applicable to NZ-only deployment)*
- European Parliament Position: https://www.europarl.europa.eu/legislative-train/theme-a-europe-fit-for-the-digital-age/file-regulation-on-artificial-intelligence
- EU AI Act Text: https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:52021PC0206

**OECD AI Principles**
- OECD Recommendation on AI: https://oecd.ai/en/ai-principles
- Responsible AI Policy Framework: https://oecd.ai/en/dashboards/policy-initiatives

**UNESCO AI Ethics**
- Recommendation on Ethics of AI: https://unesdoc.unesco.org/ark:/48223/pf0000381137

### 1.4 Carbon Credit & Environmental Regulations

**New Zealand Emissions Trading Scheme (NZ ETS)**
- Climate Change Response Act 2002: https://www.legislation.govt.nz/act/public/2002/0040/latest/DLM158584.html
- EPA ETS Information: https://www.epa.govt.nz/industry-areas/emissions-trading-scheme/
- ETS Participant Guide: https://www.epa.govt.nz/assets/Uploads/Documents/Emissions-Trading-Scheme/Guidance/ETS-Participants-Guide.pdf
- Forestry ETS Guide: https://www.mpi.govt.nz/forestry/forestry-in-the-emissions-trading-scheme/

**Climate Change Response Act 2002**
- Full Act: https://www.legislation.govt.nz/act/public/2002/0040/latest/whole.html
- Ministry for the Environment: https://environment.govt.nz/what-government-is-doing/areas-of-work/climate-change/

**Resource Management Act 1991**
- Official Legislation: https://www.legislation.govt.nz/act/public/1991/0069/latest/DLM230265.html
- Ministry for the Environment Guidance: https://environment.govt.nz/acts-and-regulations/acts/resource-management-act/

**Forests Act 1949**
- Official Text: https://www.legislation.govt.nz/act/public/1949/0019/latest/DLM255626.html

### 1.5 International Carbon Standards (Reference Only)

> **Note:** These international standards are included for reference and best practices only. The NZ ETS is the primary regulatory framework for this deployment.

**Verified Carbon Standard (VCS)** - *Reference only*
- Verra VCS Program: https://verra.org/programs/verified-carbon-standard/
- VCS Standard: https://verra.org/wp-content/uploads/2019/09/VCS_Standard_v4.0.pdf

**Gold Standard** - *Reference only*
- Gold Standard for Global Goals: https://www.goldstandard.org/
- Standards Documents: https://www.goldstandard.org/articles/gold-standard-global-goals

**Climate Action Reserve** - *Reference only*
- Official Website: https://www.climateactionreserve.org/
- Program Manual: https://www.climateactionreserve.org/how/program-manual/

**ISO 14064 (GHG Accounting)**
- ISO 14064-1:2018: https://www.iso.org/standard/66453.html
- ISO Standards Overview: https://www.iso.org/iso-14001-environmental-management.html

**ISO 14065 (Verification Bodies)**
- ISO 14065:2020: https://www.iso.org/standard/74257.html

---

## 2. AI & Machine Learning Technical References

### 2.1 Model Architecture & Training

**EfficientNet**
- Original Paper: Tan, M., & Le, Q. (2019). "EfficientNet: Rethinking Model Scaling for Convolutional Neural Networks." ICML 2019.
- arXiv: https://arxiv.org/abs/1905.11946
- PyTorch Implementation: https://pytorch.org/vision/main/models/efficientnet.html

**PyTorch Deep Learning Framework**
- Official Documentation: https://pytorch.org/docs/stable/index.html
- Tutorials: https://pytorch.org/tutorials/

**Transfer Learning**
- Yosinski, J., et al. (2014). "How transferable are features in deep neural networks?" NeurIPS 2014.
- Survey: https://arxiv.org/abs/1808.01974

**Data Augmentation**
- Shorten, C., & Khoshgoftaar, T. M. (2019). "A survey on Image Data Augmentation for Deep Learning." Journal of Big Data, 6(1), 60.
- Albumentations Library: https://albumentations.ai/

### 2.2 Model Evaluation & Validation

**Classification Metrics**
- Scikit-learn Metrics: https://scikit-learn.org/stable/modules/model_evaluation.html
- Confusion Matrix Guide: https://scikit-learn.org/stable/modules/generated/sklearn.metrics.confusion_matrix.html

**ROC-AUC Analysis**
- Fawcett, T. (2006). "An introduction to ROC analysis." Pattern Recognition Letters, 27(8), 861-874.
- Scikit-learn ROC: https://scikit-learn.org/stable/modules/generated/sklearn.metrics.roc_auc_score.html

**Confidence Calibration**
- Guo, C., et al. (2017). "On Calibration of Modern Neural Networks." ICML 2017.
- arXiv: https://arxiv.org/abs/1706.04599

**Temperature Scaling**
- Platt Scaling & Calibration Methods: https://scikit-learn.org/stable/modules/calibration.html

### 2.3 AI Bias & Fairness

**Fairness Definitions**
- Verma, S., & Rubin, J. (2018). "Fairness definitions explained." IEEE/ACM International Workshop on Software Fairness.
- Google ML Fairness: https://developers.google.com/machine-learning/fairness-overview

**Bias Detection & Mitigation**
- IBM AI Fairness 360: https://aif360.mybluemix.net/
- Microsoft Fairlearn: https://fairlearn.org/

**Algorithmic Justice**
- Barocas, S., Hardt, M., & Narayanan, A. (2019). "Fairness and Machine Learning." fairmlbook.org

### 2.4 Explainable AI (XAI)

**Interpretability Methods**
- Molnar, C. (2022). "Interpretable Machine Learning." https://christophm.github.io/interpretable-ml-book/

**LIME (Local Interpretable Model-agnostic Explanations)**
- Ribeiro, M. T., et al. (2016). "'Why Should I Trust You?': Explaining the Predictions of Any Classifier." KDD 2016.
- GitHub: https://github.com/marcotcr/lime

**SHAP (SHapley Additive exPlanations)**
- Lundberg, S. M., & Lee, S. I. (2017). "A Unified Approach to Interpreting Model Predictions." NeurIPS 2017.
- Documentation: https://shap.readthedocs.io/

**Grad-CAM**
- Selvaraju, R. R., et al. (2017). "Grad-CAM: Visual Explanations from Deep Networks via Gradient-based Localization." ICCV 2017.

---

## 3. Information Security & Cybersecurity

### 3.1 Security Standards

**ISO 27001 (Information Security Management)**
- ISO 27001:2022: https://www.iso.org/standard/27001
- Implementation Guide: https://www.iso.org/isoiec-27001-information-security.html

**SOC 2 (Service Organization Controls)**
- AICPA SOC 2: https://www.aicpa.org/interestareas/frc/assuranceadvisoryservices/aicpasoc2report
- SOC 2 Compliance Guide: https://www.aicpa.org/resources/download/soc-2-compliance-simplified

**NIST Cybersecurity Framework**
- Framework Overview: https://www.nist.gov/cyberframework
- Core Functions: https://nvlpubs.nist.gov/nistpubs/CSWP/NIST.CSWP.04162018.pdf

**Essential 8 (Australian/NZ Context)**
- ACSC Essential Eight: https://www.cyber.gov.au/resources-business-and-government/essential-cyber-security/essential-eight
- Implementation Guide: https://www.cyber.gov.au/resources-business-and-government/essential-cyber-security/essential-eight/essential-eight-maturity-model

**CERT NZ (Computer Emergency Response Team)**
- Official Site: https://www.cert.govt.nz/
- Incident Reporting: https://www.cert.govt.nz/individuals/report-an-incident/

### 3.2 Data Protection & Encryption

**NIST Encryption Standards**
- AES-256: https://csrc.nist.gov/publications/detail/fips/197/final
- Cryptographic Standards: https://csrc.nist.gov/projects/cryptographic-standards-and-guidelines

**TLS Best Practices**
- OWASP TLS Cheat Sheet: https://cheatsheetseries.owasp.org/cheatsheets/Transport_Layer_Protection_Cheat_Sheet.html
- Mozilla SSL Configuration: https://wiki.mozilla.org/Security/Server_Side_TLS

---

## 4. Risk Management & Governance

### 4.1 Risk Management Frameworks

**ISO 31000 (Risk Management)**
- ISO 31000:2018: https://www.iso.org/iso-31000-risk-management.html
- Risk Management Principles: https://www.iso.org/standard/65694.html

**COSO ERM Framework**
- COSO Enterprise Risk Management: https://www.coso.org/Pages/erm.aspx

**NIST Risk Management Framework**
- RMF Overview: https://csrc.nist.gov/projects/risk-management/about-rmf

### 4.2 AI Governance

**AI Governance Frameworks**
- World Economic Forum AI Governance: https://www.weforum.org/projects/ai-governance-alliance/
- IEEE Ethically Aligned Design: https://standards.ieee.org/industry-connections/ec/ead-v1/

**Model Risk Management**
- Federal Reserve SR 11-7: https://www.federalreserve.gov/supervisionreg/srletters/sr1107.htm
- Bank of England Model Risk Management: https://www.bankofengland.co.uk/prudential-regulation/publication/2016/model-risk-management-principles-for-stress-testing

### 4.3 Corporate Governance

**OECD Principles of Corporate Governance**
- OECD Guidelines: https://www.oecd.org/corporate/principles-corporate-governance/

**ESG (Environmental, Social, Governance)**
- SASB Standards: https://www.sasb.org/
- GRI Standards: https://www.globalreporting.org/standards/

---

## 5. Insurance & Liability

### 5.1 Professional Indemnity & Liability

**Professional Indemnity Insurance Guide**
- Insurance Council of New Zealand: https://www.icnz.org.nz/

**Cyber Insurance**
- NIST Guide to Cyber Insurance: https://www.nist.gov/news-events/news/2019/04/nist-releases-guide-cyber-insurance
- Ponemon Institute Cyber Insurance Studies: https://www.ponemon.org/

**AI Liability Frameworks**
- EU Product Liability Directive: https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:31985L0374
- AI Liability White Paper: https://ec.europa.eu/info/sites/default/files/report_from_the_expert_group_on_liability_and_new_technologies.pdf

---

## 6. Industry Standards & Best Practices

### 6.1 AI Standards

**ISO/IEC 42001 (AI Management System)**
- ISO 42001:2023: https://www.iso.org/standard/81230.html
- Implementation Guide: https://www.iso.org/committee/6794475/x/catalogue/

**IEEE Standards for AI**
- IEEE 7000 Series: https://standards.ieee.org/
- IEEE P7001 (Transparency): https://standards.ieee.org/project/7001.html

**NIST AI Risk Management Framework**
- AI RMF: https://www.nist.gov/itl/ai-risk-management-framework
- Trustworthy AI: https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.100-1.pdf

### 6.2 Software Engineering Best Practices

**MLOps Best Practices**
- Google MLOps: https://cloud.google.com/architecture/mlops-continuous-delivery-and-automation-pipelines-in-machine-learning
- Microsoft MLOps Maturity: https://learn.microsoft.com/en-us/azure/architecture/example-scenario/mlops/mlops-maturity-model

**Model Versioning & Management**
- MLflow: https://mlflow.org/docs/latest/index.html
- DVC (Data Version Control): https://dvc.org/

**CI/CD for ML**
- Continuous Delivery for ML: https://martinfowler.com/articles/cd4ml.html

---

## 7. Domain-Specific (Remote Sensing & Land Use)

### 7.1 Remote Sensing & Satellite Imagery

**Land Cover Classification**
- Phiri, D., & Morgenroth, J. (2017). "Developments in Landsat Land Cover Classification Methods." Remote Sensing, 9(9), 967.
- ESA Land Cover: https://www.esa-landcover-cci.org/

**Deep Learning for Remote Sensing**
- Zhang, L., et al. (2016). "Deep learning for remote sensing data." IEEE Geoscience and Remote Sensing Magazine, 4(2), 22-40.
- Review Paper: https://arxiv.org/abs/1710.03959

### 7.2 New Zealand Land Cover Database

**LCDB (Land Cover Database)**
- Official Database: https://lris.scinfo.org.nz/layer/104400-lcdb-v50-land-cover-database-version-50-mainland-new-zealand/
- Landcare Research: https://www.landcareresearch.co.nz/tools-and-resources/mapping/lcdb/

**NZ Geospatial Data**
- LINZ Data Service: https://data.linz.govt.nz/
- Stats NZ Geographic Data: https://datafinder.stats.govt.nz/

---

## 8. Business & Legal Resources

### 8.1 Intellectual Property

**WIPO (World Intellectual Property Organization)**
- IP Basics: https://www.wipo.int/portal/en/
- AI & IP Policy: https://www.wipo.int/about-ip/en/artificial_intelligence/

**New Zealand Intellectual Property Office**
- IP New Zealand: https://www.iponz.govt.nz/
- Patent Guide: https://www.iponz.govt.nz/about-ip/patents/

### 8.2 Contract & Commercial Law

**New Zealand Contract Law**
- Contract and Commercial Law Act 2017: https://www.legislation.govt.nz/act/public/2017/0005/latest/DLM6844000.html

**Fair Trading Act 1986**
- Official Text: https://www.legislation.govt.nz/act/public/1986/0121/latest/DLM96439.html
- Commerce Commission: https://comcom.govt.nz/

**Consumer Guarantees Act 1993**
- Legislation: https://www.legislation.govt.nz/act/public/1993/0091/latest/DLM311053.html

---

## 9. Financial & Accounting

### 9.1 Tax & Financial Compliance

**New Zealand Tax System**
- Inland Revenue: https://www.ird.govt.nz/
- GST Registration: https://www.ird.govt.nz/gst/registering-for-gst

**Financial Reporting Standards**
- External Reporting Board: https://www.xrb.govt.nz/
- Accounting Standards: https://www.xrb.govt.nz/accounting-standards/

### 9.2 Anti-Money Laundering

**Anti-Money Laundering and Countering Financing of Terrorism Act 2009**
- Official Legislation: https://www.legislation.govt.nz/act/public/2009/0035/latest/DLM2140700.html
- DIA Guidance: https://www.dia.govt.nz/AML-CFT

---

## 10. Academic & Research Papers

### 10.1 AI Ethics & Responsible AI

- Jobin, A., et al. (2019). "The global landscape of AI ethics guidelines." Nature Machine Intelligence, 1(9), 389-399.
- Floridi, L., et al. (2018). "AI4People—An Ethical Framework for a Good AI Society." Minds and Machines, 28(4), 689-707.
- Mittelstadt, B. (2019). "Principles alone cannot guarantee ethical AI." Nature Machine Intelligence, 1(11), 501-507.

### 10.2 Carbon Credits & Climate Science

- Seddon, N., et al. (2019). "Understanding the value and limits of nature-based solutions to climate change." Philosophical Transactions of the Royal Society B, 375(1794).
- IPCC Special Report: https://www.ipcc.ch/sr15/
- New Zealand Climate Change Research: https://www.niwa.co.nz/climate

### 10.3 Computer Vision & Deep Learning

- LeCun, Y., et al. (2015). "Deep learning." Nature, 521(7553), 436-444.
- Goodfellow, I., et al. (2016). "Deep Learning." MIT Press. https://www.deeplearningbook.org/
- He, K., et al. (2016). "Deep Residual Learning for Image Recognition." CVPR 2016.

---

## 11. Professional Organizations & Resources

### 11.1 AI & Technology

**Partnership on AI**
- Website: https://partnershiponai.org/

**AI Now Institute**
- Research: https://ainowinstitute.org/

**The Alan Turing Institute**
- AI Ethics: https://www.turing.ac.uk/research/interest-groups/ai-ethics

### 11.2 Environmental & Carbon Markets

**International Carbon Action Partnership (ICAP)**
- ETS Resources: https://icapcarbonaction.com/

**Carbon Market Watch**
- Market Analysis: https://carbonmarketwatch.org/

**New Zealand Carbon Farming Association**
- Resources: https://www.carbonfarming.org.nz/

---

## 12. Tools & Software Documentation

### 12.1 Development Tools

**Python**
- Official Documentation: https://docs.python.org/3/

**PyTorch**
- Documentation: https://pytorch.org/docs/
- Tutorials: https://pytorch.org/tutorials/

**Scikit-learn**
- Documentation: https://scikit-learn.org/stable/

**OpenCV**
- Documentation: https://docs.opencv.org/

**Pandas**
- Documentation: https://pandas.pydata.org/docs/

### 12.2 Cloud & Infrastructure

**Microsoft Azure**
- Azure ML: https://learn.microsoft.com/en-us/azure/machine-learning/
- Azure Security: https://learn.microsoft.com/en-us/azure/security/

**AWS**
- SageMaker: https://aws.amazon.com/sagemaker/
- AWS Well-Architected: https://aws.amazon.com/architecture/well-architected/

**Google Cloud**
- Vertex AI: https://cloud.google.com/vertex-ai
- AI Best Practices: https://cloud.google.com/architecture/ml-on-gcp-best-practices

---

## 13. Industry Reports & Whitepapers

### 13.1 AI Industry Reports

- McKinsey Global Institute (2023). "The state of AI in 2023: Generative AI's breakout year."
- Gartner AI Maturity Model: https://www.gartner.com/en/documents/
- Forrester AI Wave Reports: https://www.forrester.com/

### 13.2 Carbon Market Reports

**New Zealand Specific:**
- Ministry for the Environment NZ ETS Reports: https://environment.govt.nz/what-government-is-doing/areas-of-work/climate-change/ets/
- Parliamentary Commissioner for the Environment: https://pce.parliament.nz/

**International (Reference):**
- World Bank State and Trends of Carbon Pricing: https://www.worldbank.org/en/programs/pricing-carbon
- Ecosystem Marketplace Reports: https://www.ecosystemmarketplace.com/

---

## 14. Training & Certification Resources

### 14.1 AI & ML Certifications

**Coursera**
- Deep Learning Specialization (Andrew Ng): https://www.coursera.org/specializations/deep-learning
- AI For Everyone: https://www.coursera.org/learn/ai-for-everyone

**Fast.ai**
- Practical Deep Learning: https://course.fast.ai/

### 14.2 Compliance & Privacy Certifications

**IAPP (International Association of Privacy Professionals)**
- CIPP/E, CIPM Certifications: https://iapp.org/certify/

**ISACA**
- CISA, CISM Certifications: https://www.isaca.org/credentialing

**ISC2**
- CISSP Certification: https://www.isc2.org/Certifications/CISSP

---

## 15. Conference Proceedings & Journals

### 15.1 AI & ML Conferences

- NeurIPS (Conference on Neural Information Processing Systems)
- ICML (International Conference on Machine Learning)
- CVPR (Computer Vision and Pattern Recognition)
- ICCV (International Conference on Computer Vision)
- AAAI (Association for the Advancement of Artificial Intelligence)

### 15.2 Academic Journals

- Nature Machine Intelligence
- Journal of Machine Learning Research (JMLR)
- IEEE Transactions on Pattern Analysis and Machine Intelligence
- ACM Transactions on Intelligent Systems and Technology

---

## Document Metadata

**Compiled By:** [Your Name/Organization]  
**Date:** November 28, 2025  
**Version:** 1.0  
**Last Updated:** November 28, 2025  
**Next Review:** February 28, 2026

---

## Notes on Reference Usage

This reference list supports the following documents:
1. **Validation Report** - Technical references for model architecture, evaluation metrics, and performance standards
2. **Risk Mitigation Strategy** - Risk management frameworks, security standards, and governance best practices
3. **Legal Compliance Checklist** - Regulatory requirements, privacy laws, carbon credit regulations, and compliance standards

**Deployment Scope:** This AI system is designed for deployment exclusively within New Zealand. International regulations (GDPR, CCPA, EU AI Act, etc.) are included for reference only and are not applicable to NZ-only operations. Primary compliance focus is on:
- New Zealand Privacy Act 2020
- NZ Emissions Trading Scheme (ETS)
- Climate Change Response Act 2002
- New Zealand Algorithm Charter (voluntary)
- NZ cybersecurity standards (Essential 8, CERT NZ)

**Disclaimer:** While every effort has been made to ensure accuracy, regulations and standards evolve. Always verify current requirements with official sources and legal counsel before making compliance decisions. If expanding internationally in the future, consult the international references and engage local legal counsel in target jurisdictions.

---

**END OF REFERENCES**
