# 使用方法

## 确认NAT类
打开：https://mao.fan/mynat
如果是NAT1，基本可以穿透
如果是NAT2，需要打开UPNP
如果是NAT3，需要打开UPNP
NAT4就不用尝试了，不行的

## 申请短URL
 - 申请地址：https://1web.us.kg/

## 保存短URL
 - 链接`/s/`后面的`AABBCCDD`是suffix`网站后缀`
 - `更新密码`要保存好，只会显示一次，无法恢复

## 安装Lucky
安装教程：https://lucky666.cn/docs/install

## 设置Lucky
1. 设置本地地址端口：

2. 设置云端更新地址：
 - 请求地址：`https://1web.us.kg/p/`
 - 请求类型：POST
 - 请求体：
```json
{
  "suffix": "网站后缀",
  "tokens": "更新密码",
  "typing": "http",
  "ipaddr": "{ip}",
  "porter": "{port}"
}
```

## 测试Lucky
等保存之后，打开https://1web.us.kg/s/XXXXXXXX
如果能正常打开则穿透成功

## 设置Ports
1. 打开StunConnects（桌面APP）或者IP:1680（Docker）
2. 新增连接映射：
    - 映射备注：您自己设置一个名称
    - 跳转链接：上一步成功的短链接
    - 本地端口：监听本地端口，不填则随机生成
3. 复制本地或者云端地址，在浏览器或软件进行测试