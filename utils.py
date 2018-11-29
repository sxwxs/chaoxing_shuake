import os
import time
import json
import math
import socket
import random 

import selenium


def switch_to_video_frame(driver):
    driver.switch_to.frame(driver.find_elements_by_tag_name('iframe')[0])
    driver.switch_to.frame(driver.find_elements_by_tag_name('iframe')[0])

def start_play(driver):
    switch_to_video_frame(driver)
    # click play button in the center of the screen
    driver.find_element_by_xpath('//*[@id="video"]/button').click()
    driver.switch_to.default_content()

def reseum(driver):
    switch_to_video_frame(driver)
    # click play button in the control panel
    driver.find_element_by_xpath('//*[@id="video"]/div[4]/button[1]').click()
    driver.switch_to.default_content()

def recv_until_nl(s):
    # recive from socket byte by byte until \n
    text = b''
    while True:
        ch = ''
        while len(ch) == 0:
                ch = s.recv(1)
        if ch == b'\n':
                return text.decode('utf8')
        text += ch
                
def ans_question(driver):
    switch_to_video_frame(driver)
    # get question title element
    question_title_element = driver.find_element_by_xpath('//div[@class="ans-videoquiz-title"]')
    question = question_title_element.text
    print(question)
    options = []
    uls = question_title_element.parent.find_elements_by_tag_name('ul')
    for ul in uls:
        # find options list
        if 'ans-videoquiz-opts' in ul.get_attribute('class'):
            break
    if 'ans-videoquiz-opts' not in ul.get_attribute('class'):
        raise Exception('error can not find options')
    lis = ul.find_elements_by_tag_name('li')
    for li in lis:
        options.append(li.text)
    s = socket.socket()
    s.connect(('as.codeplot.top', 1507))
    s.send((question.replace('\n', '\\n')+'\n').encode('utf8'))
    ans = int(recv_until_nl(s))
    s.close()
    if ans == -1: # -1 
        ans = 0
        while ans < len(lis):
            time.sleep(random.randint(2,9))
            lis[ans].find_element_by_tag_name('label').click()
            driver.find_elements_by_class_name('ans-videoquiz-submit')[0].click()
            time.sleep(1)
            try:
                alertx = driver.switch_to.alert
                alertx.accept()
                # wrong ans
            except selenium.common.exceptions.NoAlertPresentException:
                s = socket.socket()
                s.connect(('as.codeplot.top', 1507))
                s.send((json.dumps({'question': question.replace('\n', '\\n'), 'options': options, 'ans': ans}) + '\n').encode('utf8'))
                s.close()
                break
            ans += 1
    else:
        lis[ans].find_element_by_tag_name('label').click()
        time.sleep(random.randint(2,9))
        driver.find_elements_by_class_name('ans-videoquiz-submit')[0].click()
    f = open('question.jsonl', 'a')
    f.write(json.dumps({'question': question, 'options': options, 'ans': ans})+'\n')
    f.close()
    driver.switch_to.default_content()
    #alert.text == '回答有错误'
    #alert.accept()

def get_video_duration(driver):
    switch_to_video_frame(driver)
    vd = driver.find_elements_by_xpath('//*[@id="video_html5_api"]')
    duration = vd[0].get_attribute('duration')
    driver.switch_to.default_content()
    return duration


def get_video_curTime(driver):
    switch_to_video_frame(driver)
    vd = driver.find_elements_by_xpath('//*[@id="video_html5_api"]')
    curTime = vd[0].get_attribute('currentTime')
    driver.switch_to.default_content()
    return curTime

def play_loop(driver):
    start_play(driver)
    time.sleep(2)
    cur_duration = float(get_video_duration(driver))
    print (cur_duration / 60, 'min')
    flag = False
    last_time = 0
    while True:
        if math.isnan(cur_duration):
            cur_duration = float(get_video_duration(driver))
        time.sleep(10)
        cur_time = float(get_video_curTime(driver))
        if cur_time + 1 >= cur_duration:
            return
        if cur_time > last_time:
            flag = False
            last_time = cur_time
            lt = time.localtime()
            print ('%d-%d-%d %d:%d --  %f %%'%(lt.tm_year, lt.tm_mon, lt.tm_mday, lt.tm_hour, lt.tm_min, cur_time*100.0 / cur_duration))
        else:
            if flag:
                ans_question(driver)
            else:
                try:
                    reseum(driver)
                except selenium.common.exceptions.WebDriverException:
                    driver.switch_to.default_content()
                flag = True

def get_cur_title(driver):
    driver.switch_to.default_content()
    return driver.find_element_by_xpath('//*[@id="mainid"]/h1').text