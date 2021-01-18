# idea maven依赖引入失败，dependencies全部红线问题

解决办法：出现这种情况一般是有某个依赖包坐标或版本无法下载导致的，先maven clean，然后maven install，找出无法下载的包，修改为正确的坐标，在重新reimport即可

idea需要删除.idea和*.iml重新导入项目
