# TbMeishi
有些网页页面比较复杂，有各种请求参数，或加密参数。如果直接请求或分析ajax会非常繁琐。
selenium是一个自动化工具，可以驱动浏览器完成各种操作，比如点击，输入，下拉等。利用selenium，这样我们只关心操作，不用关心后台发生了怎样的请求。
PhantomJS是一个无界面浏览器。

1.利用selenium驱动浏览器搜索关键字，得到查询后的商品列表。
2.得到商品页码数，模拟翻页，得到后续页面的商品列表。
3.利用PyQuery分析源码，解析得到的商品信息。
4.将商品信息存储到数据库MongoDB中。
