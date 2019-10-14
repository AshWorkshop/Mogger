# Mogger

## 安装
```bash
pip install git+https://github.com/AshWorkshop/Mogger.git
```

## 使用
假设`MongoDB`已启用
```Python
import mogger
logger = mogger.Logger(url="mongodb://root:example@localhost:27017/", database="logging", collection="log", level=mogger.INFO)

logger.info("Hello, world!")
logger.warning({
    'description': '测试'
})

logger.get(level=mogger.INFO, latest=2)
logger.get(level=mogger.INFO, exact=True, latest=1)
```