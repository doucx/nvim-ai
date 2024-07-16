# vim-localai
用本地LLM为neovim提供加强的类

## 设置
```lua
-- 基本参数
vim.g.vim_localai_settings = {
  urls = {
    completions = "http://localhost:5000/v1/completions", -- 网址，以text-generator-webui提供的openai api为例
  },
  completions = {
    max_tokens= 64,
    temperature = 0.7,
    top_p = 0.9,
    top_k = 20,
    repetition_penalty = 1.15,

    stop = {"A:", "B:"} -- 遇到`A:`或`B:`时停止生成
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
