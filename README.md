# vim-localai
用本地LLM为neovim提供加强的类
## python AI接口
```mermaid
flowchart LR
    设定参数-->AI
    上下文-->AI.completion-->续写内容
```

```mermaid
classDiagram
    class Gene{
        __init__(url, json)
        __iter__()
    }

    class BaseConfig{
        url
        use_model
        temperature
        top_k
        ...
    }

    class AI{
        base_config
        completion(text) -> Gene
    }
    AI <.. Gene
    AI <.. BaseConfig
```
#### Gene
一个生成器，从ws连接中获取词语

#### BaseConfig 
基本设置，定义了模型的基本参数

#### AI 
提供一组方法(目前只需要实现completion)用于方便使用。
## Vim操作
自动续写：
```mermaid
flowchart LR
    上下文-->md["如果在末端\n或者在续写内容中"]

    md--否--->什么都不做
    md--是--->自动续写-->续写内容
    md--是--->锁定实上下文

    续写内容-->执行长续写-->继续续写更多
    续写内容-->高亮1

    暂存内容-->高亮2

    续写内容-->重写
    续写内容-->光标移动到其中-->暂存到指针位置-->暂存内容

    光标移动到其中-->自动续写
```
上下文：
```mermaid
flowchart LR
    buffer-->固定长度-->实上下文
    buffer-->某处开始-->实上下文

    续写内容-->虚上下文
```
- 进入续写内容后实上下文被固定。

## 功能：
- 自动续写: 打开/关闭自动续写功能
    - 从某处开始
    - 全文
    - 固定长度上文
- 手动续写: 手动续写某个部分
    - 从某处开始
    - 全文
    - 固定长度上文
- 显示设置: 在右边的窗口中打开AI设置的文件
- 重新生成

## TODO
- 带提示词的修改
    - 选区
- 带下文的续写
