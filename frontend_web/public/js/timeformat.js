/**
 * Changes timeformat to fit to user's browser
 */

function changeToBrowserTime(utcTime){
    // utcTime: "YYYY-MM-DD HH:mm:ss"
    let year = parseInt(utcTime.substr(0, 4))
    let monthIdx = parseInt(utcTime.substr(5, 2)) - 1
    let day = parseInt(utcTime.substr(8, 2))
    let hour = parseInt(utcTime.substr(11, 2))
    let mins = parseInt(utcTime.substr(14, 2))
    let sec = parseInt(utcTime.substr(17, 2))
    
    const timeoffsetMinutes = new Date().getTimezoneOffset()

    const browserTime = new Date(year, monthIdx, day, hour, mins - timeoffsetMinutes, sec)
    return browserTime
}

// #last-update-headline
// .article-publish-date

function modifyTimeElements(){

    const headlineTime = document.getElementById("last-update-headline")
    if(headlineTime != null)
        headlineTime.innerHTML = changeToBrowserTime(headlineTime.innerHTML).toString()
    
    const articleTimes = document.getElementsByClassName("article-publish-date")
    if(articleTimes != null)
        for(let idx = 0; idx < articleTimes.length; idx++){
            const element = articleTimes[idx]

            element.innerHTML = changeToBrowserTime(element.innerHTML).toString()
        }
}

modifyTimeElements()