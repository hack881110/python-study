﻿
        <p>在Web应用中，服务器把网页传给浏览器，实际上就是把网页的HTML代码发送给浏览器，让浏览器显示出来。而浏览器和服务器之间的传输协议是HTTP，所以：</p>
<ul>
<li><p>HTML是一种用来定义网页的文本，会HTML，就可以编写网页；</p>
</li>
<li><p>HTTP是在网络上传输HTML的协议，用于浏览器和服务器的通信。</p>
</li>
</ul>
<p>在举例子之前，我们需要安装Google的<a href="http://www.google.com/intl/zh-CN/chrome/">Chrome浏览器</a>。</p>
<p>为什么要使用Chrome浏览器而不是IE呢？因为IE实在是太慢了，并且，IE对于开发和调试Web应用程序完全是一点用也没有。</p>
<p>我们需要在浏览器很方便地调试我们的Web应用，而Chrome提供了一套完整地调试工具，非常适合Web开发。</p>
<p>安装好Chrome浏览器后，打开Chrome，在菜单中选择“视图”，“开发者”，“开发者工具”，就可以显示开发者工具：</p>
<p><img src="../files/attachments/001399878215246e5c00e9142244698a91c5d558c5901a1000.jpg" alt="chrome-dev-tools"></p>
<p><code>Elements</code>显示网页的结构，<code>Network</code>显示浏览器和服务器的通信。我们点<code>Network</code>，确保第一个小红灯亮着，Chrome就会记录所有浏览器和服务器之间的通信：</p>
<p><img src="../files/attachments/001399878404470cf9e8257a27a4807b856b7dfa23f93a0000.jpg" alt="chrome-devtools-network"></p>
<p>当我们在地址栏输入<code>www.sina.com.cn</code>时，浏览器将显示新浪的首页。在这个过程中，浏览器都干了哪些事情呢？通过<code>Network</code>的记录，我们就可以知道。在<code>Network</code>中，定位到第一条记录，点击，右侧将显示<code>Request Headers</code>，点击右侧的<code>view source</code>，我们就可以看到浏览器发给新浪服务器的请求：</p>
<p><img src="../files/attachments/001399877287994279bc3d41b3040f985e3e8b838211465000.jpg" alt="sina-http-request"></p>
<p>最主要的头两行分析如下，第一行：</p>
<pre><code>GET / HTTP/1.1
</code></pre><p><code>GET</code>表示一个读取请求，将从服务器获得网页数据，<code>/</code>表示URL的路径，URL总是以<code>/</code>开头，<code>/</code>就表示首页，最后的<code>HTTP/1.1</code>指示采用的HTTP协议版本是1.1。目前HTTP协议的版本就是1.1，但是大部分服务器也支持1.0版本，主要区别在于1.1版本允许多个HTTP请求复用一个TCP连接，以加快传输速度。</p>
<p>从第二行开始，每一行都类似于<code>Xxx: abcdefg</code>：</p>
<pre><code>Host: www.sina.com.cn
</code></pre><p>表示请求的域名是<code>www.sina.com.cn</code>。如果一台服务器有多个网站，服务器就需要通过<code>Host</code>来区分浏览器请求的是哪个网站。</p>
<p>继续往下找到<code>Response Headers</code>，点击<code>view source</code>，显示服务器返回的原始响应数据：</p>
<p><img src="../files/attachments/0013998772979993bf20079a3d8452f9b44f9ec88f8a5c8000.jpg" alt="sina-http-response"></p>
<p>HTTP响应分为Header和Body两部分（Body是可选项），我们在<code>Network</code>中看到的Header最重要的几行如下：</p>
<pre><code>200 OK
</code></pre><p><code>200</code>表示一个成功的响应，后面的<code>OK</code>是说明。失败的响应有<code>404 Not Found</code>：网页不存在，<code>500 Internal Server Error</code>：服务器内部出错，等等。</p>
<pre><code>Content-Type: text/html
</code></pre><p><code>Content-Type</code>指示响应的内容，这里是<code>text/html</code>表示HTML网页。请注意，浏览器就是依靠<code>Content-Type</code>来判断响应的内容是网页还是图片，是视频还是音乐。浏览器并不靠URL来判断响应的内容，所以，即使URL是<code>http://example.com/abc.jpg</code>，它也不一定就是图片。</p>
<p>HTTP响应的Body就是HTML源码，我们在菜单栏选择“视图”，“开发者”，“查看网页源码”就可以在浏览器中直接查看HTML源码：</p>
<p><img src="../files/attachments/001399877306431ffee0ff7d3fe48bb88da759bb977c1e0000.jpg" alt="sina-http-source"></p>
<p>当浏览器读取到新浪首页的HTML源码后，它会解析HTML，显示页面，然后，根据HTML里面的各种链接，再发送HTTP请求给新浪服务器，拿到相应的图片、视频、Flash、JavaScript脚本、CSS等各种资源，最终显示出一个完整的页面。所以我们在<code>Network</code>下面能看到很多额外的HTTP请求。</p>
<h3 id="http-">HTTP请求</h3>
<p>跟踪了新浪的首页，我们来总结一下HTTP请求的流程：</p>
<p>步骤1：浏览器首先向服务器发送HTTP请求，请求包括：</p>
<p>方法：GET还是POST，GET仅请求资源，POST会附带用户数据；</p>
<p>路径：/full/url/path；</p>
<p>域名：由Host头指定：Host: www.sina.com.cn</p>
<p>以及其他相关的Header；</p>
<p>如果是POST，那么请求还包括一个Body，包含用户数据。</p>
<p>步骤2：服务器向浏览器返回HTTP响应，响应包括：</p>
<p>响应代码：200表示成功，3xx表示重定向，4xx表示客户端发送的请求有错误，5xx表示服务器端处理时发生了错误；</p>
<p>响应类型：由Content-Type指定；</p>
<p>以及其他相关的Header；</p>
<p>通常服务器的HTTP响应会携带内容，也就是有一个Body，包含响应的内容，网页的HTML源码就在Body中。</p>
<p>步骤3：如果浏览器还需要继续向服务器请求其他资源，比如图片，就再次发出HTTP请求，重复步骤1、2。</p>
<p>Web采用的HTTP协议采用了非常简单的请求-响应模式，从而大大简化了开发。当我们编写一个页面时，我们只需要在HTTP请求中把HTML发送出去，不需要考虑如何附带图片、视频等，浏览器如果需要请求图片和视频，它会发送另一个HTTP请求，因此，一个HTTP请求只处理一个资源。</p>
<p>HTTP协议同时具备极强的扩展性，虽然浏览器请求的是<code>http://www.sina.com.cn/</code>的首页，但是新浪在HTML中可以链入其他服务器的资源，比如<code>&lt;img src=&quot;http://i1.sinaimg.cn/home/2013/1008/U8455P30DT20131008135420.png&quot;&gt;</code>，从而将请求压力分散到各个服务器上，并且，一个站点可以链接到其他站点，无数个站点互相链接起来，就形成了World Wide Web，简称WWW。</p>
<h3 id="http-">HTTP格式</h3>
<p>每个HTTP请求和响应都遵循相同的格式，一个HTTP包含Header和Body两部分，其中Body是可选的。</p>
<p>HTTP协议是一种文本协议，所以，它的格式也非常简单。HTTP GET请求的格式：</p>
<pre><code>GET /path HTTP/1.1
Header1: Value1
Header2: Value2
Header3: Value3
</code></pre><p>每个Header一行一个，换行符是<code>\r\n</code>。</p>
<p>HTTP POST请求的格式：</p>
<pre><code>POST /path HTTP/1.1
Header1: Value1
Header2: Value2
Header3: Value3

body data goes here...
</code></pre><p>当遇到连续两个<code>\r\n</code>时，Header部分结束，后面的数据全部是Body。</p>
<p>HTTP响应的格式：</p>
<pre><code>200 OK
Header1: Value1
Header2: Value2
Header3: Value3

body data goes here...
</code></pre><p>HTTP响应如果包含body，也是通过<code>\r\n\r\n</code>来分隔的。请再次注意，Body的数据类型由<code>Content-Type</code>头来确定，如果是网页，Body就是文本，如果是图片，Body就是图片的二进制数据。</p>
<p>当存在<code>Content-Encoding</code>时，Body数据是被压缩的，最常见的压缩方式是gzip，所以，看到<code>Content-Encoding: gzip</code>时，需要将Body数据先解压缩，才能得到真正的数据。压缩的目的在于减少Body的大小，加快网络传输。</p>
<p>要详细了解HTTP协议，推荐“<a href="http://shop.oreilly.com/product/9781565925090.do">HTTP: The Definitive Guide</a>”一书，非常不错，有中文译本：</p>
<p><a href="http://t.cn/R7FguRq">HTTP权威指南</a></p>

    