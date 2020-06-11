# aws_scripts
Scripts to provision AWS using python boto3

Mainly to automate, hopefully, with single command
* create EC2 instance
  * generate of key pair for SSH
  * creating a Virtual Private Cloud ("VPC")
  * creating an Internet Gateway and associating with above VPC
  * creating default routes to Internet Gateway
  * associating the route table in VPC
  * create a Security Group associated with VPC
  * adding ingress rule to allow SSH to Security Group
  * creating a Subnet associated with VPC
  * creating EC2 instance with above
* terminating EC2 instance
  * delete the EC2 instance
  * remove the VPC associated using aws-vpc-destroy

# Pre-requisities
* Software Installation
  * On local laptop, need to install
    * Python 3
    * awscli and boto3
    ```
    pip install awscli boto3
    ```
* Create IAM accounts and obtain keys
  * On AWS console, IAM
    * Add User
      * check on Access type for
        * Programmatic Access
        * AWS Management Console access
    * Add permissions to above User
      * AdministratorAccess or assign to Group with acces
    * Create access key for above User
      * Click on User, access "Security Credentials" tab
        * click on "Create access key"
* Add keys to laptop
  * ~/.aws/config
  ```
  [default]
  aws_access_key_id = XXX
  aws_secret_access_key = xxxx
  region=ap-southeast-1
  ```
* Clone this with submodule
```
git clone git@github.com:JasonL888/aws_scripts.git --recursive
```

> if forget the recursive, can also do it post-cloning with
```
git submodules update --init 
```

# Usage
* Provision EC2 instance
```
python ec2_create_instance.py
```
> keys are generated stored in ec2_create_instance.pem
>
> debug logs are in ec2_create_instance.log


* Terminate EC2 instance
```
python ec2_terminate_instance.py
```

# License
Licence under [MIT](LICENSE)

# Acknowledgements
* Learnt a alot from article https://blog.ipswitch.com/how-to-create-and-configure-an-aws-vpc-with-python
* jeffbrl for his https://github.com/jeffbrl/aws-vpc-destroy
