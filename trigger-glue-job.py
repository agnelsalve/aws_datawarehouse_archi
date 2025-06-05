import boto3

def lambda_handler(event, context):
    glue = boto3.client('glue')
    response = glue.start_job_run(JobName='your-glue-job-name')
    return {
        'statusCode': 200,
        'body': f"Started Glue job: {response['JobRunId']}"
    }
