# **📄 Product Requirements Document (PRD)**

## **Project: Smart Photo Gallery (Web App)**

**Author:** Nicolas Pintaux  
**Status:** Approved / Ready for Architectural Design  
**Framework Alignment:** Google Cloud Well-Architected Framework (GCWAF)

## ---

**📌 Executive Summary**

The **Smart Photo Gallery** is a highly interactive, modern web application designed to showcase curated photographic assets. This document defines both the functional user experience (detailed across 4 progressive iterations) and the non-functional requirements aligned with the five pillars of the **Google Cloud Well-Architected Framework (GCWAF)**.

The application is architected to be stateless, serverless, and secure by default, leveraging Google Cloud's modern application delivery suite.

## ---

**🗺️ Functional Requirements (The 4 User Stories)**

These user stories represent the developmental evolution of the application, showing how the product scales from a static baseline to a highly interactive, feature-rich platform.

| Story ID | Name | User Story | Acceptance Criteria (GIVEN/WHEN/THEN) | Visual/UI Outcome |
| :---- | :---- | :---- | :---- | :---- |
| **US1** | **Responsive Photo Grid** | **As a** visitor, **I want to** view a clean grid of photos, **So that** I can easily scan the collection. | **GIVEN** the gallery page load, **THEN** a responsive CSS grid of 6 photo cards is displayed. **WHEN** hovering over a photo card, **THEN** the image smoothly zooms in (scale 1.05) with a transition effect. **WHEN** viewing on mobile, **THEN** the grid collapses gracefully to a single-column layout. | Modern responsive grid layout with hover-zoom effects. |
| **US2** | **Interactive Lightbox View** | **As a** visitor, **I want to** click a photo to open a detailed modal view, **So that** I can see the image in high-resolution with metadata. | **GIVEN** the photo grid, **WHEN** clicking on any photo card, **THEN** a full-screen dark semi-transparent overlay (Lightbox) opens. **THEN** the modal displays the high-resolution image, title, and category badge. **WHEN** clicking the "X" button or the overlay background, **THEN** the modal smoothly closes. | Full-screen interactive modal with an elegant dark overlay. |
| **US3** | **Dynamic Category Filters** | **As a** visitor, **I want to** filter photos by category buttons, **So that** I only see images relevant to my interests. | **GIVEN** the gallery page, **THEN** a row of pill-shaped filter buttons (All, Nature, Urban, Minimal) is displayed at the top. **WHEN** clicking a filter button, **THEN** the active button is visually highlighted. **THEN** the grid dynamically filters to show only matching cards using a smooth fade transition. | Dynamic category navigation bar with smooth visual filtering. |
| **US4** | **"Like" Button & Global Counter** | **As a** logged-in user, **I want to** "like" a photo, **So that** I can express my preference and see the total community feedback. | **GIVEN** any photo card (or Lightbox view), **THEN** a heart-shaped outline button is visible. **WHEN** clicking the heart button, **THEN** the icon fills with red, and the card's individual like counter increases by 1\. **THEN** the global "Total Likes" counter in the header instantly animates and increments by 1\. | Interactive heart icons and an animated header metrics counter. |

## ---

**🛡️ Non-Functional Requirements (GCWAF Pillars)**

To guarantee enterprise readiness, the architecture of the Smart Photo Gallery strictly complies with Google Cloud Well-Architected Framework guidelines.

### **1\. Operational Excellence**

* **Infrastructure as Code (IaC):** The entire application environment must be defined using **Terraform**. No resources are to be provisioned manually in the Google Cloud Console.  
* **Continuous Integration & Deployment (CI/CD):**  
  * Deployments must be fully automated via **Google Cloud Build**.  
  * The loop execution is driven by the .agents/loop.yaml configuration triggered by Git commits on the repository.  
* **Observability:**  
  * **Cloud Logging:** Standardized application logs, structured in JSON format.  
  * **Cloud Monitoring:** Custom dashboards tracking CPU utilization, request latencies, HTTP 5xx error rates, and container concurrency.  
  * **Alerting Policies:** Instant Slack/Email alerts triggered if HTTP 5xx errors exceed 1% of total traffic over a 5-minute window.

### **2\. Security & Compliance**

* **Identity & Access Management (IAM):**  
  * Enforcement of the **principle of least privilege**. The Cloud Run service runs under a dedicated, limited service account with read-only access to Cloud Storage.  
* **Data Protection & Encryption:**  
  * All static assets (images) are stored in Google Cloud Storage.  
  * Encryption at rest is handled using **Customer-Managed Encryption Keys (CMEK)** managed via **Cloud KMS**.  
* **Network Security:**  
  * External entry points are protected by a **Global External HTTP(S) Load Balancer**.  
  * **Google Cloud Armor** is deployed with pre-configured WAF rules to block OWASP Top 10 vulnerabilities and rate-limit potential DDoS attacks.  
  * All transit data must use HTTPS (TLS 1.3 enforced).

### **3\. Reliability**

* **High Availability (HA):**  
  * The application is deployed on **Google Cloud Run** across multiple zones in the target region.  
  * Assets are stored in a **Dual-Region Cloud Storage bucket** (e.g., europe-west1 and europe-west9 for European users) to survive a single-region outage.  
* **Disaster Recovery (DR):**  
  * **Recovery Time Objective (RTO):** \< 15 minutes (fully automated serverless redeployment).  
  * **Recovery Point Objective (RPO):** \< 1 minute (for stateful like counters stored in database; 0 for stateless assets).  
* **Database HA:** Like counters are backed by a high-availability **Cloud SQL** instance (or serverless **Firestore** in Datastore mode) with multi-zone replication and Point-in-Time Recovery (PITR) enabled.

### **4\. Cost Optimization**

* **Serverless Scaling:**  
  * Cloud Run containers scale down to **0 instances** during periods of inactivity to completely eliminate idle compute costs.  
  * Concurrency limits are set to 80 requests per container to maximize resource utilization before spawning new instances.  
* **Scale Boundaries:**  
  * To prevent billing spikes from malicious traffic or runaway loops, the maximum scale is capped at **10 Cloud Run instances**.  
* **Storage Lifecycle Management:**  
  * A lifecycle policy is applied to the Cloud Storage bucket to automatically move uncompressed raw uploads to **Nearline Storage** after 30 days, and **Coldline Storage** after 90 days.

### **5\. Performance Efficiency**

* **Content Delivery Network (CDN):**  
  * **Google Cloud CDN** is enabled at the Load Balancer level to cache image assets globally at edge locations, reducing the Round Trip Time (RTT).  
  * Target Latency: **p95 \< 150ms** for cached assets globally.  
* **Asset Optimization:**  
  * The backend automatically compresses and generates WebP alternatives for uploaded images.  
  * Images must be served using responsive \<picture\> tags with srcset to avoid serving desktop-resolution assets to mobile devices.

## ---

**📊 WAF Readiness Scorecard**

| Assessment Area | Status | Score | Critical Blockers / Key Findings |
| :---- | :---- | :---- | :---- |
| **Coherence** | 🟢 OK | 100% | The development progression (US1 ➔ US4) matches the target serverless architecture perfectly. |
| **Operational Excellence** | 🟢 OK | 100% | Full automation via GitOps (loop.yaml \+ Cloud Build) and Terraform for infrastructure. |
| **Security & Reliability** | 🟢 OK | 100% | Least-privilege IAM, CMEK on Cloud Storage, and multi-region HA targets are clearly defined. |
| **Cost Optimization** | 🟢 OK | 100% | Zero-scale-enabled compute, safety boundaries, and Storage Lifecycle Policies implemented. |
| **Performance Efficiency** | 🟢 OK | 100% | Cloud CDN caching and server-side image optimization are explicitly planned. |

### ---