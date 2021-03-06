﻿
        <p>了解了HTTP协议和HTML文档，我们其实就明白了一个Web应用的本质就是：</p>
<ol>
<li><p>浏览器发送一个HTTP请求；</p>
</li>
<li><p>服务器收到请求，生成一个HTML文档；</p>
</li>
<li><p>服务器把HTML文档作为HTTP响应的Body发送给浏览器；</p>
</li>
<li><p>浏览器收到HTTP响应，从HTTP Body取出HTML文档并显示。</p>
</li>
</ol>
<p>所以，最简单的Web应用就是先把HTML用文件保存好，用一个现成的HTTP服务器软件，接收用户请求，从文件中读取HTML，返回。Apache、Nginx、Lighttpd等这些常见的静态服务器就是干这件事情的。</p>
<p>如果要动态生成HTML，就需要把上述步骤自己来实现。不过，接受HTTP请求、解析HTTP请求、发送HTTP响应都是苦力活，如果我们自己来写这些底层代码，还没开始写动态HTML呢，就得花个把月去读HTTP规范。</p>
<p>正确的做法是底层代码由专门的服务器软件实现，我们用Python专注于生成HTML文档。因为我们不希望接触到TCP连接、HTTP原始请求和响应格式，所以，需要一个统一的接口，让我们专心用Python编写Web业务。</p>
<p>这个接口就是WSGI：Web Server Gateway Interface。</p>
<p>WSGI接口定义非常简单，它只要求Web开发者实现一个函数，就可以响应HTTP请求。我们来看一个最简单的Web版本的“Hello, web!”：</p>
<pre><code>def application(environ, start_response):
    start_response(&#39;200 OK&#39;, [(&#39;Content-Type&#39;, &#39;text/html&#39;)])
    return [b&#39;&lt;h1&gt;Hello, web!&lt;/h1&gt;&#39;]
</code></pre><p>上面的<code>application()</code>函数就是符合WSGI标准的一个HTTP处理函数，它接收两个参数：</p>
<ul>
<li><p>environ：一个包含所有HTTP请求信息的<code>dict</code>对象；</p>
</li>
<li><p>start_response：一个发送HTTP响应的函数。</p>
</li>
</ul>
<p>在<code>application()</code>函数中，调用：</p>
<pre><code>start_response(&#39;200 OK&#39;, [(&#39;Content-Type&#39;, &#39;text/html&#39;)])
</code></pre><p>就发送了HTTP响应的Header，注意Header只能发送一次，也就是只能调用一次<code>start_response()</code>函数。<code>start_response()</code>函数接收两个参数，一个是HTTP响应码，一个是一组<code>list</code>表示的HTTP Header，每个Header用一个包含两个<code>str</code>的<code>tuple</code>表示。</p>
<p>通常情况下，都应该把<code>Content-Type</code>头发送给浏览器。其他很多常用的HTTP Header也应该发送。</p>
<p>然后，函数的返回值<code>b&#39;&lt;h1&gt;Hello, web!&lt;/h1&gt;&#39;</code>将作为HTTP响应的Body发送给浏览器。</p>
<p>有了WSGI，我们关心的就是如何从<code>environ</code>这个<code>dict</code>对象拿到HTTP请求信息，然后构造HTML，通过<code>start_response()</code>发送Header，最后返回Body。</p>
<p>整个<code>application()</code>函数本身没有涉及到任何解析HTTP的部分，也就是说，底层代码不需要我们自己编写，我们只负责在更高层次上考虑如何响应请求就可以了。</p>
<p>不过，等等，这个<code>application()</code>函数怎么调用？如果我们自己调用，两个参数<code>environ</code>和<code>start_response</code>我们没法提供，返回的<code>bytes</code>也没法发给浏览器。</p>
<p>所以<code>application()</code>函数必须由WSGI服务器来调用。有很多符合WSGI规范的服务器，我们可以挑选一个来用。但是现在，我们只想尽快测试一下我们编写的<code>application()</code>函数真的可以把HTML输出到浏览器，所以，要赶紧找一个最简单的WSGI服务器，把我们的Web应用程序跑起来。</p>
<p>好消息是Python内置了一个WSGI服务器，这个模块叫wsgiref，它是用纯Python编写的WSGI服务器的参考实现。所谓“参考实现”是指该实现完全符合WSGI标准，但是不考虑任何运行效率，仅供开发和测试使用。</p>
<h3 id="-wsgi-">运行WSGI服务</h3>
<p>我们先编写<code>hello.py</code>，实现Web应用程序的WSGI处理函数：</p>
<pre><code># hello.py

def application(environ, start_response):
    start_response(&#39;200 OK&#39;, [(&#39;Content-Type&#39;, &#39;text/html&#39;)])
    return [b&#39;&lt;h1&gt;Hello, web!&lt;/h1&gt;&#39;]
</code></pre><p>然后，再编写一个<code>server.py</code>，负责启动WSGI服务器，加载<code>application()</code>函数：</p>
<pre><code># server.py
# 从wsgiref模块导入:
from wsgiref.simple_server import make_server
# 导入我们自己编写的application函数:
from hello import application

# 创建一个服务器，IP地址为空，端口是8000，处理函数是application:
httpd = make_server(&#39;&#39;, 8000, application)
print(&#39;Serving HTTP on port 8000...&#39;)
# 开始监听HTTP请求:
httpd.serve_forever()
</code></pre><p>确保以上两个文件在同一个目录下，然后在命令行输入<code>python server.py</code>来启动WSGI服务器：</p>
<p><img src="../files/attachments/001400038640434579c45c375d244efbb229e98e5bd7691000.jpg" alt="wsgiref-start"></p>
<p>注意：如果<code>8000</code>端口已被其他程序占用，启动将失败，请修改成其他端口。</p>
<p>启动成功后，打开浏览器，输入<code>http://localhost:8000/</code>，就可以看到结果了：</p>
<p><img src="../files/attachments/0014000386233913cf4690bd4134b23aead27a11a7dbec9000.jpg" alt="hello-web"></p>
<p>在命令行可以看到wsgiref打印的log信息：</p>
<p><img src="../files/attachments/001400038605021a21e47e6f5d14ac181578f82fde58cb3000.jpg" alt="wsgiref-log"></p>
<p>按<code>Ctrl+C</code>终止服务器。</p>
<p>如果你觉得这个Web应用太简单了，可以稍微改造一下，从<code>environ</code>里读取<code>PATH_INFO</code>，这样可以显示更加动态的内容：</p>
<pre><code># hello.py

def application(environ, start_response):
    start_response(&#39;200 OK&#39;, [(&#39;Content-Type&#39;, &#39;text/html&#39;)])
    body = &#39;&lt;h1&gt;Hello, %s!&lt;/h1&gt;&#39; % (environ[&#39;PATH_INFO&#39;][1:] or &#39;web&#39;)
    return [body.encode(&#39;utf-8&#39;)]
</code></pre><p>你可以在地址栏输入用户名作为URL的一部分，将返回<code>Hello, xxx!</code>：</p>
<p><img src="../files/attachments/00140003866212417a4fdb1f8ad41ae99c80a75ca0dd432000.jpg" alt="hello-michael"></p>
<p>是不是有点Web App的感觉了？</p>
<h3 id="-">小结</h3>
<p>无论多么复杂的Web应用程序，入口都是一个WSGI处理函数。HTTP请求的所有输入信息都可以通过<code>environ</code>获得，HTTP响应的输出都可以通过<code>start_response()</code>加上函数返回值作为Body。</p>
<p>复杂的Web应用程序，光靠一个WSGI函数来处理还是太底层了，我们需要在WSGI之上再抽象出Web框架，进一步简化Web开发。</p>
<h3 id="-">参考源码</h3>
<p><a href="https://github.com/michaelliao/learn-python3/blob/master/samples/web/hello.py">hello.py</a></p>
<p><a href="https://github.com/michaelliao/learn-python3/blob/master/samples/web/do_wsgi.py">do_wsgi.py</a></p>

    