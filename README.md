# 🖼️ SL Photo Converter 

> A simple and practical serverless image converter built to learn and explore AWS.

[![AWS](https://img.shields.io/badge/AWS-Serverless-FF9900?logo=amazonaws&style=flat-square)](#)
[![Python](https://img.shields.io/badge/Python-3.x-3776AB?logo=python&style=flat-square)](#)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg?style=flat-square)](#)
[![Live Demo](https://img.shields.io/badge/Live_Demo-Click_Here-success?style=for-the-badge)](https://dm8g57umos2n0.cloudfront.net)

## 📖 Project Overview
SL Photo Converter is a lightweight web application that allows users to easily convert image formats (e.g., JPG, PNG, WebP) directly in their browsers. 

I built this project as a hands-on way to practice and understand AWS cloud services. Instead of using a traditional server that runs 24/7, this project uses an **AWS Serverless Architecture**. This means the system only runs when someone is actually converting a photo, making it highly cost-effective and a great way to learn cloud-native development.

🔗 **Live Demo:** https://dm8g57umos2n0.cloudfront.net

## 🏗️ System Architecture

![SL Photo Converter Architecture](assets/architecture.png)

### How it works:
1. **Client Request:** User accesses the static frontend hosted on S3 via CloudFront.
2. **Upload Ticket Generation:** The frontend requests an upload ticket. API Gateway triggers `GeneratePresignedURL`, which generates a time-limited **S3 Presigned URL**.
3. **Direct Upload:** The client uploads the original image directly to the S3 Input Bucket using the Presigned URL.
4. **Event-Driven Processing:** The S3 upload event automatically triggers `ProcessFileConverter`.
5. **Conversion:** `ProcessFileConverter` processes the image, converts it to the target format, and saves it to the S3 Output Bucket.
6. **Download:** The frontend polls for completion and retrieves the converted image via a secure download Presigned URL.

## 🛠️ Tech Stack

**Frontend:**
* HTML5, CSS3, JavaScript

**Backend & Cloud Infrastructure (AWS):**
* **Website Hosting:** Amazon S3
* **Compute:** AWS Lambda
* **Storage:** Amazon S3
* **Networking & Delivery:** Amazon CloudFront, Amazon API Gateway
* **Security & IAM:** AWS Identity and Access Management (IAM), S3 CORS, OAC

---

## 🎯 Learning Journey (Why I built this)

This project helped me step up from basic AWS tutorials to building a complete, secure, and cost-optimized system. It covers:
* Connecting different AWS services (S3, Lambda, API Gateway) securely.
* Learning Serverless concepts (zero-server management).
* Setting up basic cloud security (OAC, API Throttling).
* Understanding cost management (using S3 Lifecycle rules to delete files automatically).

## Local Setup & Deployment Guide

For anyone trying to replicate this architecture, follow this high-level deployment order:

[![Watch the video](https://img.youtube.com/vi/_5tFXJQIzi4/0.jpg)](https://www.youtube.com/watch?v=_5tFXJQIzi4)

### Phase 1: Storage & Compute (S3 & Lambda)
1. Clone the repository:
```bash
   git clone https://github.com/yourusername/sl-photo-converter.git
```

2. Create S3 Buckets: Create three separate S3 buckets (e.g., frontend-hosting, image-input, image-output). 

3. Configure IAM Roles: Create an IAM Role for your Lambda functions granting them AmazonS3FullAccess (or scoped down read/write permissions) and AWSLambdaBasicExecutionRole.

4. Deploy Lambda Functions: 
   - Create 'GeneratePresignedURL' and deploy the code from 'lambda/get_presigned_url.py'.
   - Create 'ProcessFileConverter' and deploy the code from 'lambda/process_image.py'.

5. Set up Event Triggers: In the 'image-input' S3 bucket, create an Event Notification that triggers the 'ProcessFileConverter' Lambda whenever a new object is created (s3:ObjectCreated:*).

### Phase 2: API & Security (API Gateway)
6. Create API Gateway: Create an HTTP API (or REST API) and link it to your 'GeneratePresignedURL' Lambda function.

7. Configure CORS: Enable CORS on the API Gateway to allow OPTIONS, GET, and POST requests from your frontend domain.

8. Set up Throttling: Configure rate limiting (e.g., Rate: 5, Burst: 10) to protect your AWS bill.

### Phase 3: Frontend & Global Delivery (CloudFront)
9. Update Frontend Configuration: Open 'frontend/script.js' and replace the placeholder API URL with your newly created API Gateway endpoint.

10. Upload Frontend: Upload your updated HTML, CSS, and JS files to the 'frontend-hosting' S3 bucket.

11. Create CloudFront Distribution: Create a distribution pointing to your 'frontend-hosting' S3 bucket. 

12. Enable OAC (Origin Access Control): Configure CloudFront OAC to restrict direct public access to your S3 hosting bucket, ensuring all traffic routes securely through the CDN.