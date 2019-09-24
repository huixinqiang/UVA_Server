/**
 * Created by iecas on 2018/7/10.
 */

var serviceip="http://192.168.43.197:8888/";
var height=700, width=722;
$(function() {
    "use strict";
    // Init Theme Core
    Core.init();

    $("#start").click(function(){
        var f=formatDate(new Date(),true);
        var initial_ok = getData(serviceip);
        if(initial_ok=="OK")
        {
            $("#start_info").html(f+":    启动成功");
            window.location.href="take_photo.html";

        }
        else
            $("#start_info").html(f+": "+initial_ok);
    });

    //获取数据
    function getData(url,data){
        //获取数据
        var my_data;
        $.ajax({
            url: url,
            type: "GET",
            dataType: "text",
            async: false,
            data: data,
            error:function(req,status){
                my_data=req.statusText;
            },
            success: function(result) {
                my_data=result;
            }
        });
        return my_data;
    }

    //时间戳转换日期格式
    function formatDate(stp,all) {
        var time = new Date(stp);
        var time_year = time.getFullYear();
        var time_month = time.getMonth() + 1;
        var time_date = time.getDate();
        var time_hour = time.getHours();
        var time_minute = time.getMinutes();
        var time_second = time.getSeconds();
        if (time_month < 10) {
            time_month = "0" + time_month;
        }
        if (time_date < 10) {
            time_date = "0" + time_date;
        }
        if (time_hour < 10) {
            time_hour = "0" + time_hour;
        }
        if (time_minute < 10) {
            time_minute = "0" + time_minute;
        }
        if (time_second < 10) {
            time_second = "0" + time_second;
        }
        if (all === true) {
            return time_year + "-" + time_month + "-" + time_date + " " + time_hour + ":" + time_minute + ":" + time_second;
        }
        else {
            return time_year + "-" + time_month + "-" + time_date;
        }
    }



});

