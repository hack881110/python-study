﻿
        <p>Python内建了<code>map()</code>和<code>reduce()</code>函数。</p>
<p>如果你读过Google的那篇大名鼎鼎的论文“<a href="http://research.google.com/archive/mapreduce.html">MapReduce: Simplified Data Processing on Large Clusters</a>”，你就能大概明白map/reduce的概念。</p>
<p>我们先看map。<code>map()</code>函数接收两个参数，一个是函数，一个是<code>Iterable</code>，<code>map</code>将传入的函数依次作用到序列的每个元素，并把结果作为新的<code>Iterator</code>返回。</p>
<p>举例说明，比如我们有一个函数f(x)=x<sup>2</sup>，要把这个函数作用在一个list <code>[1, 2, 3, 4, 5, 6, 7, 8, 9]</code>上，就可以用<code>map()</code>实现如下：</p>
<p><img src="../files/attachments/0013879622109990efbf9d781704b02994ba96765595f56000/0.jpg" alt="map"></p>
<p>现在，我们用Python代码实现：</p>
<pre><code>&gt;&gt;&gt; def f(x):
...     return x * x
...
&gt;&gt;&gt; r = map(f, [1, 2, 3, 4, 5, 6, 7, 8, 9])
&gt;&gt;&gt; list(r)
[1, 4, 9, 16, 25, 36, 49, 64, 81]
</code></pre><p><code>map()</code>传入的第一个参数是<code>f</code>，即函数对象本身。由于结果<code>r</code>是一个<code>Iterator</code>，<code>Iterator</code>是惰性序列，因此通过<code>list()</code>函数让它把整个序列都计算出来并返回一个list。</p>
<p>你可能会想，不需要<code>map()</code>函数，写一个循环，也可以计算出结果：</p>
<pre><code>L = []
for n in [1, 2, 3, 4, 5, 6, 7, 8, 9]:
    L.append(f(n))
print(L)
</code></pre><p>的确可以，但是，从上面的循环代码，能一眼看明白“把f(x)作用在list的每一个元素并把结果生成一个新的list”吗？</p>
<p>所以，<code>map()</code>作为高阶函数，事实上它把运算规则抽象了，因此，我们不但可以计算简单的f(x)=x<sup>2</sup>，还可以计算任意复杂的函数，比如，把这个list所有数字转为字符串：</p>
<pre><code>&gt;&gt;&gt; list(map(str, [1, 2, 3, 4, 5, 6, 7, 8, 9]))
[&#39;1&#39;, &#39;2&#39;, &#39;3&#39;, &#39;4&#39;, &#39;5&#39;, &#39;6&#39;, &#39;7&#39;, &#39;8&#39;, &#39;9&#39;]
</code></pre><p>只需要一行代码。</p>
<p>再看<code>reduce</code>的用法。<code>reduce</code>把一个函数作用在一个序列<code>[x1, x2, x3, ...]</code>上，这个函数必须接收两个参数，<code>reduce</code>把结果继续和序列的下一个元素做累积计算，其效果就是：</p>
<pre><code>reduce(f, [x1, x2, x3, x4]) = f(f(f(x1, x2), x3), x4)
</code></pre><p>比方说对一个序列求和，就可以用<code>reduce</code>实现：</p>
<pre><code>&gt;&gt;&gt; from functools import reduce
&gt;&gt;&gt; def add(x, y):
...     return x + y
...
&gt;&gt;&gt; reduce(add, [1, 3, 5, 7, 9])
25
</code></pre><p>当然求和运算可以直接用Python内建函数<code>sum()</code>，没必要动用<code>reduce</code>。</p>
<p>但是如果要把序列<code>[1, 3, 5, 7, 9]</code>变换成整数<code>13579</code>，<code>reduce</code>就可以派上用场：</p>
<pre><code>&gt;&gt;&gt; from functools import reduce
&gt;&gt;&gt; def fn(x, y):
...     return x * 10 + y
...
&gt;&gt;&gt; reduce(fn, [1, 3, 5, 7, 9])
13579
</code></pre><p>这个例子本身没多大用处，但是，如果考虑到字符串<code>str</code>也是一个序列，对上面的例子稍加改动，配合<code>map()</code>，我们就可以写出把<code>str</code>转换为<code>int</code>的函数：</p>
<pre><code>&gt;&gt;&gt; from functools import reduce
&gt;&gt;&gt; def fn(x, y):
...     return x * 10 + y
...
&gt;&gt;&gt; def char2num(s):
...     return {&#39;0&#39;: 0, &#39;1&#39;: 1, &#39;2&#39;: 2, &#39;3&#39;: 3, &#39;4&#39;: 4, &#39;5&#39;: 5, &#39;6&#39;: 6, &#39;7&#39;: 7, &#39;8&#39;: 8, &#39;9&#39;: 9}[s]
...
&gt;&gt;&gt; reduce(fn, map(char2num, &#39;13579&#39;))
13579
</code></pre><p>整理成一个<code>str2int</code>的函数就是：</p>
<pre><code>from functools import reduce

def str2int(s):
    def fn(x, y):
        return x * 10 + y
    def char2num(s):
        return {&#39;0&#39;: 0, &#39;1&#39;: 1, &#39;2&#39;: 2, &#39;3&#39;: 3, &#39;4&#39;: 4, &#39;5&#39;: 5, &#39;6&#39;: 6, &#39;7&#39;: 7, &#39;8&#39;: 8, &#39;9&#39;: 9}[s]
    return reduce(fn, map(char2num, s))
</code></pre><p>还可以用lambda函数进一步简化成：</p>
<pre><code>from functools import reduce

def char2num(s):
    return {&#39;0&#39;: 0, &#39;1&#39;: 1, &#39;2&#39;: 2, &#39;3&#39;: 3, &#39;4&#39;: 4, &#39;5&#39;: 5, &#39;6&#39;: 6, &#39;7&#39;: 7, &#39;8&#39;: 8, &#39;9&#39;: 9}[s]

def str2int(s):
    return reduce(lambda x, y: x * 10 + y, map(char2num, s))
</code></pre><p>也就是说，假设Python没有提供<code>int()</code>函数，你完全可以自己写一个把字符串转化为整数的函数，而且只需要几行代码！</p>
<p>lambda函数的用法在后面介绍。</p>
<h3 id="-">练习</h3>
<p>利用<code>map()</code>函数，把用户输入的不规范的英文名字，变为首字母大写，其他小写的规范名字。输入：<code>[&#39;adam&#39;, &#39;LISA&#39;, &#39;barT&#39;]</code>，输出：<code>[&#39;Adam&#39;, &#39;Lisa&#39;, &#39;Bart&#39;]</code>：</p>
<pre class="x-python3">
# -*- coding: utf-8 -*-
----
def normalize(name):
    pass
----
# 测试:
L1 = ['adam', 'LISA', 'barT']
L2 = list(map(normalize, L1))
print(L2)
</pre>

<p>Python提供的<code>sum()</code>函数可以接受一个list并求和，请编写一个<code>prod()</code>函数，可以接受一个list并利用<code>reduce()</code>求积：</p>
<pre class="x-python3">
# -*- coding: utf-8 -*-

from functools import reduce

def prod(L):
----
    pass
----
print('3 * 5 * 7 * 9 =', prod([3, 5, 7, 9]))
</pre>

<p>利用<code>map</code>和<code>reduce</code>编写一个<code>str2float</code>函数，把字符串<code>&#39;123.456&#39;</code>转换成浮点数<code>123.456</code>：</p>
<pre class="x-python3">
# -*- coding: utf-8 -*-

from functools import reduce

def str2float(s):
----
    pass
----
print('str2float(\'123.456\') =', str2float('123.456'))
</pre>

<h3 id="-">参考代码</h3>
<p><a href="https://github.com/michaelliao/learn-python3/blob/master/samples/functional/do_map.py">do_map.py</a></p>
<p><a href="https://github.com/michaelliao/learn-python3/blob/master/samples/functional/do_reduce.py">do_reduce.py</a></p>

    