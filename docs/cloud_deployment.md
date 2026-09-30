# Cloud Deployment Guide

This guide details two production deployment pathways:
1. **Option A: Student / Free-Tier Cloud Deployment** (Zero-cost hosting with Render, Vercel, and Supabase).
2. **Option B: Enterprise Multi-Cloud Architecture** (AWS, Azure, and Google Cloud IoT Reference Blueprints).

---

## Option A: Student / Free-Tier Cloud Deployment

### 1. Cloud Database Setup (Supabase / Neon PostgreSQL)
1. Sign up for a free account at [Supabase](https://supabase.com) or [Neon](https://neon.tech).
2. Create a new PostgreSQL project named `smart-plant-cloud`.
3. Copy the database connection URI:
   ```text
   postgresql+psycopg2://postgres:[YOUR-PASSWORD]@db.xxxx.supabase.co:5432/postgres
   ```
4. Set this as the `DATABASE_URL` environment variable. The SQLAlchemy ORM will automatically create all tables on first startup!

### 2. Backend Cloud Deployment (Render.com / Railway / Fly.io)
1. Push your repository to GitHub.
2. Sign in to [Render](https://render.com) and click **New + > Web Service**.
3. Connect your GitHub repository.
4. Set the following build configuration:
   - **Environment:** `Python 3`
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `uvicorn backend.app:app --host 0.0.0.0 --port $PORT`
5. Configure Environment Variables in the Render dashboard:
   - `DATABASE_URL`: Your Supabase connection string.
   - `SECRET_KEY`: A secure random string.
   - `IOT_DEVICE_API_KEY`: Your secret IoT device key.
6. Click **Deploy Web Service**. Your backend is now live at `https://your-app.onrender.com`!

### 3. Frontend Cloud Deployment (Vercel / Netlify)
1. Sign in to [Vercel](https://vercel.com) and click **Add New Project**.
2. Select the repository and set **Root Directory** to `frontend`.
3. Build Settings:
   - **Framework Preset:** `Vite`
   - **Build Command:** `npm run build`
   - **Output Directory:** `dist`
4. Add Environment Variable:
   - `VITE_API_BASE`: `https://your-app.onrender.com`
5. Click **Deploy**. Your dashboard is now accessible globally with full HTTPS!

---

## Option B: Enterprise Multi-Cloud Architecture

### AWS Architecture Blueprint
```text
[IoT Nodes / ESP32]
        │ (MQTT over TLS / Port 8883)
        ▼
   AWS IoT Core
        │ (Rules Engine)
        ▼
   Amazon Kinesis Data Streams / SQS
        │
        ▼
   AWS Lambda (Serverless Compute - Decision Engine)
     ├── Writes Telemetry ──► Amazon Timestream / DynamoDB
     ├── Issues Actuation ──► AWS IoT Core Device Shadow / MQTT
     └── Dispatches Alerts ─► Amazon SNS (SMS / Email) / CloudWatch
        │
        ▼
   Amazon CloudFront + S3 (React Static Hosting)
```

### Multi-Cloud Service Mapping

| Architecture Layer | AWS Implementation | Azure Implementation | Google Cloud (GCP) Implementation |
|---|---|---|---|
| **IoT Connectivity** | AWS IoT Core | Azure IoT Hub | Google Cloud IoT / Cloud Pub/Sub |
| **Edge Protocol** | MQTT / HTTPS (X.509) | MQTT / AMQP / HTTPS | MQTT / HTTPS |
| **API Gateway** | Amazon API Gateway | Azure API Management | Google Cloud API Gateway / Apigee |
| **Compute / Logic** | AWS Lambda | Azure Functions | Google Cloud Functions / Cloud Run |
| **Event Streaming** | Amazon Kinesis / SQS | Azure Event Hubs | Google Cloud Pub/Sub |
| **Time-Series Storage**| Amazon Timestream / DynamoDB | Azure Cosmos DB / Data Explorer | Google Cloud Bigtable / Firestore |
| **Relational Storage** | Amazon RDS PostgreSQL | Azure Database for PostgreSQL | Google Cloud SQL (PostgreSQL) |
| **Object / UI Hosting**| Amazon S3 + CloudFront | Azure Blob Storage + CDN | Google Cloud Storage + Cloud CDN |
| **Alert Notification** | Amazon SNS | Azure Event Grid / Notification Hubs | Google Cloud Monitoring / Firebase FCM |
| **Secrets Management** | AWS Secrets Manager | Azure Key Vault | Google Cloud Secret Manager |
