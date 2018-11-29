from selenium import webdriver, common
import time
from utils import play_loop, get_cur_title

#def main():
if True:
    prefs = {
        "profile.default_content_setting_values.plugins": 1,
        "profile.content_settings.plugin_whitelist.adobe-flash-player": 1,
        "profile.content_settings.exceptions.plugins.*,*.per_resource.adobe-flash-player": 1,
        "PluginsAllowedForUrls": "https://chaoxing.com"
    }
    options = webdriver.ChromeOptions()
    # options.add_argument('--headless')
    # options.add_argument('--disable-gpu')
    options.add_experimental_option("prefs", prefs)
    driver = webdriver.Chrome(chrome_options=options)
    raw_cookie = ''
    try:
        driver.set_window_size(1920, 1080)
    except common.exceptions.WebDriverException:
        pass
    driver.get('http://passport2.chaoxing.com/login?fid=22169&refer=http://i.mooc.chaoxing.com')
    print ('========================')
    print ('请手动登陆，进入学习页面，然后按回车继续，窗口可能会自动切换')
    print ('========================')
    input("")
    # change to course window
    for x in driver.window_handles:
        driver.switch_to.window(x)
        if driver.title == '学习进度页面':
            break
    driver.switch_to.default_content()
    time.sleep(2)
    # get course list and print it
    lsx = driver.find_elements_by_class_name('ncells')

    time.sleep(1)
    i = 0
    
    try:
        for l in lsx:
            print ('[', i, ']', l.text)
            #time.sleep(0.1)
            i += 1
        i = int(input('请输入接下来需要观看的课程编号（方括号内的数字）:'))
    except selenium.common.exceptions.StaleElementReferenceException:
        print ('错误，无法打印课程列表')
        while True:
            i = int(input('请输入0-%d的数字我们将跳到那个课程的页面，你可以确认那是否是你要观看的课程:'%len(lsx)-1))
            lsx = driver.find_elements_by_class_name('ncells')
            lsx[i].click()
            ch = input('从当前课程开始播放?(y/N):')
            if ch.lower() == 'y':
                break
    while i < len(lsx):
        driver.switch_to.default_content()
        lsx = driver.find_elements_by_class_name('ncells')
        # go to current course page
        lsx[i].click()
        time.sleep(3)
        # play video and answer question in video
        play_loop(driver)
        print (get_cur_title(driver), '结束')
        i += 1
    print ('全部视频结束')
