给request添加一个包装类ParameterRequestWrapper，继承HttpServletRequestWrapper，先从request中取输入流，读取流中的数据，然后重写getInputStream（）和getReader（）方法。

```java
public class ParameterRequestWrapper extends HttpServletRequestWrapper {
 
	private byte[] buffer;
 
	public ParameterRequestWrapper(HttpServletRequest request) throws IOException {
		super(request);
		InputStream is = request.getInputStream();
		ByteArrayOutputStream baos = new ByteArrayOutputStream();
		byte[] buff = new byte[1024];
		int read = 0;
		while ((read = is.read(buff)) > 0)
			baos.write(buff, 0, read);
 
		this.buffer = baos.toByteArray();
	}
 
 
	public BufferedReader getReader() throws IOException{
		return new BufferedReader(new InputStreamReader(getInputStream()));
	}
 
	public ServletInputStream getInputStream() throws IOException
	{
		String buf = new String(buffer);
		System.out.println("request的包装类中的内容："+buf);
		ParamUtil paramUtil = new ParamUtil();
		boolean offlineLicense = paramUtil.isOfflineLicense(buf);
		if (offlineLicense) {
			String offlineToken = paramUtil.getOfflineToken(buf);
			HttpClientUtil httpClientUtil = new HttpClientUtil();
			String user = httpClientUtil.getUserByToken(offlineToken);
			String endTime = httpClientUtil.getDisconnectUtil(user);
			String resetParamsOffline = paramUtil.resetParamsOffline(buf, endTime);
			if (resetParamsOffline==null) {//不修改
				return new BufferedServletInputStream(this.buffer);
			}else {//修改
				byte[] bufs = new byte[1024];
				bufs = resetParamsOffline.getBytes();
				return new BufferedServletInputStream(bufs);
			}
		}
		return new BufferedServletInputStream(this.buffer);
	}
 
}
```

上面是修改请求参数的，还有，有时候需要对返回的结果进行修改，这时候也需要使用包装类。写一个ParameterResponseWrapper，继承HttpServletResponseWrapper,主要是重写getOutputStream（）和getWriter（）方法。

```java
public class ParameterResponseWrapper extends HttpServletResponseWrapper{
 
    private MyWriter myWriter;
    private MyOutputStream myOutputStream;
 
    public ParameterResponseWrapper(HttpServletResponse response) throws IOException{
        super(response);
    }
 
    public ServletOutputStream getOutputStream() throws IOException{
 
    	myOutputStream = new MyOutputStream(super.getOutputStream());
        return myOutputStream;
    }
 
    public PrintWriter getWriter() throws IOException{
        myWriter =  new MyWriter(super.getWriter());
        return myWriter;
    }
 
    public MyWriter getMyWriter() {
        return myWriter;
    }
    
    public MyOutputStream getMyOutputStream(){
    	return myOutputStream;
    }
}
```

然后，就可以在filter中使用包装后的request和response了。
```java
filterChain.doFilter(reqWrapper,responseWrapper);//此处的request和response要写包装类
```
