
        <p>urllib提供了一系列用于操作URL的功能。</p>
<h3 id="get">Get</h3>
<p>urllib的<code>request</code>模块可以非常方便地抓取URL内容，也就是发送一个GET请求到指定的页面，然后返回HTTP的响应：</p>
<p>例如，对豆瓣的一个URL<code>https://api.douban.com/v2/book/2129650</code>进行抓取，并返回响应：</p>
<pre><code>from urllib import request

with request.urlopen(&#39;https://api.douban.com/v2/book/2129650&#39;) as f:
    data = f.read()
    print(&#39;Status:&#39;, f.status, f.reason)
    for k, v in f.getheaders():
        print(&#39;%s: %s&#39; % (k, v))
    print(&#39;Data:&#39;, data.decode(&#39;utf-8&#39;))
</code></pre><p>可以看到HTTP响应的头和JSON数据：</p>
<pre><code>Status: 200 OK
Server: nginx
Date: Tue, 26 May 2015 10:02:27 GMT
Content-Type: application/json; charset=utf-8
Content-Length: 2049
Connection: close
Expires: Sun, 1 Jan 2006 01:00:00 GMT
Pragma: no-cache
Cache-Control: must-revalidate, no-cache, private
X-DAE-Node: pidl1
Data: {&quot;rating&quot;:{&quot;max&quot;:10,&quot;numRaters&quot;:16,&quot;average&quot;:&quot;7.4&quot;,&quot;min&quot;:0},&quot;subtitle&quot;:&quot;&quot;,&quot;author&quot;:[&quot;廖雪峰编著&quot;],&quot;pubdate&quot;:&quot;2007-6&quot;,&quot;tags&quot;:[{&quot;count&quot;:20,&quot;name&quot;:&quot;spring&quot;,&quot;title&quot;:&quot;spring&quot;}...}
</code></pre><p>如果我们要想模拟浏览器发送GET请求，就需要使用<code>Request</code>对象，通过往<code>Request</code>对象添加HTTP头，我们就可以把请求伪装成浏览器。例如，模拟iPhone 6去请求豆瓣首页：</p>
<pre><code>from urllib import request

req = request.Request(&#39;http://www.douban.com/&#39;)
req.add_header(&#39;User-Agent&#39;, &#39;Mozilla/6.0 (iPhone; CPU iPhone OS 8_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/8.0 Mobile/10A5376e Safari/8536.25&#39;)
with request.urlopen(req) as f:
    print(&#39;Status:&#39;, f.status, f.reason)
    for k, v in f.getheaders():
        print(&#39;%s: %s&#39; % (k, v))
    print(&#39;Data:&#39;, f.read().decode(&#39;utf-8&#39;))
</code></pre><p>这样豆瓣会返回适合iPhone的移动版网页：</p>
<pre><code>...
    &lt;meta name=&quot;viewport&quot; content=&quot;width=device-width, user-scalable=no, initial-scale=1.0, minimum-scale=1.0, maximum-scale=1.0&quot;&gt;
    &lt;meta name=&quot;format-detection&quot; content=&quot;telephone=no&quot;&gt;
    &lt;link rel=&quot;apple-touch-icon&quot; sizes=&quot;57x57&quot; href=&quot;http://img4.douban.com/pics/cardkit/launcher/57.png&quot; /&gt;
...
</code></pre><h3 id="post">Post</h3>
<p>如果要以POST发送一个请求，只需要把参数<code>data</code>以bytes形式传入。</p>
<p>我们模拟一个微博登录，先读取登录的邮箱和口令，然后按照weibo.cn的登录页的格式以<code>username=xxx&amp;password=xxx</code>的编码传入：</p>
<pre><code>from urllib import request, parse

print(&#39;Login to weibo.cn...&#39;)
email = input(&#39;Email: &#39;)
passwd = input(&#39;Password: &#39;)
login_data = parse.urlencode([
    (&#39;username&#39;, email),
    (&#39;password&#39;, passwd),
    (&#39;entry&#39;, &#39;mweibo&#39;),
    (&#39;client_id&#39;, &#39;&#39;),
    (&#39;savestate&#39;, &#39;1&#39;),
    (&#39;ec&#39;, &#39;&#39;),
    (&#39;pagerefer&#39;, &#39;https://passport.weibo.cn/signin/welcome?entry=mweibo&amp;r=http%3A%2F%2Fm.weibo.cn%2F&#39;)
])

req = request.Request(&#39;https://passport.weibo.cn/sso/login&#39;)
req.add_header(&#39;Origin&#39;, &#39;https://passport.weibo.cn&#39;)
req.add_header(&#39;User-Agent&#39;, &#39;Mozilla/6.0 (iPhone; CPU iPhone OS 8_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/8.0 Mobile/10A5376e Safari/8536.25&#39;)
req.add_header(&#39;Referer&#39;, &#39;https://passport.weibo.cn/signin/login?entry=mweibo&amp;res=wel&amp;wm=3349&amp;r=http%3A%2F%2Fm.weibo.cn%2F&#39;)

with request.urlopen(req, data=login_data.encode(&#39;utf-8&#39;)) as f:
    print(&#39;Status:&#39;, f.status, f.reason)
    for k, v in f.getheaders():
        print(&#39;%s: %s&#39; % (k, v))
    print(&#39;Data:&#39;, f.read().decode(&#39;utf-8&#39;))
</code></pre><p>如果登录成功，我们获得的响应如下：</p>
<pre><code>Status: 200 OK
Server: nginx/1.2.0
...
Set-Cookie: SSOLoginState=1432620126; path=/; domain=weibo.cn
...
Data: {&quot;retcode&quot;:20000000,&quot;msg&quot;:&quot;&quot;,&quot;data&quot;:{...,&quot;uid&quot;:&quot;1658384301&quot;}}
</code></pre><p>如果登录失败，我们获得的响应如下：</p>
<pre><code>...
Data: {&quot;retcode&quot;:50011015,&quot;msg&quot;:&quot;\u7528\u6237\u540d\u6216\u5bc6\u7801\u9519\u8bef&quot;,&quot;data&quot;:{&quot;username&quot;:&quot;example@python.org&quot;,&quot;errline&quot;:536}}
</code></pre><h3 id="handler">Handler</h3>
<p>如果还需要更复杂的控制，比如通过一个Proxy去访问网站，我们需要利用<code>ProxyHandler</code>来处理，示例代码如下：</p>
<pre><code>proxy_handler = urllib.request.ProxyHandler({&#39;http&#39;: &#39;http://www.example.com:3128/&#39;})
proxy_auth_handler = urllib.request.ProxyBasicAuthHandler()
proxy_auth_handler.add_password(&#39;realm&#39;, &#39;host&#39;, &#39;username&#39;, &#39;password&#39;)
opener = urllib.request.build_opener(proxy_handler, proxy_auth_handler)
with opener.open(&#39;http://www.example.com/login.html&#39;) as f:
    pass
</code></pre><h3 id="-">小结</h3>
<p>urllib提供的功能就是利用程序去执行各种HTTP请求。如果要模拟浏览器完成特定功能，需要把请求伪装成浏览器。伪装的方法是先监控浏览器发出的请求，再根据浏览器的请求头来伪装，<code>User-Agent</code>头就是用来标识浏览器的。</p>
<h3 id="-">练习</h3>
<p>利用urllib读取XML，将XML一节的数据由硬编码改为由urllib获取：</p>
<pre class="x-python3">
from urllib import request, parse

def fetch_xml(url):
----
    pass
----
# 测试
print(fetch_xml('http://weather.yahooapis.com/forecastrss?u=c&w=2151330'))
</pre>

<h3 id="-">参考源码</h3>
<p><a href="https://github.com/michaelliao/learn-python3/blob/master/samples/commonlib/use_urllib.py">use_urllib.py</a></p>

    