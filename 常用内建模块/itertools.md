﻿
        <p>Python的内建模块<code>itertools</code>提供了非常有用的用于操作迭代对象的函数。</p>
<p>首先，我们看看<code>itertools</code>提供的几个“无限”迭代器：</p>
<pre><code>&gt;&gt;&gt; import itertools
&gt;&gt;&gt; natuals = itertools.count(1)
&gt;&gt;&gt; for n in natuals:
...     print(n)
...
1
2
3
...
</code></pre><p>因为<code>count()</code>会创建一个无限的迭代器，所以上述代码会打印出自然数序列，根本停不下来，只能按<code>Ctrl+C</code>退出。</p>
<p><code>cycle()</code>会把传入的一个序列无限重复下去：</p>
<pre><code>&gt;&gt;&gt; import itertools
&gt;&gt;&gt; cs = itertools.cycle(&#39;ABC&#39;) # 注意字符串也是序列的一种
&gt;&gt;&gt; for c in cs:
...     print(c)
...
&#39;A&#39;
&#39;B&#39;
&#39;C&#39;
&#39;A&#39;
&#39;B&#39;
&#39;C&#39;
...
</code></pre><p>同样停不下来。</p>
<p><code>repeat()</code>负责把一个元素无限重复下去，不过如果提供第二个参数就可以限定重复次数：</p>
<pre><code>&gt;&gt;&gt; ns = itertools.repeat(&#39;A&#39;, 3)
&gt;&gt;&gt; for n in ns:
...     print(n)
...
A
A
A
</code></pre><p>无限序列只有在<code>for</code>迭代时才会无限地迭代下去，如果只是创建了一个迭代对象，它不会事先把无限个元素生成出来，事实上也不可能在内存中创建无限多个元素。</p>
<p>无限序列虽然可以无限迭代下去，但是通常我们会通过<code>takewhile()</code>等函数根据条件判断来截取出一个有限的序列：</p>
<pre><code>&gt;&gt;&gt; natuals = itertools.count(1)
&gt;&gt;&gt; ns = itertools.takewhile(lambda x: x &lt;= 10, natuals)
&gt;&gt;&gt; list(ns)
[1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
</code></pre><p><code>itertools</code>提供的几个迭代器操作函数更加有用：</p>
<h3 id="chain-">chain()</h3>
<p><code>chain()</code>可以把一组迭代对象串联起来，形成一个更大的迭代器：</p>
<pre><code>&gt;&gt;&gt; for c in itertools.chain(&#39;ABC&#39;, &#39;XYZ&#39;):
...     print(c)
# 迭代效果：&#39;A&#39; &#39;B&#39; &#39;C&#39; &#39;X&#39; &#39;Y&#39; &#39;Z&#39;
</code></pre><h3 id="groupby-">groupby()</h3>
<p><code>groupby()</code>把迭代器中相邻的重复元素挑出来放在一起：</p>
<pre><code>&gt;&gt;&gt; for key, group in itertools.groupby(&#39;AAABBBCCAAA&#39;):
...     print(key, list(group))
...
A [&#39;A&#39;, &#39;A&#39;, &#39;A&#39;]
B [&#39;B&#39;, &#39;B&#39;, &#39;B&#39;]
C [&#39;C&#39;, &#39;C&#39;]
A [&#39;A&#39;, &#39;A&#39;, &#39;A&#39;]
</code></pre><p>实际上挑选规则是通过函数完成的，只要作用于函数的两个元素返回的值相等，这两个元素就被认为是在一组的，而函数返回值作为组的key。如果我们要忽略大小写分组，就可以让元素<code>&#39;A&#39;</code>和<code>&#39;a&#39;</code>都返回相同的key：</p>
<pre><code>&gt;&gt;&gt; for key, group in itertools.groupby(&#39;AaaBBbcCAAa&#39;, lambda c: c.upper()):
...     print(key, list(group))
...
A [&#39;A&#39;, &#39;a&#39;, &#39;a&#39;]
B [&#39;B&#39;, &#39;B&#39;, &#39;b&#39;]
C [&#39;c&#39;, &#39;C&#39;]
A [&#39;A&#39;, &#39;A&#39;, &#39;a&#39;]
</code></pre><h3 id="-">小结</h3>
<p><code>itertools</code>模块提供的全部是处理迭代功能的函数，它们的返回值不是list，而是<code>Iterator</code>，只有用<code>for</code>循环迭代的时候才真正计算。</p>
<h3 id="-">参考源码</h3>
<p><a href="https://github.com/michaelliao/learn-python3/blob/master/samples/commonlib/use_itertools.py">use_itertools.py</a></p>

    