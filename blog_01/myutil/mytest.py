import hashlib
import pymysql

def myhash(num,strinfo):

    h=hashlib.sha256()
    h.update(strinfo.encode('utf-8'))
    print(num,h.hexdigest(),sep='======')


if __name__=="__main__":
    l=[]
    settings = {'host': '127.0.0.1',
                'port': 3306,
                'user': 'root',
                'password': '123456',
                'database': 'myblog',
                'charset': 'utf8'}
    connect=pymysql.connect(**settings)
    cursor=connect.cursor()
    sql = 'select bbbp.sort_content,all_all.user_name,all_all.blog_title,bbbp.btop,all_all.gcc,all_all.ccb from (select uubbt.user_name,uubbt.user_avatar,uubbt.blog_id,uubbt.blog_title,uubbt.tc,cbiccbgcc.ccb,cbiccbgcc.gcc from ((select user_name,user_avatar,blog_id,blog_title,tc from tb_user join ( select blog_id,blog_title,tc,blog_user_id from tb_blog left join (select rel_blog_id, group_concat(tag_content)tc from tb_tag join ( select rel_blog_id,rel_tag_id from tb_blog_tag )t on tag_id = rel_tag_id group by rel_blog_id )t1 on blog_id = rel_blog_id )t2 on user_id = blog_user_id) as uubbt) left join ((select cbi.comment_blog_id,cbi.ccb,cbc.gcc from (((select comment_blog_id,count(comment_blog_id)ccb from tb_comment group by comment_blog_id) as cbi) join(select comment_blog_id,group_concat(comment_content)gcc from tb_comment group by comment_blog_id)cbc on cbc.comment_blog_id=cbi.comment_blog_id))as cbiccbgcc) on cbiccbgcc.comment_blog_id=uubbt.blog_id) as all_all join (select sort_biao.rel_blog_sort_id,sort_biao.sort_content,ppp.btop from (select tb_pic_blog.pic_blog_id,group_concat(tb_pic_blog.pic_photo) as btop from tb_pic_blog group by tb_pic_blog.pic_blog_id) as ppp join (select tb_sorts.sort_id,tb_sorts.sort_content,tb_blog_sorts.rel_blog_sort_id,tb_blog_sorts.rel_sort_id from tb_sorts join tb_blog_sorts on tb_sorts.sort_id=tb_blog_sorts.rel_sort_id) as sort_biao on sort_biao.rel_blog_sort_id=ppp.pic_blog_id) as bbbp on bbbp.rel_blog_sort_id=all_all.blog_id';
    cursor.execute(sql)
    connect.commit()
    result=cursor.fetchall()
    for re in result:
        print(re)
        #re[0]:分类
        #re[1]:作者
        #re[2]:标题
        #re[3]：照片
        #re[4]：内容
        #re[5]：评论条数
