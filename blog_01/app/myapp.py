from tornado.web import Application, UIModule, RequestHandler

from blog_01.myutil.myhash import mysha256
from blog_01.myutil.mymysql import MySqlHelp


#重写init并继承Application
class MyApplication(Application):
    def __init__(self,handlers,template_path,static_path,ui_modules):

        super().__init__(handlers=handlers,template_path=template_path,static_path=static_path,ui_modules=ui_modules)
        #实例化数据库
        self.myconn=MySqlHelp()

#首页，显示管理员推荐文章
class IndexHandler(RequestHandler):
    def get(self, *args, **kwargs):
        self.render('index.html')
    def post(self, *args, **kwargs):
        pass

#检查用户名是否存在
class CheckUsername(RequestHandler):
    def get(self, *args, **kwargs):
        pass
    def post(self, *args, **kwargs):
        username=self.get_body_argument('username',None)
        if self.application.myconn.checkusername(username):
            self.write({'msg':'用户名已存在'})


#登录界面,包括跳转头像
class LoginHandler(RequestHandler):
    def get(self, *args, **kwargs):
        self.render('login.html')
    def post(self, *args, **kwargs):
        username=self.get_body_argument('username',None)
        password=self.get_body_argument('password',None)
        #密码加密
        password=mysha256(password)
        if username and password:
            if self.application.myconn.isloginsuccess(username,password):
                #存在,则跳转博客页面
                self.redirect('/blog')
            else:
                #账号密码不正确，则返回首页请登录并提示用户名或者密码错误
                self.redirect('/login?error=failerror')

#注册界面,异步查询用户名是否存在
class RegisterHandler(RequestHandler):
    def get(self, *args, **kwargs):
        self.render('register.html')
    def post(self, *args, **kwargs):
        username=self.get_body_argument('username',None)
        password=self.get_body_argument('password',None)
        #密码加密
        password=mysha256(password)
        useremail=self.get_body_argument('email',None)
        #涉及隐私可以酌情考虑不填写
        #userphone=self.get_body_argument('phone_number',None)
        if username and password and useremail:
            try:
                self.application.myconn.isregister(username,password,useremail)
            except Exception as e:
                err = str(e)
                code = err.split(',')[0].split('(')[1]
                r = ''
                if code == '1062':
                    r = 'duplicate'
                else:
                    r = 'dberror'
                #返回登录界面从新登录
                self.redirect('/register?msg=' + r)
            else:
                #跳转到个人主页
                self.redirect('/about')



#自己博客界面
class BlogHandler(RequestHandler):
    def get(self, *args, **kwargs):
        self.render('blog.html')
    def post(self, *args, **kwargs):

        self.redirect('/blog')
#个人信息界面
class AboutHandler(RequestHandler):
    def get(self, *args, **kwargs):
        self.render('about.html')
    def post(self, *args, **kwargs):
        pass
#详细的文章界面
class ArticleHandler(RequestHandler):
    def get(self, *args, **kwargs):
        self.render('article.html')
    def post(self, *args, **kwargs):
        pass


#
class IndexModule(UIModule):
    def render(self, *args, **kwargs):

        result=self.handler.application.myconn.blogdatabase()

        return self.render_string('mystaticmodule/index_module.html',result=result)

class LoginModule(UIModule):
    def render(self, *args, **kwargs):
        ree=''
        if self.request.query:
            ree+="用户名或者密码错误"
        return self.render_string('mystaticmodule/login_module.html',result=ree)


class RegisterModule(UIModule):
    def render(self, *args, **kwargs):
        msg=''
        if self.request.query:
            whatworng = self.request.query.split('=')[1].split(',')[0]
            if whatworng == "duplicate":
                msg += "用户名已存在"
            else:
                msg += "数据库正在维护"
        return self.render_string('mystaticmodule/register_module.html',result=msg)

class BlogModule(UIModule):
    def render(self, *args, **kwargs):
        return self.render_string('mystaticmodule/blog_module.html',)

class ArticleModule(UIModule):
    def render(self, *args, **kwargs):
       return self.render_string('mystaticmodule/article_module.html',)

class AboutModule(UIModule):
    def render(self, *args, **kwargs):
        return self.render_string('mystaticmodule/about_module.html',)
