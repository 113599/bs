//将num左补0为len长度的字符串
export function lpadNum(num, len) {
    var l = num.toString().length;
    while(l < len) {
        num = "0" + num;
        l++;
    }
    return num;
}

//将传入的Date格式化为"yyyy-MM-dd HH:mm:ss"
export function formatDate(d){

    var year = d.getFullYear();
    var month = d.getMonth() + 1;
    var day = d.getDate();
    var hours = d.getHours();
    var minutes = d.getMinutes();
    var seconds = d.getSeconds();
    var resStr = year + "-" +  lpadNum(month, 2) + "-" + lpadNum(day, 2) 
                    + " " + lpadNum(hours,2) + ":" + lpadNum(minutes,2) 
                    + ":" + lpadNum(seconds,2);
    return resStr;
}

export function formatDate_1(d){

    var year = d.getFullYear();
    var month = d.getMonth() + 1;
    var day = d.getDate();
    var resStr = year + "-" +  lpadNum(month, 2) + "-" + lpadNum(day, 2);
    return resStr;
}

// 字符串转换为时间
export function parseDate(str){

    str = str.replace(/-/g, "/");
    return new Date(str);
}

// 获取指定时间的对象
export function getDateObj(d){

    return {
        year: d.getFullYear(),
        month: d.getMonth() + 1,
        day: d.getDate()
    }
}

/**
 * 获取未来5天的日期
 */
export function getNextDays(){

    let days = [];

    let temp = new Date();

    for (let i = 24 * 3; i <= 24 * 7; i += 24) {

        let dateItem = new Date(temp.getTime() + i * 60 * 60 * 1000);

        days.push(formatDate_1(dateItem));
    }

    return days;
}

/**
 * 判断预约处理情况
 * 0 未到预约日期，等待中
 * 1 已到预约日期，等待使用登记
 * 2 预约过期未使用，等待爽约处理
 * 3 预约到期并且登记使用
 * 4.预约过期并且爽约处理
 */
export function contrastOrderDate(orderDate, orderTimes, status){

    let temps = orderTimes.split("~");

    let minDate = parseDate(orderDate + " " + temps[0] + ":00");
	let maxDate = parseDate(orderDate + " " + temps[1] + ":00");
    let nowDate = new Date();

    if(status == 0){

        if(nowDate < minDate){

            return 0;
        }else if(nowDate >= minDate && nowDate <= maxDate){
    
            return 1;
        }else{
    
            return 2;
        }
    }else if(status == 1){

        return 3;
    }else{

        return 4;
    }

    
}