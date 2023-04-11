function lpadNum(num, len) {
    var l = num.toString().length;
    while(l < len) {
        num = "0" + num;
        l++;
    }
    return num;
}

export function getDateInfo(){

    let d = new Date();

    let year = d.getFullYear();
    let month = d.getMonth() + 1;
    let day = d.getDate();
    let hours = d.getHours();
    let minutes = d.getMinutes();

    let dateStr = year + "-" +  lpadNum(month, 2) + "-" + lpadNum(day, 2);

    let timeStr = lpadNum(hours,2) + ":" + lpadNum(minutes,2);
    return {
        d: dateStr,
        t: timeStr
    };
}

