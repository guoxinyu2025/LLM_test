## price 价格比对

1. 获取厂商列表，模型列表
2. 获取模型列表
3. 获取调用接口类型
4. 统计调用次数，获取开始金额，调用完金额
5. 成功模型，失败模型，错误原因写入本地


## How to use 

```shell
提供LLMProvider服务压测命令行工具。

Usage:
  press [flags]
  press [command]

Available Commands:
  completion  Generate the autocompletion script for the specified shell
  help        Help about any command
  model_check 检测模型结果及状态|模型返回结果是否符合预期
  providers   获取厂商列表|模型列表

Flags:
  -h, --help   help for press

Use "press [command] --help" for more information about a command.
```