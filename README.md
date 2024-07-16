# nvim-ai
让neovim变成类似text-generator-webui的notebook

## 前提
有一个类似openai api的api，推荐使用text-generator-webui的openai api（因为在用这个）

## 安装
```bash
cd ~/.config/nvim/rplugin/python3 # 或者任何别的python插件目录
git clone https://github.com/doucx/nvim-ai.git
pip install -r ./requirements.txt
nvim
```
然后运行`:UpdateRemotePlugins`，再重新启动`nvim`

## 设置
将以下信息放在`init.lua`里。
```lua
-- 基本参数
vim.g.vim_localai_settings = {
  urls = {
    completions = "http://localhost:5000/v1/completions", -- 网址，以text-generator-webui提供的openai api为例
  },
  completions = {
    max_tokens = 64,
    temperature = 0.7,
    top_p = 0.9,
    top_k = 20,
    -- stop = {"A:", "B:"} -- 遇到`A:`或`B:`时停止生成

    -- 我不确定以下这些参数有没有用处
    repetition_penalty = 1.15,
  }
}
-- 按键绑定
vim.api.nvim_set_keymap('n', '<S-CR>', ":AICompletions<CR>", { noremap = true, silent = false })
vim.api.nvim_set_keymap('n', '<C-BS>', ":AIStopCompletions<CR>", { noremap = true, silent = false })
vim.api.nvim_set_keymap('n', '<C-CR>', ":AIReCompletions<CR>", { noremap = true, silent = false })
vim.api.nvim_set_keymap('n', '<S-BS>', ":AIClearCompletions<CR>", { noremap = true, silent = false })
```

## Vim Command
## AICompletions
续写全文
## AIStopCompletions
停止续写全文
## AIReCompletions
重新进行续写
## AIClearCompletions
清除续写内容

## TODO
- 高亮生成内容
- 加入openai token以使用openai的api（真正的）
- 对仅部分内容进行处理
