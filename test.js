

// 寻找文本内容为“跳过”的按钮并点击
function skipAd() {
    
    console.log(111111)
    
    let buttons = document.querySelectorAll('button, a, div'); // 查找可能的按钮元素
    let skipFound = false;
    
    buttons.forEach(button => {
        if (button.textContent.includes('跳过')) {
            button.click(); // 点击包含“跳过”文本的按钮
            skipFound = true;
            console.log("成功点击跳过按钮"); // 输出通知内容
        }
    });

    if (!skipFound) {
        console.log("未找到跳过按钮");
    }
}

// 延时执行，确保页面加载完成
setTimeout(skipAd, 1000); // 1秒后执行
