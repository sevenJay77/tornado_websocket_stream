
var websocket = null;

//判断当前浏览器是否支持WebSocket
if ('WebSocket' in window) {
    websocket = new ReconnectingWebSocket('ws://' + window.location.host + window.location.pathname + 'ws');
    websocket.reconnectInterval = 4000;
} else {
    alert('Not support websocket')
}

function setLogInfo(log) {
    console.log(log);
}

//连接发生错误的回调方法
websocket.onerror = function () {
    setLogInfo("error");
};

//连接成功建立的回调方法
websocket.onopen = function (event) {
    setLogInfo("open");
};


websocket.onclose = function () {
    setLogInfo("close");
    websocket.close();
};

window.onbeforeunload = function () {
    websocket.close();
};

//接收到消息的回调方法
websocket.onmessage = function (event) {
    var reader = new FileReader();
    reader.onload = function()
    {
        showImage(this.result);
    };
    // 二进制读取websocket内容
    reader.readAsArrayBuffer(event.data);
};

async function showImage(buffer) {
    console.log(buffer);
    var imageData = await getImageData(buffer);
    var camera;
    if (imageData.length > 0) {
        var reader = new FileReader();
        reader.onload = function (event) {
            if (event.target.readyState == FileReader.DONE) {
                // 属性将包含一个data:URL格式的字符串（base64编码）以表示所读取文件的内容。
                var url = event.target.result;
                camera = document.getElementById('cam');
                camera.src = url;
            }
        };
        // 获取到blob对象
        reader.readAsDataURL(imageData[0]);
    }
}

function getImageData(buffer) {
    return new Promise(function (resolve, reject) {
        setTimeout(function () {
            // arraybuffer 转为blob
            var imageBlob = new Blob([buffer]);
            resolve(new Array(imageBlob));
        }, 10)

    })
}