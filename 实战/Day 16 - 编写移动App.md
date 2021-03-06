﻿
        <p>网站部署上线后，还缺点啥呢？</p>
<p>在移动互联网浪潮席卷而来的今天，一个网站没有上线移动App，出门根本不好意思跟人打招呼。</p>
<p>所以，<code>awesome-python3-webapp</code>必须得有一个移动App版本！</p>
<h3 id="-iphone-">开发iPhone版本</h3>
<p>我们首先来看看如何开发iPhone App。前置条件：一台Mac电脑，安装XCode和最新的iOS SDK。</p>
<p>在使用MVVM编写前端页面时，我们就能感受到，用REST API封装网站后台的功能，不但能清晰地分离前端页面和后台逻辑，现在这个好处更加明显，移动App也可以通过REST API从后端拿到数据。</p>
<p>我们来设计一个简化版的iPhone App，包含两个屏幕：列出最新日志和阅读日志的详细内容：</p>
<p><img src="../files/attachments/001402635871095b05d9bb6a9c64c3dbb9bdc94171bcd62000.jpg" alt="awesomepy-iphone-app"></p>
<p>只需要调用API：<code>/api/blogs</code>。</p>
<p>在XCode中完成App编写：</p>
<p><img src="../files/attachments/001402635955576dae7c85a76ab49e694dcba0574b1fd22000.jpg" alt="awesomepy-iphone-app-xcode"></p>
<p>由于我们的教程是Python，关于如何开发iOS，请移步<a href="https://developer.apple.com/technologies/ios/">Develop Apps for iOS</a>。</p>
<p><a href="https://github.com/michaelliao/awesome-python3-webapp/tree/day-16/ios">点击下载iOS App源码</a>。</p>
<p>如何编写Android App？这个当成作业了。</p>
<h3 id="-">参考源码</h3>
<p><a href="https://github.com/michaelliao/awesome-python3-webapp/tree/day-16">day-16</a></p>

    