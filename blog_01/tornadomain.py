from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from tornado.options import options, define, parse_config_file

from blog_01.app.myapp import MyApplication, IndexHandler, BlogHandler, AboutHandler, RegisterHandler, LoginHandler, \
    ArticleHandler, IndexModule, LoginModule, RegisterModule, BlogModule, ArticleModule, AboutModule, CheckUsername

#端口设置
define('duankou',type=int,default=8888)
#端口所在文件夹
parse_config_file('../config/config')
#路由配置


app=MyApplication(handlers=[('/',IndexHandler),
                          ('/blog',BlogHandler),
                          ('/about',AboutHandler),
                          ('/check',CheckUsername),
                          ('/login',LoginHandler),
                          ('/register',RegisterHandler),
                          ('/article',ArticleHandler),
                          ],
                template_path='mytemplates',
                static_path='mystatics',
                ui_modules={
                    'indexmodule':IndexModule,
                    'loginmodule':LoginModule,
                    'registermodule':RegisterModule,
                    'blogmodule':BlogModule,
                    'articlemodule':ArticleModule,
                    'aboutmodule':AboutModule,
                },)
#启动服务
server = HTTPServer(app)
#监听端口
server.listen(options.duankou)
IOLoop.current().start()

