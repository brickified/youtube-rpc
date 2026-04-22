// ==UserScript==
// @name         Youtube RPC
// @namespace    http://tampermonkey.net/
// @version      2026-04-16
// @description  Youtube RPC
// @author       Brickified
// @match        https://www.youtube.com/*
// @icon         https://www.google.com/s2/favicons?sz=64&domain=youtube.com
// @grant GM_xmlhttpRequest
// @connect localhost
// @connect 127.0.0.1
// ==/UserScript==

(function(){
    const port = 2342;
    console.log('Youtube RPC by Brickified --- Started!')

    let sec = s => new Date(s * 1000).toISOString().substring(11, 19);

    function playerStatus() {
        let video = document.querySelector('video')
        let playing = !video.paused
        let time = sec(Math.round(video.currentTime))

        if (playing) {
            playing = '_a'
        } else {
            playing = '_b'
        }

        return playing+' '+time
    }

    function getUrl() {
        if (window.location.search.split('?v=') == undefined) {
            return undefined
        } else {
            return window.location.search.split('?v=')[1].split('&')[0]
        }
    }

    function deconflict() {
        let data = getUrl()
        let url = 'http://localhost:'+port+'/?deconflict='+data
        console.log('YTRPC | sent deconflict')
        GM_xmlhttpRequest({
            method: "GET",
            url: url
        })
    }

    let lastStat = null
    setInterval(_=>{
        let stat = playerStatus()
        let data = stat+" ; "+getUrl()
        if (stat !== lastStat) {
            lastStat = stat

            let url = 'http://localhost:'+port+'/?status='+btoa(data)
            console.log('YTRPC | sent data "'+data+'"')
            if (getUrl() !== undefined) {
                GM_xmlhttpRequest({
                    method: "GET",
                    url: url
                })
            }
        }
    }, 5000)

    let lastUrl = getUrl()
    setInterval(_=>{
        let url = getUrl()
        if (url !== lastUrl) {
            lastUrl = url
            deconflict()
        }
    },500)
    setInterval(_=>{
        let video = document.querySelector('video')
        if (!video.paused) {
            deconflict()
        }
    },15e3)
    deconflict()
})()
