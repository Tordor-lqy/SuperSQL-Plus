# SuperSQL 快速开发上线API

只需要编写sql语句以及接口相关信息即可上线API，对于简单需求无需编写多余代码

* 支持params参数 body/json参数
* 支持自定义脚本
* SQL语句支持Jinja2模版语法，更加灵活
* 支持多数据源(目前只支持mysql)
* 支持配置JWT鉴权

缺点：
* python语言性能限制，不适用于大规模生产环境

适用场景
* 用于制作DEMO
* 功能简单的项目

## 计划更新功能

* 支持配置公共脚本
* 支持静态文件代理
* 监控API
* 支持更多类型的数据库

## 环境要求


- `Python 3.10 及以上（64bit）`

## 配置文件

参考 Config.py

## 安装步骤

1. 克隆项目代码到本地环境：

2. 安装依赖包：

   ```bash
   pip install -r requirements.txt
   ```

## 数据库

   * 执行sql文件创建数据库
   * 并且在`config.py` `app/controller/super.py`  中修改数据库配置信息
   * 在表`api_admin`中添加一个管理员

## 运行项目

   本地开发环境中运行项目：
   ```bash
   python3 run.py
   ```

## 部署

   在生产环境中运行项目
   ```bash
     waitress-serve --listen=*:5060  --call "app:create_app"
   ```




