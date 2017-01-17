
        <p>在正式开始Web开发前，我们需要编写一个Web框架。</p>
<p><code>aiohttp</code>已经是一个Web框架了，为什么我们还需要自己封装一个？</p>
<p>原因是从使用者的角度来说，<code>aiohttp</code>相对比较底层，编写一个URL的处理函数需要这么几步：</p>
<p>第一步，编写一个用<code>@asyncio.coroutine</code>装饰的函数：</p>
<pre><code>@asyncio.coroutine
def handle_url_xxx(request):
    pass
</code></pre><p>第二步，传入的参数需要自己从<code>request</code>中获取：</p>
<pre><code>url_param = request.match_info[&#39;key&#39;]
query_params = parse_qs(request.query_string)
</code></pre><p>最后，需要自己构造<code>Response</code>对象：</p>
<pre><code>text = render(&#39;template&#39;, data)
return web.Response(text.encode(&#39;utf-8&#39;))
</code></pre><p>这些重复的工作可以由框架完成。例如，处理带参数的URL<code>/blog/{id}</code>可以这么写：</p>
<pre><code>@get(&#39;/blog/{id}&#39;)
def get_blog(id):
    pass
</code></pre><p>处理<code>query_string</code>参数可以通过关键字参数<code>**kw</code>或者命名关键字参数接收：</p>
<pre><code>@get(&#39;/api/comments&#39;)
def api_comments(*, page=&#39;1&#39;):
    pass
</code></pre><p>对于函数的返回值，不一定是<code>web.Response</code>对象，可以是<code>str</code>、<code>bytes</code>或<code>dict</code>。</p>
<p>如果希望渲染模板，我们可以这么返回一个<code>dict</code>：</p>
<pre><code>return {
    &#39;__template__&#39;: &#39;index.html&#39;,
    &#39;data&#39;: &#39;...&#39;
}
</code></pre><p>因此，Web框架的设计是完全从使用者出发，目的是让使用者编写尽可能少的代码。</p>
<p>编写简单的函数而非引入<code>request</code>和<code>web.Response</code>还有一个额外的好处，就是可以单独测试，否则，需要模拟一个<code>request</code>才能测试。</p>
<h3 id="-get-post">@get和@post</h3>
<p>要把一个函数映射为一个URL处理函数，我们先定义<code>@get()</code>：</p>
<pre><code>def get(path):
    &#39;&#39;&#39;
    Define decorator @get(&#39;/path&#39;)
    &#39;&#39;&#39;
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kw):
            return func(*args, **kw)
        wrapper.__method__ = &#39;GET&#39;
        wrapper.__route__ = path
        return wrapper
    return decorator
</code></pre><p>这样，一个函数通过<code>@get()</code>的装饰就附带了URL信息。</p>
<p><code>@post</code>与<code>@get</code>定义类似。</p>
<h3 id="-requesthandler">定义RequestHandler</h3>
<p>URL处理函数不一定是一个<code>coroutine</code>，因此我们用<code>RequestHandler()</code>来封装一个URL处理函数。</p>
<p><code>RequestHandler</code>是一个类，由于定义了<code>__call__()</code>方法，因此可以将其实例视为函数。</p>
<p><code>RequestHandler</code>目的就是从URL函数中分析其需要接收的参数，从<code>request</code>中获取必要的参数，调用URL函数，然后把结果转换为<code>web.Response</code>对象，这样，就完全符合<code>aiohttp</code>框架的要求：</p>
<pre><code>class RequestHandler(object):

    def __init__(self, app, fn):
        self._app = app
        self._func = fn
        ...

    @asyncio.coroutine
    def __call__(self, request):
        kw = ... 获取参数
        r = yield from self._func(**kw)
        return r
</code></pre><p>再编写一个<code>add_route</code>函数，用来注册一个URL处理函数：</p>
<pre><code>def add_route(app, fn):
    method = getattr(fn, &#39;__method__&#39;, None)
    path = getattr(fn, &#39;__route__&#39;, None)
    if path is None or method is None:
        raise ValueError(&#39;@get or @post not defined in %s.&#39; % str(fn))
    if not asyncio.iscoroutinefunction(fn) and not inspect.isgeneratorfunction(fn):
        fn = asyncio.coroutine(fn)
    logging.info(&#39;add route %s %s =&gt; %s(%s)&#39; % (method, path, fn.__name__, &#39;, &#39;.join(inspect.signature(fn).parameters.keys())))
    app.router.add_route(method, path, RequestHandler(app, fn))
</code></pre><p>最后一步，把很多次<code>add_route()</code>注册的调用：</p>
<pre><code>add_route(app, handles.index)
add_route(app, handles.blog)
add_route(app, handles.create_comment)
...
</code></pre><p>变成自动扫描：</p>
<pre><code># 自动把handler模块的所有符合条件的函数注册了:
add_routes(app, &#39;handlers&#39;)
</code></pre><p><code>add_routes()</code>定义如下：</p>
<pre><code>def add_routes(app, module_name):
    n = module_name.rfind(&#39;.&#39;)
    if n == (-1):
        mod = __import__(module_name, globals(), locals())
    else:
        name = module_name[n+1:]
        mod = getattr(__import__(module_name[:n], globals(), locals(), [name]), name)
    for attr in dir(mod):
        if attr.startswith(&#39;_&#39;):
            continue
        fn = getattr(mod, attr)
        if callable(fn):
            method = getattr(fn, &#39;__method__&#39;, None)
            path = getattr(fn, &#39;__route__&#39;, None)
            if method and path:
                add_route(app, fn)
</code></pre><p>最后，在<code>app.py</code>中加入<code>middleware</code>、<code>jinja2</code>模板和自注册的支持：</p>
<pre><code>app = web.Application(loop=loop, middlewares=[
    logger_factory, response_factory
])
init_jinja2(app, filters=dict(datetime=datetime_filter))
add_routes(app, &#39;handlers&#39;)
add_static(app)
</code></pre><h3 id="middleware">middleware</h3>
<p><code>middleware</code>是一种拦截器，一个URL在被某个函数处理前，可以经过一系列的<code>middleware</code>的处理。</p>
<p>一个<code>middleware</code>可以改变URL的输入、输出，甚至可以决定不继续处理而直接返回。middleware的用处就在于把通用的功能从每个URL处理函数中拿出来，集中放到一个地方。例如，一个记录URL日志的<code>logger</code>可以简单定义如下：</p>
<pre><code>@asyncio.coroutine
def logger_factory(app, handler):
    @asyncio.coroutine
    def logger(request):
        # 记录日志:
        logging.info(&#39;Request: %s %s&#39; % (request.method, request.path))
        # 继续处理请求:
        return (yield from handler(request))
    return logger
</code></pre><p>而<code>response</code>这个<code>middleware</code>把返回值转换为<code>web.Response</code>对象再返回，以保证满足<code>aiohttp</code>的要求：</p>
<pre><code>@asyncio.coroutine
def response_factory(app, handler):
    @asyncio.coroutine
    def response(request):
        # 结果:
        r = yield from handler(request)
        if isinstance(r, web.StreamResponse):
            return r
        if isinstance(r, bytes):
            resp = web.Response(body=r)
            resp.content_type = &#39;application/octet-stream&#39;
            return resp
        if isinstance(r, str):
            resp = web.Response(body=r.encode(&#39;utf-8&#39;))
            resp.content_type = &#39;text/html;charset=utf-8&#39;
            return resp
        if isinstance(r, dict):
            ...
</code></pre><p>有了这些基础设施，我们就可以专注地往<code>handlers</code>模块不断添加URL处理函数了，可以极大地提高开发效率。</p>
<h3 id="-">参考源码</h3>
<p><a href="https://github.com/michaelliao/awesome-python3-webapp/tree/day-05">day-05</a></p>

    