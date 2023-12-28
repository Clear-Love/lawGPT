# lawGPT

## 如何使用

### 项目后端

1. 下载项目所需模型[Chatlaw-text2Vec](https://huggingface.co/chestnutlzj/ChatLaw-Text2Vec) 和语言模型 [Chatglm2-6b](https://huggingface.co/THUDM/chatglm2-6b) 放入model文件夹下
2. 编辑配置文件`lawgpt/config/settings.yml`
3. 制作向量数据库
```
cd backend
python lawgpt/services/vecDBService.py
```
4. 安装项目所需依赖
    ```shell
    pip install poetry
    poetry build
    poetry install ./dist/*.whl
    ```
5. 运行项目 -p选项修改端口
    ```shell
    lawgpt server -p 8000
    # or
    python app.py
    ```
### 前端

- docker 启动
    ```shell
    docker run -d \
        -p 80:3000 \
        --restart unless-stopped \
        --name lawgpt-ui
    ```
- dev
```
pnpm install
pnpm run dev
```

- build
```
pnpm install
pnpm run build
node server/index.mjs
```

## 声明
4. 本项目任何资源**仅供学术研究使用，严禁任何商业用途**。
5. 模型输出受多种不确定性因素影响，本项目当前无法保证其准确性，**严禁用于真实法律场景**。
6. 本项目不承担任何法律责任，亦不对因使用相关资源和输出结果而可能产生的任何损失承担责任。