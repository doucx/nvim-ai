# vim-localai
用本地LLM为neovim提供加强的类
## AI接口
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
一个生成器，从ws连接中产生词语

#### BaseConfig 
基本设置，定义了模型的基本参数

#### AI 
提供一组方法(目前只需要实现completion)用于方便使用。
## Vim操作
```mermaid
flowchart LR
    subgraph 上下文获取
        buffer-->固定长度-->上下文
        buffer-->某处开始-->上下文
        buffer-->选区-->上下文
    end
    上下文
    subgraph 续写方法
        上下文-->续写
        上下文-->自动续写

        续写---阻断
        续写---长长度

        续写-->续写内容---o定位

        自动续写---不阻断输入
        自动续写---短长度
        自动续写-->自动续写内容--o定位
        自动续写内容-->暂存

        暂存-->续写内容

        定位-->高亮
        定位-->重写
        定位-->保留

        续写内容-->重写
        续写内容-->保留

        重写--o参数变动

        保留--o选区1[选区]
        保留--o到指针位置
        保留--o默认清空
    end
```
它需要做到这些：
1. 可以进行续写与打断
    - 无选区时
        - 默认行为
    - 对选区进行续写
2. 可以方便地舍弃/切换续写的内容
    - 对续写内容的定位
    - 重写
    - 选择保留
3. 容易看见续写了什么
    - 对续写内容的定位，增加“高亮”
