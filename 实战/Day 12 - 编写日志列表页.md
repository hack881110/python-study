
        <p>MVVM模式不但可用于Form表单，在复杂的管理页面中也能大显身手。例如，分页显示Blog的功能，我们先把后端代码写出来：</p>
<p>在<code>apis.py</code>中定义一个<code>Page</code>类用于存储分页信息：</p>
<pre><code>class Page(object):

    def __init__(self, item_count, page_index=1, page_size=10):
        self.item_count = item_count
        self.page_size = page_size
        self.page_count = item_count // page_size + (1 if item_count % page_size &gt; 0 else 0)
        if (item_count == 0) or (page_index &gt; self.page_count):
            self.offset = 0
            self.limit = 0
            self.page_index = 1
        else:
            self.page_index = page_index
            self.offset = self.page_size * (page_index - 1)
            self.limit = self.page_size
        self.has_next = self.page_index &lt; self.page_count
        self.has_previous = self.page_index &gt; 1

    def __str__(self):
        return &#39;item_count: %s, page_count: %s, page_index: %s, page_size: %s, offset: %s, limit: %s&#39; % (self.item_count, self.page_count, self.page_index, self.page_size, self.offset, self.limit)

    __repr__ = __str__
</code></pre><p>在<code>handlers.py</code>中实现API：</p>
<pre><code>@get(&#39;/api/blogs&#39;)
def api_blogs(*, page=&#39;1&#39;):
    page_index = get_page_index(page)
    num = yield from Blog.findNumber(&#39;count(id)&#39;)
    p = Page(num, page_index)
    if num == 0:
        return dict(page=p, blogs=())
    blogs = yield from Blog.findAll(orderBy=&#39;created_at desc&#39;, limit=(p.offset, p.limit))
    return dict(page=p, blogs=blogs)
</code></pre><p>管理页面：</p>
<pre><code>@get(&#39;/manage/blogs&#39;)
def manage_blogs(*, page=&#39;1&#39;):
    return {
        &#39;__template__&#39;: &#39;manage_blogs.html&#39;,
        &#39;page_index&#39;: get_page_index(page)
    }
</code></pre><p>模板页面首先通过API：<code>GET /api/blogs?page=?</code>拿到Model：</p>
<pre><code>{
    &quot;page&quot;: {
        &quot;has_next&quot;: true,
        &quot;page_index&quot;: 1,
        &quot;page_count&quot;: 2,
        &quot;has_previous&quot;: false,
        &quot;item_count&quot;: 12
    },
    &quot;blogs&quot;: [...]
}
</code></pre><p>然后，通过Vue初始化MVVM：</p>
<pre><code>&lt;script&gt;
function initVM(data) {
    var vm = new Vue({
        el: &#39;#vm&#39;,
        data: {
            blogs: data.blogs,
            page: data.page
        },
        methods: {
            edit_blog: function (blog) {
                location.assign(&#39;/manage/blogs/edit?id=&#39; + blog.id);
            },
            delete_blog: function (blog) {
                if (confirm(&#39;确认要删除“&#39; + blog.name + &#39;”？删除后不可恢复！&#39;)) {
                    postJSON(&#39;/api/blogs/&#39; + blog.id + &#39;/delete&#39;, function (err, r) {
                        if (err) {
                            return alert(err.message || err.error || err);
                        }
                        refresh();
                    });
                }
            }
        }
    });
    $(&#39;#vm&#39;).show();
}
$(function() {
    getJSON(&#39;/api/blogs&#39;, {
        page: {{ page_index }}
    }, function (err, results) {
        if (err) {
            return fatal(err);
        }
        $(&#39;#loading&#39;).hide();
        initVM(results);
    });
});
&lt;/script&gt;
</code></pre><p>View的容器是<code>#vm</code>，包含一个table，我们用<code>v-repeat</code>可以把Model的数组<code>blogs</code>直接变成多行的<code>&lt;tr&gt;</code>：</p>
<pre><code>&lt;div id=&quot;vm&quot; class=&quot;uk-width-1-1&quot;&gt;
    &lt;a href=&quot;/manage/blogs/create&quot; class=&quot;uk-button uk-button-primary&quot;&gt;&lt;i class=&quot;uk-icon-plus&quot;&gt;&lt;/i&gt; 新日志&lt;/a&gt;

    &lt;table class=&quot;uk-table uk-table-hover&quot;&gt;
        &lt;thead&gt;
            &lt;tr&gt;
                &lt;th class=&quot;uk-width-5-10&quot;&gt;标题 / 摘要&lt;/th&gt;
                &lt;th class=&quot;uk-width-2-10&quot;&gt;作者&lt;/th&gt;
                &lt;th class=&quot;uk-width-2-10&quot;&gt;创建时间&lt;/th&gt;
                &lt;th class=&quot;uk-width-1-10&quot;&gt;操作&lt;/th&gt;
            &lt;/tr&gt;
        &lt;/thead&gt;
        &lt;tbody&gt;
            &lt;tr v-repeat=&quot;blog: blogs&quot; &gt;
                &lt;td&gt;
                    &lt;a target=&quot;_blank&quot; v-attr=&quot;href: &#39;/blog/&#39;+blog.id&quot; v-text=&quot;blog.name&quot;&gt;&lt;/a&gt;
                &lt;/td&gt;
                &lt;td&gt;
                    &lt;a target=&quot;_blank&quot; v-attr=&quot;href: &#39;/user/&#39;+blog.user_id&quot; v-text=&quot;blog.user_name&quot;&gt;&lt;/a&gt;
                &lt;/td&gt;
                &lt;td&gt;
                    &lt;span v-text=&quot;blog.created_at.toDateTime()&quot;&gt;&lt;/span&gt;
                &lt;/td&gt;
                &lt;td&gt;
                    &lt;a href=&quot;#0&quot; v-on=&quot;click: edit_blog(blog)&quot;&gt;&lt;i class=&quot;uk-icon-edit&quot;&gt;&lt;/i&gt;
                    &lt;a href=&quot;#0&quot; v-on=&quot;click: delete_blog(blog)&quot;&gt;&lt;i class=&quot;uk-icon-trash-o&quot;&gt;&lt;/i&gt;
                &lt;/td&gt;
            &lt;/tr&gt;
        &lt;/tbody&gt;
    &lt;/table&gt;

    &lt;div v-component=&quot;pagination&quot; v-with=&quot;page&quot;&gt;&lt;/div&gt;
&lt;/div&gt;
</code></pre><p>往Model的<code>blogs</code>数组中增加一个Blog元素，table就神奇地增加了一行；把<code>blogs</code>数组的某个元素删除，table就神奇地减少了一行。所有复杂的Model-View的映射逻辑全部由MVVM框架完成，我们只需要在HTML中写上<code>v-repeat</code>指令，就什么都不用管了。</p>
<p>可以把<code>v-repeat=&quot;blog: blogs&quot;</code>看成循环代码，所以，可以在一个<code>&lt;tr&gt;</code>内部引用循环变量<code>blog</code>。<code>v-text</code>和<code>v-attr</code>指令分别用于生成文本和DOM节点属性。</p>
<p>完整的Blog列表页如下：</p>
<p><img src="../files/attachments/0014025813192591fb147e5d8564257b6a94ca831a7f39f000.jpg" alt="awesomepy-manage-blogs"></p>
<h3 id="-">参考源码</h3>
<p><a href="https://github.com/michaelliao/awesome-python3-webapp/tree/day-12">day-12</a></p>

    