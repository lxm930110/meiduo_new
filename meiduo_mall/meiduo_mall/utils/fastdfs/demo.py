from fdfs_client.client import Fdfs_client

if __name__ == '__main__':
    client = Fdfs_client('client.conf')
    ret = client.upload_appender_by_filename('/home/ubuntu/Desktop/121.jpg')
    print(ret)