"""连接数据库"""
import pymysql

class MySqlHelp:
    def __init__(self,host='127.0.0.1',port=3306,user='root',password='123456',database='myblog',charset='utf8'):
        self.host=host
        self.port=port
        self.user=user
        self.password=password
        self.database=database
        self.charset=charset
        self.conn=None#链接
        self.cursor=None#游标

    def ConnectDatabase(self):
        ##建立链接
        self.conn=pymysql.connect(host=self.host,port=self.port,user=self.user,password=self.password,database=self.database,charset=self.charset)
        if self.conn:
            self.cursor=self.conn.cursor()
        else:
            raise Exception("数据库参数有误!")

    def isloginsuccess(self,username,password):
        #根据输入数据链接参数
        # 建立与数据的链接
        sql = 'select count(*) from tb_user ' \
              'where user_name=%s and ' \
              'user_password=%s'
        params=(username,password)
        try:
            self.ConnectDatabase()
            self.cursor.execute(sql,params)
            result = self.cursor.fetchone()
            if result[0]:
                return True
            else:
                return False
        except Exception as e:
            raise e



    def isregister(self,username,password,useremail):
        """注册用户到数据库"""
        sql = 'insert into tb_user(user_name, user_password, user_email) values(%s,%s,%s);'
        params=(username,password,useremail)
        try:
            self.ConnectDatabase()
            self.cursor.execute(sql,params)
            self.conn.commit()
        except Exception as e:
            raise e

    def blogdatabase(self):
        """展示信息到推荐首页"""
        sql='select bbbp.sort_content,all_all.user_name,all_all.blog_title,all_all.blog_createdat,bbbp.btop,all_all.gcc,all_all.ccb from (select uubbt.user_name,uubbt.user_avatar,uubbt.blog_id,uubbt.blog_title,uubbt.tc,uubbt.blog_createdat,cbiccbgcc.ccb,cbiccbgcc.gcc from ((select user_name,user_avatar,blog_id,blog_title,tc,blog_createdat from tb_user join ( select blog_id,blog_title,tc,blog_user_id,blog_createdat from tb_blog left join (select rel_blog_id, group_concat(tag_content)tc from tb_tag join ( select rel_blog_id,rel_tag_id from tb_blog_tag )t on tag_id = rel_tag_id group by rel_blog_id )t1 on blog_id = rel_blog_id )t2 on user_id = blog_user_id) as uubbt) left join ((select cbi.comment_blog_id,cbi.ccb,cbc.gcc from (((select comment_blog_id,count(comment_blog_id)ccb from tb_comment group by comment_blog_id) as cbi) join(select comment_blog_id,group_concat(comment_content)gcc from tb_comment group by comment_blog_id)cbc on cbc.comment_blog_id=cbi.comment_blog_id))as cbiccbgcc) on cbiccbgcc.comment_blog_id=uubbt.blog_id) as all_all join (select sort_biao.rel_blog_sort_id,sort_biao.sort_content,ppp.btop from (select tb_pic_blog.pic_blog_id,group_concat(tb_pic_blog.pic_photo) as btop from tb_pic_blog group by tb_pic_blog.pic_blog_id) as ppp join (select tb_sorts.sort_id,tb_sorts.sort_content,tb_blog_sorts.rel_blog_sort_id,tb_blog_sorts.rel_sort_id from tb_sorts join tb_blog_sorts on tb_sorts.sort_id=tb_blog_sorts.rel_sort_id) as sort_biao on sort_biao.rel_blog_sort_id=ppp.pic_blog_id) as bbbp on bbbp.rel_blog_sort_id=all_all.blog_id;'
        try:
            self.ConnectDatabase()
            self.cursor.execute(sql)
            self.conn.commit()
            result=self.cursor.fetchall()
            blog = []
            for re in result:
                # re[0]:分类
                # re[1]:作者
                # re[2]:标题
                # re[3]：创建时间
                # re[4]：照片
                # re[5]：内容
                # re[6]：评论条数
                dictblog = {}
                dictblog['sort'] = re[0]
                dictblog['author'] = re[1]
                dictblog['title'] = re[2]
                dictblog['createtime'] = str(re[3])[5:19]
                if re[4]:
                    dictblog['photo'] = re[4]
                else:
                    dictblog['photo'] = ''

                dictblog['content'] = re[5]

                dictblog['count'] = re[6]
                blog.append(dictblog)
            return blog
        except Exception as e:
            raise e
    def checkusername(self,username):
        sql='select count(*) from tb_user where user_name=%s;'
        params=(username,)
        try:
            self.ConnectDatabase()
            self.cursor.execute(sql,params)
            self.conn.commit()
            result=self.cursor.fetchone()
            if result[0]:
                return result[0]

        except Exception as e:
            raise e
    def checkuserphoto(self,username):
        """检查用户头像"""
        sql='select user_avatar from tb_user where user_name=%s'
        params=(username,)
        try:
            self.ConnectDatabase()
            self.cursor.execute(sql,params)
            self.conn.commit()
            result=self.cursor.fetchone()
            if result:
                return result[0]

        except Exception as e:
            raise e
    def checkexistsname(self,username):
        """检查姓名是否存在"""
        sql='select user_id from tb_user where username=%s'
        params=(username,)
        try:
            self.ConnectDatabase()
            self.cursor.execute(sql,params)
            self.conn.commit()
            result=self.cursor.fetchone()
            if result:
                return result[0]
            else:
                return False
        except Exception as e:
            raise e

    def showuserbolg(self,username):
        sql='select '

