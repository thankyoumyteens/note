# 重写FeignClient输出日志

FeignClient默认输出的日志，是多条INFO日志，在并发时，很有可能会互相干扰，而且格式也无法调整。

Feign默认情况下，是使用 feign.Client.Default 发起http请求，可以重写Client，并注入Bean来替换掉 feign.Client.Default，从而实现日志记录

编写FeignConfiguration
```java
public class FeignConfiguration {

    // 注入自定义的LogClient 替换 feign.Client.Default
    @Bean
    public Client feignClient() {
        return new LogClient(null, null);
    }
}
```

重写Client
```java
import com.alibaba.fastjson.JSON;
import com.alibaba.fastjson.JSONException;
import feign.Client;
import feign.Request;
import feign.Response;
import lombok.extern.slf4j.Slf4j;
import org.springframework.http.HttpHeaders;
import org.springframework.http.MediaType;
import org.springframework.util.StopWatch;
import org.springframework.util.StreamUtils;

import javax.net.ssl.HostnameVerifier;
import javax.net.ssl.SSLSocketFactory;
import java.io.*;
import java.util.Collection;
import java.util.Map;

@Slf4j
public class LogClient extends Client.Default {

    public LogClient(SSLSocketFactory socketFactory, HostnameVerifier hostnameVerifier) {
        super(socketFactory, hostnameVerifier);
    }

    @Override
    public Response execute(Request request, Request.Options options) throws IOException {
        StopWatch stopWatch = new StopWatch();
        stopWatch.start();

        Exception exception = null;
        BufferingFeignClientResponse response = null;
        try {
            response = new BufferingFeignClientResponse(super.execute(request, options));
        } catch (Exception exp) {
            log.error(exp.getMessage(), exp);
            exception = exp;
            throw exp;
        } finally {
            stopWatch.stop();
            // 记录request及response信息
            StringBuilder sb = new StringBuilder("[log started]\r\n");
            sb.append(request.httpMethod()).append(" ").append(request.url()).append("\r\n");
            // 记录请求Header
            combineHeaders(sb, request.headers());
            combineRequestBody(sb, request.body(), request.requestTemplate().queries());
            sb.append("\r\nResponse cost time(ms)： ").append(stopWatch.getLastTaskTimeMillis());
            if (response != null) {
                sb.append("  status: ").append(response.status());
            }
            sb.append("\r\n");
            if (response != null) {
                // 记录响应Header
                combineHeaders(sb, response.headers());
                combineResponseBody(sb, response.body(), response.headers().get(HttpHeaders.CONTENT_TYPE));
            }
            if (exception != null) {
                sb.append("Exception:\r\n  ").append(exception.getMessage()).append("\r\n");
            }
            sb.append("\r\n[log ended]");
            // 输出日志
            log.debug(sb.toString());
        }

        Response ret = response.getResponse().toBuilder()
                .body(response.getBody(), response.getResponse().body().length())
                .build();
        response.close();

        return ret;
    }

    private static void combineHeaders(StringBuilder sb, Map<String, Collection<String>> headers) {
        if (headers != null && !headers.isEmpty()) {
            sb.append("Headers:\r\n");
            for (Map.Entry<String, Collection<String>> ob : headers.entrySet()) {
                for (String val : ob.getValue()) {
                    sb.append("  ").append(ob.getKey()).append(": ").append(val).append("\r\n");
                }
            }
        }
    }

    private static void combineRequestBody(StringBuilder sb, byte[] body, Map<String, Collection<String>> params) {
        if (params != null) {
            sb.append("Request Params:\r\n").append("  ").append(params).append("\r\n");
        }
        if (body != null && body.length > 0) {
            sb.append("Request Body:\r\n").append("  ").append(new String(body)).append("\r\n");
        }
    }

    private static void combineResponseBody(StringBuilder sb, String respStr, Collection<String> collection) {
        if (respStr == null) {
            return;
        }
        if (collection.contains(MediaType.APPLICATION_JSON_VALUE) || collection.contains(MediaType.APPLICATION_JSON)) {
            try {
                respStr = JSON.parseObject(respStr).toString();
                //no care this exception
            } catch (JSONException e) {
            }
        }
        sb.append("Body:\r\n").append(respStr).append("\r\n");
    }

    static final class BufferingFeignClientResponse implements Closeable {
        private final Response response;
        private byte[] body;

        private BufferingFeignClientResponse(Response response) {
            this.response = response;
        }

        private Response getResponse() {
            return this.response;
        }

        private int status() {
            return this.response.status();
        }

        private Map<String, Collection<String>> headers() {
            return this.response.headers();
        }

        private String body() throws IOException {
            StringBuilder sb = new StringBuilder();
            try (InputStreamReader reader = new InputStreamReader(getBody())) {
                char[] tmp = new char[1024];
                int len;
                while ((len = reader.read(tmp, 0, tmp.length)) != -1) {
                    sb.append(new String(tmp, 0, len));
                }
            }
            return sb.toString();
        }

        private InputStream getBody() throws IOException {
            if (this.body == null) {
                this.body = StreamUtils.copyToByteArray(this.response.body().asInputStream());
            }
            return new ByteArrayInputStream(this.body);
        }

        @Override
        public void close() {
            this.response.close();
        }
    }
}
```
