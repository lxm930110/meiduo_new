
from django.core.files.storage import Storage
# 先导入我们安装的 fdfs_client.client 客户端
from fdfs_client.client import Fdfs_client
# 导入 settings 文件
from django.conf import settings

class FastDFSStorage(Storage):

    # 我们再添加一个新的方法
    # 该方法会在我们上传之前,判断文件名称是否冲突
    def exists(self, name):

        return False
    '''
    {'Group name': 'group1', 'Remote file_id':
     'group1/M00/00/00/wKhrlF6pqDmEAlBGAAAAAAxJkS4833.jpg', 
     'Status': 'Upload successed.',
      'Local file name': '/home/ubuntu/Desktop/121.jpg',
       'Uploaded size': '9.00KB', 'Storage IP': '192.168.107.188'}
    '''

    def save(self, name, content, max_length=None):
        # 创建客户端对象:
        client = Fdfs_client(settings.FDFS_CLIENT_CONF)

        result = client.upload_by_buffer(content.read())

        if result.get('Status') != 'Upload successed.':
            raise Exception('上传文件到FDFS系统失败')

        file_id = result.get('Remote file_id')

        return file_id
    def url(self, name):
        return settings.FDFS_URL + name
