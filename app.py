from flask import Flask, render_template, redirect
import sqlite3
from datetime import datetime

app = Flask(__name__)

@app.route('/')
def HomePage():
    return render_template('HomePage.html')


@app.route('/resume')
def show_resume():  # inline with the 'show_resume' of jinja href="{{ url_for('show_resume')}}"
    return render_template('resume.html')


@app.route('/projects')
def show_projects():  # inline with the 'show_resume' of jinja href="{{ url_for('show_resume')}}"
    return render_template('ProjectsPage.html')


def parse_due_date(due_date_text):
    # 根据给定的日期字符串格式化成日期对象
    return datetime.strptime(due_date_text, '%A, %B %d, %Y').date()
# 注册自定义过滤器
app.jinja_env.filters['parse_due_date'] = parse_due_date

@app.context_processor
def utility_processor():
    def parse_due_date(due_date_text):
        # 根据给定的日期字符串格式化成日期对象
        return datetime.strptime(due_date_text, '%A, %B %d, %Y').date()
    return dict(parse_due_date=parse_due_date)

@app.route('/projects/dues')
def due():
    # 连接 SQLite 数据库
    conn = sqlite3.connect('course.db')
    c = conn.cursor()

    # 获取最大的 batch_id
    c.execute("SELECT MAX(batch_id) FROM course_dues")
    max_batch_id = c.fetchone()[0]

    # 获取最大 batch_id 对应的数据
    c.execute("SELECT * FROM course_dues WHERE batch_id = ?", (max_batch_id,))
    data = c.fetchall()

    # 如果最大 batch_id 中没有数据，则依次取下一个 batch_id
    if not data:
        max_batch_id -= 1
        c.execute("SELECT * FROM course_dues WHERE batch_id = ?", (max_batch_id,))
        data = c.fetchall()

    # 获取当前日期
    current_date = datetime.now().date()

    # 关闭数据库连接
    conn.close()

    # 将日期字符串转换为日期对象，并排序数据
    data.sort(key=lambda x: parse_due_date(x[4]))

    # 渲染模板并传递数据
    return render_template('dues.html', data=data, current_date=current_date)


@app.route('/projects/auto_eda_flask')
def make_auto_eda():
    # 使用 redirect 函数进行端口跳转
    # 注意：这里只是一个示例，实际中你可能需要使用完整的 URL
    streamlit_port = 8501
    return redirect(f'http://3.99.174.2:{streamlit_port}/')


if __name__ == '__main__':
    app.run(debug=True)