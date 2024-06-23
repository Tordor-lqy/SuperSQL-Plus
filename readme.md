# SuperSQL 快速开发上线API

优点：
* 只需要编写sql语句即可上线API，对于简单需求无需编写多余代码
* 支持多数据源
* 支持一键配置JWT鉴权

缺点：
* 抛弃了ORM ，安全性有所降低
* python语言性能限制，不适用于真实生产环境

适用场景
* 用于小规模的API
* 时间紧迫情况下
* 用于制作DEMO

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
   




