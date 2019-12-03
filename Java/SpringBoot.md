# SpringBoot图片上传后页面无法显示

问题描述：
页面上传图片文件, 后台接收图片保存到本地, 
返回保存路径, 发现页面的<img\>标签无法显示图片, 
F12显示无法加载图片, 
请求地址为localhost:8080/static/img
（楼主将图片保存到了static下）, 
显示404无此资源。

解决方法：需要配置虚拟文件路径的映射
```
//新增加一个类用来添加虚拟路径映射
@Configuration
public class MyPicConfig implements WebMvcConfigurer {    
    @Override    
    public void addResourceHandlers(ResourceHandlerRegistry registry) {        
        registry.
            addResourceHandler("/upload/**")
            .addResourceLocations("file:D:/upload/");    
    }
}
```
addResourceHandler()里配置需要映射的文件夹, 此处代表localhost:8080/upload/下的所有资源。

addResourceLocations()配置文件夹在系统中的路径, 使用绝对路径, 格式为"file:你的路径"

