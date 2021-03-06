﻿
        <h3 id="stringio">StringIO</h3>
<p>很多时候，数据读写不一定是文件，也可以在内存中读写。</p>
<p>StringIO顾名思义就是在内存中读写str。</p>
<p>要把str写入StringIO，我们需要先创建一个StringIO，然后，像文件一样写入即可：</p>
<pre><code>&gt;&gt;&gt; from io import StringIO
&gt;&gt;&gt; f = StringIO()
&gt;&gt;&gt; f.write(&#39;hello&#39;)
5
&gt;&gt;&gt; f.write(&#39; &#39;)
1
&gt;&gt;&gt; f.write(&#39;world!&#39;)
6
&gt;&gt;&gt; print(f.getvalue())
hello world!
</code></pre><p><code>getvalue()</code>方法用于获得写入后的str。</p>
<p>要读取StringIO，可以用一个str初始化StringIO，然后，像读文件一样读取：</p>
<pre><code>&gt;&gt;&gt; from io import StringIO
&gt;&gt;&gt; f = StringIO(&#39;Hello!\nHi!\nGoodbye!&#39;)
&gt;&gt;&gt; while True:
...     s = f.readline()
...     if s == &#39;&#39;:
...         break
...     print(s.strip())
...
Hello!
Hi!
Goodbye!
</code></pre><h3 id="bytesio">BytesIO</h3>
<p>StringIO操作的只能是str，如果要操作二进制数据，就需要使用BytesIO。</p>
<p>BytesIO实现了在内存中读写bytes，我们创建一个BytesIO，然后写入一些bytes：</p>
<pre><code>&gt;&gt;&gt; from io import BytesIO
&gt;&gt;&gt; f = BytesIO()
&gt;&gt;&gt; f.write(&#39;中文&#39;.encode(&#39;utf-8&#39;))
6
&gt;&gt;&gt; print(f.getvalue())
b&#39;\xe4\xb8\xad\xe6\x96\x87&#39;
</code></pre><p>请注意，写入的不是str，而是经过UTF-8编码的bytes。</p>
<p>和StringIO类似，可以用一个bytes初始化BytesIO，然后，像读文件一样读取：</p>
<pre><code>&gt;&gt;&gt; from io import BytesIO
&gt;&gt;&gt; f = BytesIO(b&#39;\xe4\xb8\xad\xe6\x96\x87&#39;)
&gt;&gt;&gt; f.read()
b&#39;\xe4\xb8\xad\xe6\x96\x87&#39;
</code></pre><h3 id="-">小结</h3>
<p>StringIO和BytesIO是在内存中操作str和bytes的方法，使得和读写文件具有一致的接口。</p>
<h3 id="-">参考源码</h3>
<p><a href="https://github.com/michaelliao/learn-python3/blob/master/samples/io/do_stringio.py">do_stringio.py</a></p>
<p><a href="https://github.com/michaelliao/learn-python3/blob/master/samples/io/do_bytesio.py">do_bytesio.py</a></p>

    