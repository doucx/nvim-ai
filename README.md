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
上下文：
```mermaid
flowchart LR
    buffer-->固定长度-->实上下文

    续写内容-->虚上下文
```
- 进入续写内容后实上下文被固定。

## 功能：
- 手动续写: 手动续写某个部分
    - 全文
- 显示设置: 在右边的窗口中打开AI设置的文件
- 重新生成
