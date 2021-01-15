from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import jieba
from wordcloud import WordCloud
from imageio import imread
import matplotlib.pyplot as plt


def getSinaNews(pages):
    # 要爬取的网页
    url = 'https://news.sina.com.cn/roll/'
    # 获取无界面浏览器
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    browser = webdriver.Chrome(options=chrome_options)
    # 爬
    news_list = ''
    while pages > 0:
        try:
            browser.get(url)
            news = browser.find_elements_by_xpath(
                '//*[@id="d_list"]/ul/li/span/a')
            # 将爬取到的所有新闻标题放到一个String中
            for i in news:
                news_list = news_list + str(i.text)
        except NoSuchElementException:
            print('NoSuchElementException')
            browser.close()
            continue
        # 找到下一页按钮，并点击
        browser.find_element_by_xpath('//*[@id="d_list"]/div/span/a').click()
        pages = pages - 1

    browser.quit()
    return news_list


def createWordCloud(news_list):  # 词云，热词可视化
    bg_image = imread("BuzzwordTracking/apple.jpg")
    stopwords = [line.strip() for line in open(
        'BuzzwordTracking/StopWords.txt', encoding='utf-8').readlines()]
    mytext = jieba.cut(news_list, cut_all=False)
    wt = " /".join(mytext)
    # 设置词云相关参数
    word_cloud = WordCloud(
        # 设置背景颜色
        background_color="white",
        # 设置最大显示的字数
        max_words=200,
        # 设置背景图片
        mask=bg_image,
        # 此处添加停用词库
        stopwords=stopwords,
        # 设置中文字体，词云默认字体是“DroidSansMono.ttf字体库”，不支持中文
        font_path="BuzzwordTracking/SimHei.ttf",
        # 设置字体最大值
        max_font_size=500,
        # 设置有多少种随机生成状态，即有多少种配色方案
        random_state=30,
        # 轮廓线宽度
        contour_width=3,
        # 轮廓线颜色
        contour_color='steelblue',
    )
    mycloud = word_cloud.generate(wt)  # 生成词云

    # 设置生成图片的标题
    plt.title('WordCloudOfSina')  # 必须得用英文，否则报错且不显示
    plt.imshow(mycloud)
    # 设置是否显示 X、Y 轴的下标
    plt.axis("off")
    plt.show()


if __name__ == '__main__':
    page = eval(input('请输入要爬取的页面数量：'))
    news_list = getSinaNews(page)
    createWordCloud(news_list)
