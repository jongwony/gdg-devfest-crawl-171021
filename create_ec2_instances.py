import argparse
from utils.aws import Resource


def aws_init(name='Auxiliary', count=1, security_group_ids=None, key_pair=None):
    aws = Resource()
    if not len(aws.get_instances(name)):
        aws.create_instance(name, count, security_group_ids, key_pair)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--name', required=True)
    parser.add_argument('--count', required=True)
    parser.add_argument('--keypair', required=True)
    parser.add_argument('--security-group-ids', required=True)
    args = parser.parse_args()

    aws_init(args.name, int(args.count), [args.security_group_ids], args.keypair)
