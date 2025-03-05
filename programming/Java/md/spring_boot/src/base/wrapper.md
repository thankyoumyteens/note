# 使用包装类修改请求和响应数据

### 1. 包装 request

```java
import jakarta.servlet.ReadListener;
import jakarta.servlet.ServletInputStream;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletRequestWrapper;

import java.io.*;
import java.nio.charset.StandardCharsets;
import java.util.Collections;
import java.util.Enumeration;
import java.util.HashMap;
import java.util.Map;

// 自定义请求包装类
public class CustomRequestWrapper extends HttpServletRequestWrapper {
    // 由于getInputStream()和getReader()方法读取数据是一次性的,
    // 所以这里使用body来暂存请求体数据
    // 然后重写getInputStream()和getReader()方法返回修改后的新数据
    private final String body;

    public CustomRequestWrapper(HttpServletRequest request) {
        super(request);
        // 接收请求体数据, 保存到stringBuilder中
        StringBuilder stringBuilder = new StringBuilder();
        BufferedReader bufferedReader = null;
        try {
            InputStream inputStream = request.getInputStream();
            if (inputStream != null) {
                bufferedReader = new BufferedReader(new InputStreamReader(inputStream, StandardCharsets.UTF_8));
                char[] charBuffer = new char[128];
                int bytesRead;
                while ((bytesRead = bufferedReader.read(charBuffer)) > 0) {
                    stringBuilder.append(charBuffer, 0, bytesRead);
                }
            }
        } catch (IOException ex) {
            ex.printStackTrace();
        } finally {
            if (bufferedReader != null) {
                try {
                    bufferedReader.close();
                } catch (IOException ex) {
                    ex.printStackTrace();
                }
            }
        }
        String s = stringBuilder.toString();
        System.out.println("读取到的请求体: " + s);
        // TODO 在这里对请求体数据进行修改后再赋值给body
        s = "{\"name\": \"John\", \"age\": 30}";
        body = s;
    }

    @Override
    public ServletInputStream getInputStream() throws IOException {
        // 返回修改后的请求体数据
        final ByteArrayInputStream byteArrayInputStream = new ByteArrayInputStream(body.getBytes());
        return new ServletInputStream() {
            @Override
            public boolean isFinished() {
                return byteArrayInputStream.available() == 0;
            }

            @Override
            public boolean isReady() {
                return true;
            }

            @Override
            public void setReadListener(ReadListener readListener) {
                throw new UnsupportedOperationException();
            }

            @Override
            public int read() throws IOException {
                return byteArrayInputStream.read();
            }
        };
    }

    @Override
    public BufferedReader getReader() throws IOException {
        return new BufferedReader(new InputStreamReader(this.getInputStream(), StandardCharsets.UTF_8));
    }

    public String getBody() {
        return this.body;
    }

    // 示例：修改请求参数
    @Override
    public String getParameter(String name) {
        // TODO 在这里修改请求参数
        if ("param1".equals(name)) {
            return "modifiedValue";
        }
        return super.getParameter(name);
    }

    @Override
    public Map<String, String[]> getParameterMap() {
        // 接收所有get请求参数
        Map<String, String[]> originalMap = super.getParameterMap();
        Map<String, String[]> modifiedMap = new HashMap<>(originalMap);
        // TODO 在这里修改请求参数
        if (originalMap.containsKey("param1")) {
            modifiedMap.put("param1", new String[]{"modifiedValue"});
        }
        return modifiedMap;
    }

    @Override
    public Enumeration<String> getParameterNames() {
        return Collections.enumeration(getParameterMap().keySet());
    }

    @Override
    public String[] getParameterValues(String name) {
        return getParameterMap().get(name);
    }
}
```

### 2. 包装 response

```java
import jakarta.servlet.ServletOutputStream;
import jakarta.servlet.WriteListener;
import jakarta.servlet.http.HttpServletResponse;
import jakarta.servlet.http.HttpServletResponseWrapper;

import java.io.ByteArrayOutputStream;
import java.io.IOException;
import java.io.OutputStreamWriter;
import java.io.PrintWriter;
import java.util.Arrays;

// 自定义响应包装类
public class CustomResponseWrapper extends HttpServletResponseWrapper {
    private final ByteArrayOutputStream outputStream;
    private ServletOutputStream servletOutputStream;
    private PrintWriter writer;

    public CustomResponseWrapper(HttpServletResponse response) {
        super(response);
        outputStream = new ByteArrayOutputStream();
    }

    @Override
    public ServletOutputStream getOutputStream() throws IOException {
        if (writer != null) {
            throw new IllegalStateException("getWriter() has already been called on this response.");
        }
        // 把响应体数据写入到我们指定的输出流servletOutputStream中
        // 这样我们就可以获取到响应体数据了
        if (servletOutputStream == null) {
            servletOutputStream = new CustomServletOutputStream(outputStream);
        }
        return servletOutputStream;
    }

    @Override
    public PrintWriter getWriter() throws IOException {
        if (servletOutputStream != null) {
            throw new IllegalStateException("getOutputStream() has already been called on this response.");
        }
        if (writer == null) {
            writer = new PrintWriter(new OutputStreamWriter(outputStream, getCharacterEncoding()));
        }
        return writer;
    }

    public byte[] getContentAsByteArray() {
        if (writer != null) {
            writer.flush();
        } else if (servletOutputStream != null) {
            try {
                servletOutputStream.flush();
            } catch (IOException e) {
                e.printStackTrace();
            }
        }
        byte[] content = outputStream.toByteArray();
        System.out.println("修改前的响应体: " + Arrays.toString(content));
        // TODO 在这里对响应体数据进行修改后再返回
        String r = "{\"name\": \"John\", \"age\": 30}";
        return r.getBytes();
    }

    private static class CustomServletOutputStream extends ServletOutputStream {
        private final ByteArrayOutputStream outputStream;

        public CustomServletOutputStream(ByteArrayOutputStream outputStream) {
            this.outputStream = outputStream;
        }

        @Override
        public boolean isReady() {
            return true;
        }

        @Override
        public void setWriteListener(WriteListener writeListener) {
            // 暂不实现
        }

        @Override
        public void write(int b) throws IOException {
            outputStream.write(b);
        }
    }
}
```

### 3. 在 filter 中使用包装类

```java
import jakarta.servlet.*;
import jakarta.servlet.FilterConfig;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;

import java.io.IOException;

public class CustomFilter implements Filter {

    // 指定要跳过的接口
    private static final String[] SKIP_URLS = {"/demo/hello"};

    @Override
    public void init(FilterConfig filterConfig) {
    }

    @Override
    public void doFilter(ServletRequest servletRequest, ServletResponse servletResponse, FilterChain filterChain) throws IOException, ServletException {
        HttpServletRequest request = (HttpServletRequest) servletRequest;
        HttpServletResponse response = (HttpServletResponse) servletResponse;

        String requestUrl = request.getRequestURI();
        // 检查请求 URL 是否为指定要跳过的接口
        for (String skipUrl : SKIP_URLS) {
            if (requestUrl.equals(skipUrl)) {
                // 直接放行请求
                filterChain.doFilter(servletRequest, servletResponse);
                return;
            }
        }

        // 使用包装类替换
        CustomRequestWrapper requestWrapper = new CustomRequestWrapper(request);
        CustomResponseWrapper responseWrapper = new CustomResponseWrapper(response);
        filterChain.doFilter(requestWrapper, responseWrapper);

        // 获取修改后的响应体
        byte[] contentAsByteArray = responseWrapper.getContentAsByteArray();
        // 返回给客户端
        response.setContentType("application/json");
        response.setCharacterEncoding("UTF-8");
        servletResponse.setContentLength(contentAsByteArray.length);
        servletResponse.getOutputStream().write(contentAsByteArray);
    }

    @Override
    public void destroy() {
        Filter.super.destroy();
    }
}
```

### 4. 注册 filter

```java
import org.springframework.boot.web.servlet.FilterRegistrationBean;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

@Configuration
public class FilterConfig {

    @Bean
    public FilterRegistrationBean<CustomFilter> tokenFilter() {
        FilterRegistrationBean<CustomFilter> registration = new FilterRegistrationBean<>();
        // 设置过滤器实例
        registration.setFilter(new CustomFilter());
        // 设置过滤器的 URL 匹配模式，对所有接口生效
        registration.addUrlPatterns("/*");
        // 设置过滤器名称
        registration.setName("customFilter");
        // 设置过滤器的执行顺序
        registration.setOrder(1);
        return registration;
    }
}
```
