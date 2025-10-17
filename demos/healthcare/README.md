# 🏥 Healthcare Demo

Patient operations with scheduling, case management, and medical reference data.

## 🚀 Quick Start

```bash
git clone git@github.com:hasura/axiom.git
cd axiom
cp .data/.env.template .data/healthcare/.env
cd demos/healthcare
ddn run dataset-up
ddn supergraph build local
ddn run docker-start
```

## ✨ Actions

- **Case Management** - Reassign cases, update urgency, mark cases at risk or for review
- **Scheduling** - Block emergency slots, adjust operator availability
- **Patient Operations** - Patient management and care coordination
- **Emergency Response** - Emergency slot management system
- **Insurance Integration** - Plan management and verification

## 📊 Data

- **Patients** - Demographics, medical history, insurance information
- **Providers** - Doctors, specialists, availability schedules
- **Appointments** - Scheduling, cancellations, no-shows, emergency slots
- **Medical Reference** - Medications, procedures, diagnostic codes
- **Cases** - Case urgency, risk assessment, reassignment, review flagging
- **Insurance** - Plans and coverage information
