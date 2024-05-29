# 使用包装类修改请求和响应数据

示例接口:

```java
package demo;

import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import java.io.BufferedReader;
import java.io.IOException;

@WebServlet("/hello")
public class HelloServlet extends HttpServlet {
    @Override
    protected void doGet(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {}

    @Override
    protected void doPost(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
        BufferedReader br = req.getReader();
        String params = br.readLine();
        resp.setContentType("text/html");
        resp.setStatus(200);
        resp.setCharacterEncoding("utf8");
        // 原样返回
        resp.getWriter().write(params);
    }
}
```

要求: 请求和响应都是加密内容, 需要自动对请求体解密, 自动对响应体加密。

## RequestWrapper

```java
package demo;

import javax.servlet.ReadListener;
import javax.servlet.ServletInputStream;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletRequestWrapper;
import java.io.*;

public class SecretRequestWrapper extends HttpServletRequestWrapper {

    // 存储请求体数据
    private final byte[] body;

    public SecretRequestWrapper(HttpServletRequest request) throws IOException {
        super(request);
        try (InputStream in = request.getInputStream();
             ByteArrayOutputStream out = new ByteArrayOutputStream()
        ) {
            byte[] buff = new byte[1024];
            int read;
            while ((read = in.read(buff)) > 0) {
                out.write(buff, 0, read);
            }
            byte[] byteArray = out.toByteArray();
            // 解密
            for (int i = 0; i < byteArray.length; i++) {
                byteArray[i] = (byte) (byteArray[i] + 1);
            }
            this.body = byteArray;
        }
    }

    @Override
    public BufferedReader getReader() {
        return new BufferedReader(new InputStreamReader(getInputStream()));
    }

    /**
     * request获取post请求体的时候, 会使用这个方法
     */
    @Override
    public ServletInputStream getInputStream() {

        final ByteArrayInputStream buffer = new ByteArrayInputStream(body);

        return new ServletInputStream() {

            @Override
            public int read() {
                return buffer.read();
            }

            @Override
            public boolean isFinished() {
                return buffer.available() == 0;
            }

            @Override
            public boolean isReady() {
                return true;
            }

            @Override
            public void setReadListener(ReadListener readListener) {
                throw new UnsupportedOperationException("Not supported");
            }
        };
    }
}
```

## ResponseWrapper

```java
package demo;

import javax.servlet.http.HttpServletResponse;
import javax.servlet.http.HttpServletResponseWrapper;
import java.io.CharArrayWriter;
import java.io.IOException;
import java.io.PrintWriter;
import java.nio.charset.StandardCharsets;

public class SecretResponseWrapper extends HttpServletResponseWrapper {

    // 返回给servlet的writer
    private final PrintWriter cachedWriter;
    // 存储响应体内容, 它内部的buf字段会保存调用write()方法写入的所有数据
    private final CharArrayWriter bufferedWriter;

    public SecretResponseWrapper(HttpServletResponse response) {
        super(response);
        bufferedWriter = new CharArrayWriter();
        // cachedWriter的write()实际调用的是bufferedWriter的write()
        cachedWriter = new PrintWriter(bufferedWriter);
    }

    /**
     * HelloServlet中通过getWriter()获取Writer对象写响应体
     * 使用自定义的Writer对象
     */
    @Override
    public PrintWriter getWriter() {
        return cachedWriter;
    }

    /**
     * 获取存储在bufferedWriter中的响应体内容
     */
    public String getContent() {
        byte[] byteArray = bufferedWriter.toString().getBytes();
        // 加密
        for (int i = 0; i < byteArray.length; i++) {
            byteArray[i] = (byte) (byteArray[i] - 1);
        }
        try {
            return new String(byteArray, StandardCharsets.UTF_8);
        } catch (Exception e) {
            return "";
        }
    }
}
```

## filter

```java
package demo;

import javax.servlet.*;
import javax.servlet.annotation.WebFilter;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import java.io.IOException;

@WebFilter("/*")
public class DemoFilter implements Filter {
    @Override
    public void init(FilterConfig filterConfig) {}

    @Override
    public void doFilter(ServletRequest servletRequest, ServletResponse servletResponse, FilterChain filterChain) throws IOException, ServletException {
        HttpServletRequest request = (HttpServletRequest) servletRequest;
        HttpServletResponse response = (HttpServletResponse) servletResponse;
        // 使用包装类替换
        SecretResponseWrapper r = new SecretResponseWrapper(response);
        filterChain.doFilter(new SecretRequestWrapper(request), r);
        // SecretRequestWrapper获取到响应体后并不会写回给客户端,
        // 而是存储在bufferedWriter中
        String content = r.getContent();
        // 返回给客户端
        servletResponse.getWriter().write(content);
    }

    @Override
    public void destroy() {}
}
```
