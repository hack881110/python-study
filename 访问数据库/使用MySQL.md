﻿
        <p>MySQL是Web世界中使用最广泛的数据库服务器。SQLite的特点是轻量级、可嵌入，但不能承受高并发访问，适合桌面和移动应用。而MySQL是为服务器端设计的数据库，能承受高并发访问，同时占用的内存也远远大于SQLite。</p>
<p>此外，MySQL内部有多种数据库引擎，最常用的引擎是支持数据库事务的InnoDB。</p>
<h3 id="-mysql">安装MySQL</h3>
<p>可以直接从MySQL官方网站下载最新的<a href="http://dev.mysql.com/downloads/mysql/5.6.html">Community Server 5.6.x</a>版本。MySQL是跨平台的，选择对应的平台下载安装文件，安装即可。</p>
<p>安装时，MySQL会提示输入<code>root</code>用户的口令，请务必记清楚。如果怕记不住，就把口令设置为<code>password</code>。</p>
<p>在Windows上，安装时请选择<code>UTF-8</code>编码，以便正确地处理中文。</p>
<p>在Mac或Linux上，需要编辑MySQL的配置文件，把数据库默认的编码全部改为UTF-8。MySQL的配置文件默认存放在<code>/etc/my.cnf</code>或者<code>/etc/mysql/my.cnf</code>：</p>
<pre><code>[client]
default-character-set = utf8

[mysqld]
default-storage-engine = INNODB
character-set-server = utf8
collation-server = utf8_general_ci
</code></pre><p>重启MySQL后，可以通过MySQL的客户端命令行检查编码：</p>
<pre><code>$ mysql -u root -p
Enter password: 
Welcome to the MySQL monitor...
...

mysql&gt; show variables like &#39;%char%&#39;;
+--------------------------+--------------------------------------------------------+
| Variable_name            | Value                                                  |
+--------------------------+--------------------------------------------------------+
| character_set_client     | utf8                                                   |
| character_set_connection | utf8                                                   |
| character_set_database   | utf8                                                   |
| character_set_filesystem | binary                                                 |
| character_set_results    | utf8                                                   |
| character_set_server     | utf8                                                   |
| character_set_system     | utf8                                                   |
| character_sets_dir       | /usr/local/mysql-5.1.65-osx10.6-x86_64/share/charsets/ |
+--------------------------+--------------------------------------------------------+
8 rows in set (0.00 sec)
</code></pre><p>看到<code>utf8</code>字样就表示编码设置正确。</p>
<p><em>注</em>：如果MySQL的版本≥5.5.3，可以把编码设置为<code>utf8mb4</code>，<code>utf8mb4</code>和<code>utf8</code>完全兼容，但它支持最新的Unicode标准，可以显示emoji字符。</p>
<h3 id="-mysql-">安装MySQL驱动</h3>
<p>由于MySQL服务器以独立的进程运行，并通过网络对外服务，所以，需要支持Python的MySQL驱动来连接到MySQL服务器。MySQL官方提供了mysql-connector-python驱动，但是安装的时候需要给pip命令加上参数<code>--allow-external</code>：</p>
<pre><code>$ pip install mysql-connector-python --allow-external mysql-connector-python
</code></pre><p>如果上面的命令安装失败，可以试试另一个驱动：</p>
<pre><code>$ pip install mysql-connector
</code></pre><p>我们演示如何连接到MySQL服务器的test数据库：</p>
<pre><code># 导入MySQL驱动:
&gt;&gt;&gt; import mysql.connector
# 注意把password设为你的root口令:
&gt;&gt;&gt; conn = mysql.connector.connect(user=&#39;root&#39;, password=&#39;password&#39;, database=&#39;test&#39;)
&gt;&gt;&gt; cursor = conn.cursor()
# 创建user表:
&gt;&gt;&gt; cursor.execute(&#39;create table user (id varchar(20) primary key, name varchar(20))&#39;)
# 插入一行记录，注意MySQL的占位符是%s:
&gt;&gt;&gt; cursor.execute(&#39;insert into user (id, name) values (%s, %s)&#39;, [&#39;1&#39;, &#39;Michael&#39;])
&gt;&gt;&gt; cursor.rowcount
1
# 提交事务:
&gt;&gt;&gt; conn.commit()
&gt;&gt;&gt; cursor.close()
# 运行查询:
&gt;&gt;&gt; cursor = conn.cursor()
&gt;&gt;&gt; cursor.execute(&#39;select * from user where id = %s&#39;, (&#39;1&#39;,))
&gt;&gt;&gt; values = cursor.fetchall()
&gt;&gt;&gt; values
[(&#39;1&#39;, &#39;Michael&#39;)]
# 关闭Cursor和Connection:
&gt;&gt;&gt; cursor.close()
True
&gt;&gt;&gt; conn.close()
</code></pre><p>由于Python的DB-API定义都是通用的，所以，操作MySQL的数据库代码和SQLite类似。</p>
<h3 id="-">小结</h3>
<ul>
<li><p>执行INSERT等操作后要调用<code>commit()</code>提交事务；</p>
</li>
<li><p>MySQL的SQL占位符是<code>%s</code>。</p>
</li>
</ul>
<h3 id="-">参考源码</h3>
<p><a href="https://github.com/michaelliao/learn-python3/blob/master/samples/db/do_mysql.py">do_mysql.py</a></p>

    