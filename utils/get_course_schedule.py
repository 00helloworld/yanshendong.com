from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import time
import pytz
import sqlite3

def get_wp_time():
    # 获取温尼伯的时区
    winnipeg_tz = pytz.timezone('America/Winnipeg')

    # 获取当前时间戳
    current_timestamp = time.time()

    # 将时间戳转换为本地时间
    current_local_time = time.localtime(current_timestamp)

    # 将本地时间转换为温尼伯时区的时间
    # current_winnipeg_time = pytz.utc.localize(time.strftime('%Y-%m-%d %H:%M', current_local_time)).astimezone(winnipeg_tz)
    current_winnipeg_time = time.strftime("%Y%m%d: %H:%M", current_local_time)

    return current_winnipeg_time


def get_all_dues():
    due_date_infos = []
    url = 'https://nexus.uwinnipeg.ca/d2l/login?logout=1'

    options = webdriver.ChromeOptions()
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.6261.69 Safari/537.36")
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_argument('--headless')  # 启用 Headless 模式
    options.add_argument('--disable-gpu')

    # 创建一个 WebDriver 对象
    driver = webdriver.Chrome(options=options)  # 这里假设你使用 Chrome 浏览器，需要安装相应的 WebDriver

    # 打开登录页面
    driver.get(url)

    time.sleep(3)

    # 找到用户名和密码输入框，并输入对应的值
    username_input = driver.find_element('id', 'userName')
    username_input.send_keys('dong-y38')

    pass_input = driver.find_element('id', 'password')
    pass_input.send_keys('Dd775852174110%')

    print(username_input)
    print(pass_input)

    # 提交表单
    pass_input.send_keys(Keys.RETURN)

    time.sleep(5)
    # 将页面 HTML 内容保存到文件
    with open('response.html', 'w', encoding='utf-8') as file:
        file.write(driver.page_source)

    # 找到课程列表
    button = driver.find_element(By.CLASS_NAME, 'd2l-navigation-s-course-menu')
    # 使用 ActionChains 来点击元素的中心
    actions = ActionChains(driver)
    actions.move_to_element(button).click().perform()

    time.sleep(3)

    course_ul = driver.find_element(By.CLASS_NAME, 'd2l-datalist')
    course_ul = driver.find_element(By.XPATH, '/html/body/div[1]/header/nav/d2l-navigation/d2l-navigation-main-header/div[2]/div[1]/d2l-navigation-dropdown-button-icon/d2l-dropdown-content/div/div/div[1]/div/ul')
    # 找到 ul 元素下的所有 li 元素
    li_elements = course_ul.find_elements(By.TAG_NAME, 'li')

    # 遍历 li 元素并输出文本内容
    course_urls = []

    for li in li_elements:
        a = li.find_element(By.TAG_NAME, 'a')
        print(a.get_attribute('href'))
        course_url = a.get_attribute('href')
        course_urls.append(course_url)


    
    for course_url in course_urls:
        print(course_url)
        course_code = course_url.split('/')[-1]
        content_url = f'https://nexus.uwinnipeg.ca/d2l/le/content/{course_code}/Home'
        driver.get(content_url)
        time.sleep(2)

        # 获取 <title> 元素的文本内容
        course_title_ = driver.find_element(By.XPATH, '/html/body/header/nav/d2l-navigation/d2l-navigation-main-header/div[1]/div[2]/div/a')
        course_title = course_title_.text
        print(course_title)

        # 点击schedule
        schedule_div_xpath = '/html/body/div[3]/div/div[1]/div[2]/div[1]/div/ul[1]/li[3]/a/div/div/div/div[1]/div/div[1]'
        schedule_div = driver.find_element(By.XPATH, schedule_div_xpath)
        # 使用 ActionChains 来点击元素的中心
        actions = ActionChains(driver)
        actions.move_to_element(schedule_div).click().perform()

        time.sleep(3)

        full_schedule_xpath = '/html/body/div[3]/div/div[2]/div/div/div[3]/div[1]/div/div/ul/li[2]/a'
        full_schedule_a = driver.find_element(By.XPATH, full_schedule_xpath)
        # 使用 ActionChains 来点击元素的中心
        actions = ActionChains(driver)
        actions.move_to_element(full_schedule_a).click().perform()
        time.sleep(1)
        actions.move_to_element(full_schedule_a).click().perform()
        time.sleep(1)
        actions.move_to_element(full_schedule_a).click().perform()
        time.sleep(5) # 等待一下加载
        # 展开日期详情
        schedule_list_div_xpath = '/html/body/div[3]/div/div[2]/div/div/div[3]/div[3]/div/div/ul/li/div[1]/div'
        schedule_list_div_xpath = '/html/body/div[3]/div/div[2]/div/div/div[3]/div[3]/div/div/ul/li/div[1]/div'
        
        schedule_list_div = driver.find_element(By.XPATH, schedule_list_div_xpath)
        due_date_div_class = './div'
        due_date_divs = schedule_list_div.find_elements(By.XPATH, due_date_div_class)
        print(len(due_date_divs))

        for due_date_div in due_date_divs:
            # 点击展开日期详情
            actions = ActionChains(driver)
            actions.move_to_element(due_date_div).click().perform()
            time.sleep(2)

            # 日期
            panel_element = due_date_div.find_element(By.XPATH, ".//d2l-collapsible-panel")
            # 获取 panel-title 属性值
            date_text = panel_element.get_attribute('panel-title')
            print(date_text)
            time.sleep(2)

            content_li_elements = due_date_div.find_elements(By.XPATH, ".//li")
            for content in content_li_elements:
                # 找到 h2 元素并获取其文本内容
                due_title_h2 = content.find_element(By.XPATH, ".//h2")
                due_title = due_title_h2.text
                print(due_title)

                # 找到包含 data-date 属性的元素并获取其 data-date 属性值 abbr不一定存在
                due_timestamp = 0
                try:
                    timestamp_abbr = content.find_element(By.XPATH, ".//abbr")
                    due_timestamp = timestamp_abbr.get_attribute("data-date")
                    print(due_timestamp)
                except:
                    print('abbr does not exist')

                due_item = {
                    'course_code': course_code,
                    'course_title': course_title,
                    'due_date_text': date_text,
                    'due_title': due_title,
                    'due_timestamp': due_timestamp,
                    'content_url': content_url,
                    'update_time': get_wp_time()
                }
                due_date_infos.append(due_item)

            print('done')
            time.sleep(2)

        for i in due_date_infos:
            print(i)
    
    return due_date_infos
        

def insert_table(data):
    # 连接到 SQLite 数据库
    conn = sqlite3.connect('course.db')

    # 创建一个游标对象
    cur = conn.cursor()

    # 创建 course_dues 表（如果不存在）
    cur.execute('''CREATE TABLE IF NOT EXISTS course_dues
                (id INTEGER PRIMARY KEY AUTOINCREMENT,
                    batch_id INTEGER,
                    course_code TEXT,
                    course_title TEXT,
                    due_date_text TEXT,
                    due_title TEXT,
                    due_timestamp TEXT,
                    content_url TEXT,
                    update_time TEXT)''')

    # 查询当前数据库中 batch_id 的最大值
    cur.execute("SELECT MAX(batch_id) FROM course_dues")
    max_batch_id = cur.fetchone()[0]

    # 设置初始的 batch_id
    if max_batch_id is None:
        batch_id = 1
    else:
        batch_id = max_batch_id + 1

    # 将数据插入数据库
    for due in data:
        cur.execute('''INSERT INTO course_dues (batch_id, course_code, course_title, due_date_text, due_title, due_timestamp, content_url, update_time)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)''',
                    (batch_id, due['course_code'], due['course_title'], due['due_date_text'], due['due_title'],
                    due['due_timestamp'], due['content_url'], due['update_time']))

    # 提交事务
    conn.commit()

    # 关闭数据库连接
    conn.close()


def main():
    data = get_all_dues()
    insert_table(data)
    # try:
    #     data = get_all_dues()
    # except:
    #     print('****************** get_all_dues() Error ******************')
    #     return 1
    
    # try:
    #     insert_table(data)
    # except:
    #     print('****************** insert_table() Error ******************')
    #     return 2
    
    return 0

if __name__ == '__main__':

    main()

    # schedule.every().hour.do(main)
    # while True:
    #     schedule.run_pending()
    #     time.sleep(10)