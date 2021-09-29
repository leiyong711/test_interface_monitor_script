项目说明
```
用于监控当地实际用户真实访问当地节点接口响应时间
```

执行流程
```
1、在对应节点服务器对api进行请求，测试当地访问节点响应时间。
2、通过HTTP请求把测试结果发回到测试服务器上的web服务进行入库并统计
```

部署需求
```
1、目前美国东部、美国西部、英国各需要部署一份
2、每小时需要调度一次
```

Python依赖库
```
python所用到的依赖库在 requirements.txt
批量安装命令:
pip3 install -r requirements.txt
```

启动方式
```
python3 main.py -p <代理地址> -n <节点名称> -c 2
例如:
python3 main.py -p  http://user:pssswd@1.1.1.1:80 -n US-East -c 2
参数说明：
-p 代理ip地址  
-n 节点名称(当前脚本部署节点)
   美国东部 US-East
   美国西部 US-West
   英国    UK
-c 每次单个接口执行次数
```

## docker run
```
docker run -d --name monitor_script --restart=always pytomtoto/test_interface_monitor_script:bfe3a888 tail -f /dev/null
docker run -d --name monitor_script --restart=always registry.cn-hangzhou.aliyuncs.com/leiyong/test_interface_monitor_script:04a48427 tail -f /dev/null
```
