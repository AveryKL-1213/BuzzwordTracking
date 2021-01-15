import jieba
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from wordcloud import WordCloud
from imageio import imread
import matplotlib.pyplot as plt
import collections


class BuzzWord:
    def __init__(self):
        # 新浪滚动新闻
        self.url = 'https://news.sina.com.cn/roll/#pageid=153&lid=2509&k=&num=50&page='
        self.newsList = ""
        self.top10Words = []
        self.stopwords = [line.strip() for line in open(
            'BuzzwordTracking/StopWords.txt', encoding='utf-8').readlines()] + [u' ']

    def getNewsTitle(self, Page=20):  # 获取全部新闻标题，默认获取20页的新闻标题
        # 模拟人的自动化访问
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--headless')
        browser = webdriver.Chrome(options=chrome_options)
        while Page > 0:
            try:
                print(self.url+str(21-Page))
                browser.get(self.url+str(21-Page))
                browser.refresh()
                newsTitle = browser.find_elements_by_xpath(
                    '//*[@id="d_list"]/ul/li/span/a')
                for i in newsTitle:
                    self.newsList = self.newsList + str(i.text)
            except NoSuchElementException:
                print('NoSuchElementException')
                browser.close()
                continue
            Page -= 1
        browser.quit()
        return self.newsList

    def wordCount(self):  # 词频统计
        allWordList = jieba.cut(self.newsList, cut_all=False)
        words = []
        for word in allWordList:  # 循环读出每个分词
            if word not in self.stopwords:  # 如果不在去除词库中
                words.append(word)  # 分词追加到列表
        word_counts = collections.Counter(words)  # 对分词做词频统计
        self.top10Words = word_counts.most_common(10)  # 获取前10最高频的词
        print(self.top10Words)  # 输出检查

    def getWordCloud(self):  # 使用wordcloud将热词可视化
        background = imread("BuzzwordTracking/apple.jpg")
        allWordList = jieba.cut(self.newsList, cut_all=False)
        wt = " /".join(allWordList)
        # 设置词云相关参数
        word_cloud = WordCloud(
            # 设置背景颜色
            background_color="white",
            # 设置最大显示的字数
            max_words=200,
            # 设置背景图片
            mask=background,
            # 此处添加停用词库
            stopwords=self.stopwords,
            # 设置中文字体
            font_path="BuzzwordTracking/SimHei.ttf",
            # 设置字体最大值
            max_font_size=500,
            # 设置有多少种随机生成状态，即有多少种配色方案
            random_state=40,
            # 轮廓线宽度
            contour_width=3,
            # 轮廓线颜色
            contour_color='steelblue',
        )
        mycloud = word_cloud.generate(wt)  # 生成词云

        # 设置生成图片的标题
        plt.title('BuzzWords Tracking')
        plt.imshow(mycloud)
        # 设置是否显示 X、Y 轴的下标
        plt.axis("off")
        plt.show()


if __name__ == '__main__':
    buzzword = BuzzWord()
    buzzword.getNewsTitle()
    buzzword.wordCount()
    buzzword.getWordCloud()
