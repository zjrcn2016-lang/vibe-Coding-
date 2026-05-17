一、因为Claude-code需要用到海外的信用卡，以及海外网络环境来进行使用，对我们来说不是很方便，所以我们可以用中转站来解决 付费以及网络问题，实现用国内环境配置Claude-code.

我用到的中转站是：云雾API
https://yunwu.ai/register?aff=CUO8

二、Windows安装Claude-code
参考文档：
https://yunwu.apifox.cn/doc-7010249
1、
管理员模式打开Powershell,按照官方安装方法安装
```
   irm https://claude.ai/install.ps1 | iex
```
2、安装完之后会在你的系统盘（我的系统盘是C盘）用户，用户名下生成一个.claude文件
参考目录:
C:\Users\用户名\\.claude
在这里我们需要新建一个settings.json文件来连结中转站

![[Pasted image 20260517132543.png]]
```
{
  "env": {
    "ANTHROPIC_AUTH_TOKEN": "sk-你的中转站令牌",
    "ANTHROPIC_BASE_URL": "主站名字",
    "ANTHROPIC_DEFAULT_HAIKU_MODEL": "claude-sonnet-4-6",
    "ANTHROPIC_DEFAULT_HAIKU_MODEL_NAME": "claude-sonnet-4-6",
    "ANTHROPIC_DEFAULT_OPUS_MODEL": "claude-sonnet-4-6",
    "ANTHROPIC_DEFAULT_OPUS_MODEL_NAME": "claude-sonnet-4-6",
    "ANTHROPIC_DEFAULT_SONNET_MODEL": "claude-sonnet-4-6",
    "ANTHROPIC_DEFAULT_SONNET_MODEL_NAME": "claude-sonnet-4-6",
    "ANTHROPIC_MODEL": "claude-sonnet-4-6",
    "API_TIMEOUT_MS": "300000",
    "CLAUDE_CODE_DISABLE_EXPERIMENTAL_BETAS": "1"
  }
}
```
注意json格式不能用#注释
3、打开claude,因为win10的Powershell的界面太丑了，所以可以去微软商店下载一个windows terminal
![[Pasted image 20260517132928.png]]

通过Terminal，打开Claude,建议在项目根目录中打开。

通过Terminal 进入你所在的项目目录，然后输入claude就可以打开啦
```
cluade
```

![[Pasted image 20260517133237.png|697]]

PS：建议大家在中转站中新建一个令牌，选择对应的特价的分组,来节省token的消耗。
![[Pasted image 20260517133438.png|697]]


4、CC-Switch可视化配置工具。
[CC Switch 官方网站 - AI 编程 CLI 统一管理工具](https://www.ccswitch.io/zh/)

因为我们每次改模型或者以后切换中转站，总是要打开settings.json文件很麻烦。所以推荐使用这个工具可以方便我们修改配置

可视化界面如图，大家自行摸索即可。
![[Pasted image 20260517134836.png]]