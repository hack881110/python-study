﻿
        <p>collections是Python内建的一个集合模块，提供了许多有用的集合类。</p>
<h3 id="namedtuple">namedtuple</h3>
<p>我们知道<code>tuple</code>可以表示不变集合，例如，一个点的二维坐标就可以表示成：</p>
<pre><code>&gt;&gt;&gt; p = (1, 2)
</code></pre><p>但是，看到<code>(1, 2)</code>，很难看出这个<code>tuple</code>是用来表示一个坐标的。</p>
<p>定义一个class又小题大做了，这时，<code>namedtuple</code>就派上了用场：</p>
<pre><code>&gt;&gt;&gt; from collections import namedtuple
&gt;&gt;&gt; Point = namedtuple(&#39;Point&#39;, [&#39;x&#39;, &#39;y&#39;])
&gt;&gt;&gt; p = Point(1, 2)
&gt;&gt;&gt; p.x
1
&gt;&gt;&gt; p.y
2
</code></pre><p><code>namedtuple</code>是一个函数，它用来创建一个自定义的<code>tuple</code>对象，并且规定了<code>tuple</code>元素的个数，并可以用属性而不是索引来引用<code>tuple</code>的某个元素。</p>
<p>这样一来，我们用<code>namedtuple</code>可以很方便地定义一种数据类型，它具备tuple的不变性，又可以根据属性来引用，使用十分方便。</p>
<p>可以验证创建的<code>Point</code>对象是<code>tuple</code>的一种子类：</p>
<pre><code>&gt;&gt;&gt; isinstance(p, Point)
True
&gt;&gt;&gt; isinstance(p, tuple)
True
</code></pre><p>类似的，如果要用坐标和半径表示一个圆，也可以用<code>namedtuple</code>定义：</p>
<pre><code># namedtuple(&#39;名称&#39;, [属性list]):
Circle = namedtuple(&#39;Circle&#39;, [&#39;x&#39;, &#39;y&#39;, &#39;r&#39;])
</code></pre><h3 id="deque">deque</h3>
<p>使用<code>list</code>存储数据时，按索引访问元素很快，但是插入和删除元素就很慢了，因为<code>list</code>是线性存储，数据量大的时候，插入和删除效率很低。</p>
<p>deque是为了高效实现插入和删除操作的双向列表，适合用于队列和栈：</p>
<pre><code>&gt;&gt;&gt; from collections import deque
&gt;&gt;&gt; q = deque([&#39;a&#39;, &#39;b&#39;, &#39;c&#39;])
&gt;&gt;&gt; q.append(&#39;x&#39;)
&gt;&gt;&gt; q.appendleft(&#39;y&#39;)
&gt;&gt;&gt; q
deque([&#39;y&#39;, &#39;a&#39;, &#39;b&#39;, &#39;c&#39;, &#39;x&#39;])
</code></pre><p><code>deque</code>除了实现list的<code>append()</code>和<code>pop()</code>外，还支持<code>appendleft()</code>和<code>popleft()</code>，这样就可以非常高效地往头部添加或删除元素。</p>
<h3 id="defaultdict">defaultdict</h3>
<p>使用<code>dict</code>时，如果引用的Key不存在，就会抛出<code>KeyError</code>。如果希望key不存在时，返回一个默认值，就可以用<code>defaultdict</code>：</p>
<pre><code>&gt;&gt;&gt; from collections import defaultdict
&gt;&gt;&gt; dd = defaultdict(lambda: &#39;N/A&#39;)
&gt;&gt;&gt; dd[&#39;key1&#39;] = &#39;abc&#39;
&gt;&gt;&gt; dd[&#39;key1&#39;] # key1存在
&#39;abc&#39;
&gt;&gt;&gt; dd[&#39;key2&#39;] # key2不存在，返回默认值
&#39;N/A&#39;
</code></pre><p>注意默认值是调用函数返回的，而函数在创建<code>defaultdict</code>对象时传入。</p>
<p>除了在Key不存在时返回默认值，<code>defaultdict</code>的其他行为跟<code>dict</code>是完全一样的。</p>
<h3 id="ordereddict">OrderedDict</h3>
<p>使用<code>dict</code>时，Key是无序的。在对<code>dict</code>做迭代时，我们无法确定Key的顺序。</p>
<p>如果要保持Key的顺序，可以用<code>OrderedDict</code>：</p>
<pre><code>&gt;&gt;&gt; from collections import OrderedDict
&gt;&gt;&gt; d = dict([(&#39;a&#39;, 1), (&#39;b&#39;, 2), (&#39;c&#39;, 3)])
&gt;&gt;&gt; d # dict的Key是无序的
{&#39;a&#39;: 1, &#39;c&#39;: 3, &#39;b&#39;: 2}
&gt;&gt;&gt; od = OrderedDict([(&#39;a&#39;, 1), (&#39;b&#39;, 2), (&#39;c&#39;, 3)])
&gt;&gt;&gt; od # OrderedDict的Key是有序的
OrderedDict([(&#39;a&#39;, 1), (&#39;b&#39;, 2), (&#39;c&#39;, 3)])
</code></pre><p>注意，<code>OrderedDict</code>的Key会按照插入的顺序排列，不是Key本身排序：</p>
<pre><code>&gt;&gt;&gt; od = OrderedDict()
&gt;&gt;&gt; od[&#39;z&#39;] = 1
&gt;&gt;&gt; od[&#39;y&#39;] = 2
&gt;&gt;&gt; od[&#39;x&#39;] = 3
&gt;&gt;&gt; list(od.keys()) # 按照插入的Key的顺序返回
[&#39;z&#39;, &#39;y&#39;, &#39;x&#39;]
</code></pre><p><code>OrderedDict</code>可以实现一个FIFO（先进先出）的dict，当容量超出限制时，先删除最早添加的Key：</p>
<pre><code>from collections import OrderedDict

class LastUpdatedOrderedDict(OrderedDict):

    def __init__(self, capacity):
        super(LastUpdatedOrderedDict, self).__init__()
        self._capacity = capacity

    def __setitem__(self, key, value):
        containsKey = 1 if key in self else 0
        if len(self) - containsKey &gt;= self._capacity:
            last = self.popitem(last=False)
            print(&#39;remove:&#39;, last)
        if containsKey:
            del self[key]
            print(&#39;set:&#39;, (key, value))
        else:
            print(&#39;add:&#39;, (key, value))
        OrderedDict.__setitem__(self, key, value)
</code></pre><h3 id="counter">Counter</h3>
<p><code>Counter</code>是一个简单的计数器，例如，统计字符出现的个数：</p>
<pre><code>&gt;&gt;&gt; from collections import Counter
&gt;&gt;&gt; c = Counter()
&gt;&gt;&gt; for ch in &#39;programming&#39;:
...     c[ch] = c[ch] + 1
...
&gt;&gt;&gt; c
Counter({&#39;g&#39;: 2, &#39;m&#39;: 2, &#39;r&#39;: 2, &#39;a&#39;: 1, &#39;i&#39;: 1, &#39;o&#39;: 1, &#39;n&#39;: 1, &#39;p&#39;: 1})
</code></pre><p><code>Counter</code>实际上也是<code>dict</code>的一个子类，上面的结果可以看出，字符<code>&#39;g&#39;</code>、<code>&#39;m&#39;</code>、<code>&#39;r&#39;</code>各出现了两次，其他字符各出现了一次。</p>
<h3 id="-">小结</h3>
<p><code>collections</code>模块提供了一些有用的集合类，可以根据需要选用。</p>
<h3 id="-">参考源码</h3>
<p><a href="https://github.com/michaelliao/learn-python3/blob/master/samples/commonlib/use_collections.py">use_collections.py</a></p>

    