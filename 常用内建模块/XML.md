﻿
        <p>XML虽然比JSON复杂，在Web中应用也不如以前多了，不过仍有很多地方在用，所以，有必要了解如何操作XML。</p>
<h3 id="dom-vs-sax">DOM vs SAX</h3>
<p>操作XML有两种方法：DOM和SAX。DOM会把整个XML读入内存，解析为树，因此占用内存大，解析慢，优点是可以任意遍历树的节点。SAX是流模式，边读边解析，占用内存小，解析快，缺点是我们需要自己处理事件。</p>
<p>正常情况下，优先考虑SAX，因为DOM实在太占内存。</p>
<p>在Python中使用SAX解析XML非常简洁，通常我们关心的事件是<code>start_element</code>，<code>end_element</code>和<code>char_data</code>，准备好这3个函数，然后就可以解析xml了。</p>
<p>举个例子，当SAX解析器读到一个节点时：</p>
<pre><code>&lt;a href=&quot;/&quot;&gt;python&lt;/a&gt;
</code></pre><p>会产生3个事件：</p>
<ol>
<li><p>start_element事件，在读取<code>&lt;a href=&quot;/&quot;&gt;</code>时；</p>
</li>
<li><p>char_data事件，在读取<code>python</code>时；</p>
</li>
<li><p>end_element事件，在读取<code>&lt;/a&gt;</code>时。</p>
</li>
</ol>
<p>用代码实验一下：</p>
<pre><code>from xml.parsers.expat import ParserCreate

class DefaultSaxHandler(object):
    def start_element(self, name, attrs):
        print(&#39;sax:start_element: %s, attrs: %s&#39; % (name, str(attrs)))

    def end_element(self, name):
        print(&#39;sax:end_element: %s&#39; % name)

    def char_data(self, text):
        print(&#39;sax:char_data: %s&#39; % text)

xml = r&#39;&#39;&#39;&lt;?xml version=&quot;1.0&quot;?&gt;
&lt;ol&gt;
    &lt;li&gt;&lt;a href=&quot;/python&quot;&gt;Python&lt;/a&gt;&lt;/li&gt;
    &lt;li&gt;&lt;a href=&quot;/ruby&quot;&gt;Ruby&lt;/a&gt;&lt;/li&gt;
&lt;/ol&gt;
&#39;&#39;&#39;

handler = DefaultSaxHandler()
parser = ParserCreate()
parser.StartElementHandler = handler.start_element
parser.EndElementHandler = handler.end_element
parser.CharacterDataHandler = handler.char_data
parser.Parse(xml)
</code></pre><p>需要注意的是读取一大段字符串时，<code>CharacterDataHandler</code>可能被多次调用，所以需要自己保存起来，在<code>EndElementHandler</code>里面再合并。</p>
<p>除了解析XML外，如何生成XML呢？99%的情况下需要生成的XML结构都是非常简单的，因此，最简单也是最有效的生成XML的方法是拼接字符串：</p>
<pre><code>L = []
L.append(r&#39;&lt;?xml version=&quot;1.0&quot;?&gt;&#39;)
L.append(r&#39;&lt;root&gt;&#39;)
L.append(encode(&#39;some &amp; data&#39;))
L.append(r&#39;&lt;/root&gt;&#39;)
return &#39;&#39;.join(L)
</code></pre><p>如果要生成复杂的XML呢？建议你不要用XML，改成JSON。</p>
<h3 id="-">小结</h3>
<p>解析XML时，注意找出自己感兴趣的节点，响应事件时，把节点数据保存起来。解析完毕后，就可以处理数据。</p>
<h3 id="-">练习</h3>
<p>请利用SAX编写程序解析Yahoo的XML格式的天气预报，获取当天和第二天的天气：</p>
<p><a href="http://weather.yahooapis.com/forecastrss?u=c&amp;w=2151330">http://weather.yahooapis.com/forecastrss?u=c&amp;w=2151330</a></p>
<p>参数<code>w</code>是城市代码，要查询某个城市代码，可以在<a href="https://weather.yahoo.com/">weather.yahoo.com</a>搜索城市，浏览器地址栏的URL就包含城市代码。</p>
<pre class="x-python3">
# -*- coding:utf-8 -*-

from xml.parsers.expat import ParserCreate
----
class WeatherSaxHandler(object):
    pass

def parse_weather(xml):
    return {
        'city': 'Beijing',
        'country': 'China',
        'today': {
            'text': 'Partly Cloudy',
            'low': 20,
            'high': 33
        },
        'tomorrow': {
            'text': 'Sunny',
            'low': 21,
            'high': 34
        }
    }
----
# 测试:
data = r'''&lt;?xml version="1.0" encoding="UTF-8" standalone="yes" ?&gt;
&lt;rss version="2.0" xmlns:yweather="http://xml.weather.yahoo.com/ns/rss/1.0" xmlns:geo="http://www.w3.org/2003/01/geo/wgs84_pos#"&gt;
    &lt;channel&gt;
        &lt;title&gt;Yahoo! Weather - Beijing, CN&lt;/title&gt;
        &lt;lastBuildDate&gt;Wed, 27 May 2015 11:00 am CST&lt;/lastBuildDate&gt;
        &lt;yweather:location city="Beijing" region="" country="China"/&gt;
        &lt;yweather:units temperature="C" distance="km" pressure="mb" speed="km/h"/&gt;
        &lt;yweather:wind chill="28" direction="180" speed="14.48" /&gt;
        &lt;yweather:atmosphere humidity="53" visibility="2.61" pressure="1006.1" rising="0" /&gt;
        &lt;yweather:astronomy sunrise="4:51 am" sunset="7:32 pm"/&gt;
        &lt;item&gt;
            &lt;geo:lat&gt;39.91&lt;/geo:lat&gt;
            &lt;geo:long&gt;116.39&lt;/geo:long&gt;
            &lt;pubDate&gt;Wed, 27 May 2015 11:00 am CST&lt;/pubDate&gt;
            &lt;yweather:condition text="Haze" code="21" temp="28" date="Wed, 27 May 2015 11:00 am CST" /&gt;
            &lt;yweather:forecast day="Wed" date="27 May 2015" low="20" high="33" text="Partly Cloudy" code="30" /&gt;
            &lt;yweather:forecast day="Thu" date="28 May 2015" low="21" high="34" text="Sunny" code="32" /&gt;
            &lt;yweather:forecast day="Fri" date="29 May 2015" low="18" high="25" text="AM Showers" code="39" /&gt;
            &lt;yweather:forecast day="Sat" date="30 May 2015" low="18" high="32" text="Sunny" code="32" /&gt;
            &lt;yweather:forecast day="Sun" date="31 May 2015" low="20" high="37" text="Sunny" code="32" /&gt;
        &lt;/item&gt;
    &lt;/channel&gt;
&lt;/rss&gt;
'''
weather = parse_weather(data)
assert weather['city'] == 'Beijing', weather['city']
assert weather['country'] == 'China', weather['country']
assert weather['today']['text'] == 'Partly Cloudy', weather['today']['text']
assert weather['today']['low'] == 20, weather['today']['low']
assert weather['today']['high'] == 33, weather['today']['high']
assert weather['tomorrow']['text'] == 'Sunny', weather['tomorrow']['text']
assert weather['tomorrow']['low'] == 21, weather['tomorrow']['low']
assert weather['tomorrow']['high'] == 34, weather['tomorrow']['high']
print('Weather:', str(weather))
</pre>

<h3 id="-">参考源码</h3>
<p><a href="https://github.com/michaelliao/learn-python3/blob/master/samples/commonlib/use_sax.py">use_sax.py</a></p>

    