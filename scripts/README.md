# Simplified Data Pipeline with AWS CDK

This project demonstrates a simple data pipeline using AWS services. It includes dynamically created S3 buckets for raw and processed data, a Glue job for ETL processing, and a script to generate input data for testing.

---

## **Project Structure**

project/
├── app.py                 # Entry point for the AWS CDK application
├── cdk.json               # CDK configuration file
├── requirements.txt       # Python dependencies
├── stacks/                # CDK stacks
│   ├── __init__.py
│   ├── s3_stack.py        # Creates S3 buckets for raw and processed data
│   └── glue_stack.py      # Defines the Glue ETL job
├── scripts/               # Supporting scripts
│   ├── data_generator.py  # Script to generate input data
│   └── etl_job.py         # Glue ETL job script
└── data/                  # Local data folder
    └── raw/               # Folder for raw input data

---

## **Setup Instructions**

### **1. Prerequisites**
- Python 3.8 or higher
- AWS CLI configured with proper credentials
- Node.js (for AWS CDK CLI)
- AWS CDK installed globally:
  npm install -g aws-cdk

### **2. Install Python Dependencies**
Set up a virtual environment and install the required libraries:

python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

### **3. Deploy the Infrastructure**
Synthesize and deploy the CDK stacks:
```bash
cdk synth
cdk deploy
```

---

## **Project Components**

### **1. S3 Buckets**
- **RawDataBucket**: Stores raw input data.
- **ProcessedDataBucket**: Stores processed data after transformation.

### **2. Glue Job**
- The Glue ETL job reads raw data from the `RawDataBucket`, applies transformations, and writes processed data to the `ProcessedDataBucket`.

### **3. Data Generator**
- The `data_generator.py` script creates test input data and saves it in the `data/raw` folder.

---

## **Usage Instructions**

### **1. Generate Test Data**
Run the data generator script to create a JSON file with 1,000 test entries:
```bash
python scripts/data_generator.py
```

### **2. Upload Data to S3**
Upload the generated file to the raw S3 bucket:
```bash
aws s3 cp data/raw/<generated_file>.json s3://<RawDataBucket>/
```

### **3. Run the Glue Job**
Trigger the Glue ETL job via the AWS Console or CLI:
```bash
aws glue start-job-run --job-name ETLJob
```

### **4. Verify Outputs**
Check the processed S3 bucket for transformed files:
```bash
aws s3 ls s3://<ProcessedDataBucket>/
```

---

## **Testing**

### **Manual Testing**
1. Run the data generator script to create test data.
2. Upload the generated file to the raw S3 bucket.
3. Trigger the Glue job and inspect the processed output in the processed S3 bucket.

### **Automated Testing**
- Use `pytest` and AWS CDK Assertions to validate the infrastructure deployment.

---

## **Future Enhancements**
- Add orchestration using AWS Step Functions.
- Integrate ML model training with SageMaker.
- Set up CI/CD pipelines using AWS CodePipeline.

---

## **Contributor**
- **Name** [Partha Sarathi Kundu](https://www.linkedin.com/in/partha-sarathi-kundu/recent-activity/articles/)

