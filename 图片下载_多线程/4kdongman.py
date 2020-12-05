from functools import reduce
from lxml import etree
import requests
from multiprocessing.dummy import Pool
import os

# 创建文件夹
if not os.path.exists('./output'):
    os.mkdir('./output')
# 所有页数的url
url = 'http://pic.netbian.com/4kdongman/'
url_list = [url] + [url + 'index_' + str(i) + '.html' for i in range(2, 147)]
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/86.0.4240.198 Safari/537.36',
}


def save_img(dic):
    try:
        url = dic['src']
        file_path = './output/' + dic['name']
        content = requests.get(url=url, headers=headers).content
        with open(file_path, 'wb') as fp:
            fp.write(content)
            print('保存》》' + dic['name'] + '《《成功')
    except:
        print('保存失败')


def get_images(url):
    try:
        # 一页的返回内容
        page_text = requests.get(url=url, headers=headers).text
        # 加载返回内容
        tree = etree.HTML(page_text)
        # 所有li标签
        li_list = tree.xpath('//ul[@class="clearfix"]/li')
        images = []
        for li in li_list:
            img_src = 'http://pic.netbian.com/' + li.xpath('./a/img/@src')[0]
            name = li.xpath('./a/img/@alt')[0] + '.jpg'
            dic = {
                'src': img_src,
                'name': name.encode('iso-8859-1').decode('gbk')
            }
            images.append(dic)
        return images
    except:
        print('url获取失败')


# 创建线程池
pool = Pool(8)
# 多线程获取图片url
image = pool.map(get_images, url_list)
# 或得图片url列表
images = reduce(lambda x, y: x + y, image)
# 多线程保存图片
pool.map(save_img, images)
# 关闭线程池
pool.close()
pool.join()
