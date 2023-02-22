```js
axios.post('/exportExcel', params, { responseType: 'blob' })
    .then(res => {
        let fileName = res.headers['content-disposition'];
        let regFileName = fileName.match(/=(.*)$/)[1];
        let decodedFileName = decodeURI(regFileName);
        const link = document.createElement('a');
        let blob = new Blob([res.data], { type: 'application/vnd.ms-excel;charset=utf-8' });
        link.style.display = 'none';
        link.href = URL.createObjectURL(blob);
        link.download = decodedFileName;
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
    });
```
