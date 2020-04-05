
# Region

# VPC
# Private Subnet
# Public Subnet
# Security Group

# Availability Zone
# AWS Step Functions Workflow
# Elastic Beanstalk container
# Auto Scaling Group

# Server contents
# EC2 instance contents
# Spot Fleet

groups = {
    'AWS::AccountId': {'level': 0},
    'AWS::Region': {'level': 1},
    'AWS::IAM::': {'level': 2},
    'AWS::EC2::VPC': {'level': 3},
    'AvailabilityZone': {'level': 4},
    'AWS::EC2::SecurityGroup': {'level': 4},
    'AWS::EC2::Subnet': {'level': 5},
    'Default': {'level': 6} # e.g. EC2 instance
}

blacklist_resource_types = [
    'AWS::SSM::Parameter',
    'AWS::Lambda::Permission',
    'AWS::ApiGateway::Deployment',
    'AWS::Lambda::Version',
    'AWS::Lambda::LayerVersionPermission',
    'AWS::IAM::ManagedPolicy',
    'AWS::SQS::QueuePolicy'
]

# https://aws.amazon.com/architecture/icons/
resource_type_image = {
    'AWS::Serverless::Function': 'AWS-Lambda_Lambda-Function_light-bg@4x.png',
    'AWS::Serverless::LayerVersion': 'AWS-Lambda@4x.png',
    # 'AWS::Lambda::LayerVersionPermission': '',
    'AWS::Serverless::Api': 'Amazon-API-Gateway_Endpoint_light-bg@4x.png',
    'AWS::IAM::Role': 'AWS-Identity-and-Access-Management-IAM_Role_light-bg@4x.png',
    'AWS::ApiGateway::Account': 'Amazon-API-Gateway_Endpoint_light-bg@4x.png',
    'AWS::Logs::LogGroup': 'Amazon-CloudWatch@4x.png',
    'AWS::S3::Bucket': 'Amazon-Simple-Storage-Service-S3_Bucket_light-bg@4x.png',
    'AWS::SNS::Topic': 'Amazon-Simple-Notification-Service-SNS_Topic_light-bg@4x.png',
    'AWS::SQS::Queue': 'Amazon-Simple-Queue-Service-SQS_Queue_light-bg@4x.png',
    # 'AWS::SQS::QueuePolicy': '',
    'AWS::SNS::Subscription': 'Amazon-Simple-Notification-Service-SNS_light-bg@4x.png',
    'AWS::IAM::ManagedPolicy': 'AWS-Identity-and-Access-Management-IAM_Permissions_light-bg@4x.png',
    'AWS::SSM::Parameter': 'AWS-Systems-Manager_Parameter-Store_light-bg@4x.png'
}
