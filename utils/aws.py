import time

from utils.pathenv import get_path

import boto3


class Resource:
    def __init__(self, profile='default', region='ap-northeast-2'):
        self.session = boto3.Session(profile_name=profile, region_name=region)
        self.ec2 = self.session.resource('ec2')

    def ec2_on_off(self, name):
        """
        Name 태그를 통해 인스턴스 가동 및 중지를 스위칭합니다.
        """
        instances = self.get_instances(name)
        for instance in instances:
            if instance.state['Name'] == 'stopped':
                # Prevent telegram polling conflicts
                time.sleep(1)
                print('Start Instances ' + instance.instance_id)
                instance.start()
            elif instance.state['Name'] == 'running':
                print('Stop Instances ' + instance.instance_id)
                instance.stop()

    def get_instances(self, name):
        instances = []
        for instance in self.ec2.instances.all():
            if instance.tags:
                if True in [x['Value'] == name for x in instance.tags]:
                    instances.append(instance)
        return instances

    def create_instance(self, name='Auxiliary', count=1, security_group_ids=None, key_pair=None):
        """
        https://boto3.readthedocs.io/en/latest/reference/services/ec2.html#EC2.ServiceResource.create_instances
        Required EC2 Access in IAM
        For ssh access, security group ids(list), keypair(keyname) required
        """
        # FIXME: 프로젝트 Fork 시 쉘 스크립트 내부를 변경해야 합니다.
        with open(get_path('ec2_init_script.sh')) as fd:
            user_data = fd.read()

        self.ec2.create_instances(
            ImageId='ami-d28a53bc',
            InstanceType='t2.micro',
            MinCount=count,
            MaxCount=count,
            KeyName=key_pair,
            Monitoring={'Enabled': True},
            SecurityGroupIds=security_group_ids,
            UserData=user_data,
            TagSpecifications=[{
                'ResourceType': 'instance',
                'Tags': [{'Key': 'Name', 'Value': name}],
            }],
        )

        print('{}: {} instances created!'.format(name, count))
