# lawGPT

1. 下载项目所需模型[Chatlaw-text2Vec]() 和语言模型 [Chatglm2-6b]() 放入model文件夹下
2. 编辑配置文件`lawgpt/config/settings.yml`
3. 安装项目所需依赖
    ```shell
    pip install poetry
    poetry build
    poetry install ./dist/*.whl
    ```
4. 运行项目 -p选项修改端口
    ```shell
    lawgpt server -p 8000
    # or
    python app.py
    
## 声明

1. 本项目任何资源**仅供学术研究使用，严禁任何商业用途**。
2. 模型输出受多种不确定性因素影响，本项目当前无法保证其准确性，**严禁用于真实法律场景**。
3. 本项目不承担任何法律责任，亦不对因使用相关资源和输出结果而可能产生的任何损失承担责任。