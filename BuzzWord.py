import jieba
import collections
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from wordcloud import WordCloud
from imageio import imread
import matplotlib.pyplot as plt


class BuzzWord:
    def __init__(self):
        # 新浪滚动新闻
        self.url = 'https://news.sina.com.cn/roll/#pageid=153&lid=2509&k=&num=50&page='
        self.newsList = ""  # 全部的新闻标题
        self.top10Words = []  # 词频前10的词
        self.stopwords = [line.strip() for line in open(  # 停用字
            'BuzzwordTracking/StopWords.txt', encoding='utf-8').readlines()] + [u' ']

    def getNewsTitle(self, Page=20):  # 获取全部新闻标题，默认获取20页的新闻标题
        # 模拟人的自动化访问
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--headless')
        browser = webdriver.Chrome(options=chrome_options)
        for i in range(1, Page+1):  # 循环获取每页的所有新闻标题
            try:
                print('Get Page%d' % i)
                browser.get(self.url+str(i))
                browser.refresh()
                newsTitle = browser.find_elements_by_xpath(
                    '//*[@id="d_list"]/ul/li/span/a')
                for title in newsTitle:
                    self.newsList = self.newsList + str(title.text)
            except NoSuchElementException:
                print('NoSuchElementException')
                browser.close()
                continue
        browser.quit()

    def countBuzzword(self):  # 热词词频统计
        allWordList = jieba.cut(self.newsList, cut_all=False)
        words = []
        for word in allWordList:  # 循环读出每个词
            if word not in self.stopwords:  # 不在停用词中
                words.append(word)  # 追加到列表
        word_counts = collections.Counter(words)  # 对分词做词频统计
        self.top10Words = word_counts.most_common(10)  # 前10高频的词
        print(self.top10Words)

    def getWordCloud(self):  # 使用wordcloud将热词可视化
        background = imread("BuzzwordTracking/apple.jpg")
        allWordList = jieba.cut(self.newsList, cut_all=False)
        joinedWords = " /".join(allWordList)
        # 设置词云相关参数
        word_cloud = WordCloud(
            background_color="white",
            max_words=200,
            mask=background,
            # 添加停用词库
            stopwords=self.stopwords,
            # 设置中文字体
            font_path="BuzzwordTracking/SimHei.ttf",
            max_font_size=500,
            random_state=40,
            contour_width=3,
            contour_color='blue',
        )
        wordCloudPicture = word_cloud.generate(joinedWords)  # 生成词云
        # 显示词云图片
        plt.title('BuzzWords Tracking')
        plt.imshow(wordCloudPicture)
        plt.axis("off")
        plt.show()


if __name__ == '__main__':
    buzzword = BuzzWord()
    buzzword.getNewsTitle()
    buzzword.countBuzzword()
    buzzword.getWordCloud()
