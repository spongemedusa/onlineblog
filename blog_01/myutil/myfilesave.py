"文件操作"
def fileoperation(fileurl,filename,data):
    """上传图片,保存到硬盘上"""
    with open(fileurl+'/%s'%(filename),'wb') as f:
        f.write(data)