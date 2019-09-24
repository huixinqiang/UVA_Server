/**
 * Created by iecas on 2018/7/10.
 */
var serviceip="http://192.168.43.197:8888/";
var height=722, width=700;
var margin = {left:30, right:30};
$(function() {
    "use strict";
    width = document.body.clientWidth-300-margin.left-margin.right;
    height = document.body.clientHeight-68;
    $('#slice-container').height=document.body.clientHeight-60;
    $('#main-container').empty();
    var svg = d3.select("#main-container")
        .append("svg")
        .attr("transform", function(){
            return "translate(" +xStart()
                + "," + yStart() + ")";
        })
        .attr("height",height)
        .attr("width",width)
        .call(
            d3.zoom()
                .scaleExtent([1,10])
                .on("zoom",zoomHandler)
        );

    //定义图像比例尺
    var x=d3.scaleLinear()
        .range([0,width]),
        y=d3.scaleLinear()
            .range([0,height]);

    // Init Theme Core
    createHTML();

    // Admin Dock Plugin
    $('.quick-compose-form').dockmodal({
        minimizedWidth: 260,
        width: 470,
        height: 480,
        title: '历史拍摄列表',
        initialState: "minimized",
        showClose:false,
        showPopout:false
    });

    var playInterval;
    var pause_flag = false;

    $("#take-pic-auto").click(function(){
        if(pause_flag)
        {
            this.textContent="拍摄";
            clearInterval(playInterval);
            pause_flag=false;
        }
        else
        {
            this.textContent="暂停";
            playInterval = setInterval(function(){
                createHTML();
            },2000);
            pause_flag=true;
        }


    });

    $("#take-pic").click(function(){
        if(pause_flag)
        {
            $("#take-pic-auto").html("拍摄");
            clearInterval(playInterval);
            pause_flag=false;
        }
        createHTML();
    });


    function xStart(){
        //return $("#main_img").position().left-$("#main-container").position().left;
        return 0;
    }
    function yStart(){
        //return $("#main_img").position().top-$("#main-container").position().top;
        return 0;
    }

    function zoomHandler(){
        var transform = d3.event.transform;

        svg.attr("transform", "translate("
            + transform.x + "," + transform.y
            + ")scale(" + transform.k + ")");
    }

    //更新切片列表HTML
    function updateSliceImgD3(data) {
        d3.select("#slice-container .panel-body")
            .classed("panel-scroller scroller scroller-active", false);
        $("#slice-container .panel-body").empty();

        var panelbody = d3.select("#slice-container .panel-body");
        panelbody.selectAll("div.of-h")
            .data(data)
            .enter()
            .append("div")
            .attr("class", "col-md-4 of-h")
            .append("img")
            // .attr("src", function (d) {
            //    return serviceip + d.clip_path;
            // })
            .attr("src","3.png")
            .attr("class", "user-avatar")
            .on("mouseover", function (d, i) {
                d3.select("img.selected-img")
                    .classed("selected-img", false);
                d3.select(this)
                    .classed("selected-img", true);

                d3.select("rect.selected")
                    .classed("selected", false);
                d3.selectAll("rect.line").filter(function (dd) {
                        if (dd.minx == d.minx && dd.maxx == d.maxx && dd.miny == d.miny && dd.maxy == d.maxy)
                            return true;
                        else
                            return false;
                    })
                    .classed("selected", true);

            });
    }

//更新切片列表HTML
    function updateSliceImg(data) {
        d3.select("#slice-container .panel-body")
            .classed("panel-scroller scroller scroller-active", false);
        $("#slice-container .panel-body").empty();

        $.each(data,function(index){

            var paths = this.clip_path.split("/");
            var title_name = paths[paths.length-1];
            var content_html='<div class="col-md-4 of-h">'+

                // '<img src="3.png" class="user-avatar" title="' + title_name + '">'+
                '<span class="badge badge-info"> '+(index+1)+'</span>'+
                '<img src="'+ serviceip + this.clip_path + '" class="user-avatar" title="' + title_name + '">'+

                '</div>';

            $("#slice-container .panel-body").append(content_html);

        });

        d3.selectAll("img.user-avatar")
            .data(data)
            .on("mouseover",function(d){
                d3.select("img.selected-img")
                    .classed("selected-img", false);
                d3.select(this)
                    .classed("selected-img", true);

                d3.select("rect.selected")
                    .classed("selected", false);
                d3.selectAll("rect.line").filter(function (dd) {
                        if (dd.minx == d.minx && dd.maxx == d.maxx && dd.miny == d.miny && dd.maxy == d.maxy)
                            return true;
                        else
                            return false;
                    })
                    .classed("selected", true);
        });

    }

        //绘制主图像
    function drawMainImage(data){
        d3.select("svg").selectAll("image")
            .data(data)
            .enter()
            .append("image");

        d3.select("svg").selectAll("image")
            .data(data)
            .exit().remove();

        d3.select("svg").selectAll("image")
            .data(data)
            // .attr("xlink:href","nb-2_1.png")
            .attr("xlink:href",function(d){return serviceip+d.img_path;})
            .attr("x",0)
            .attr("y",0)
            .attr("width",width)
            .attr("height",height);
    }

    function drawCostTime(data){
        d3.select("svg").selectAll("text.time-text")
            .data(data)
            .enter()
            .append("text")
            .attr("class","time-text");

        d3.select("svg").selectAll("text.time-text")
            .data(data)
            .exit().remove();

        d3.select("svg").selectAll("text.time-text")
            .data(data)
            .attr("class","time-text")
            .attr("x",width/2)
            .attr("y",40)
            .text(function(d){return "处理时间："+d.cost_time+"ms  图像大小："+ d.img_width +"*"+ d.img_height;});
    }

//绘制标注框
    function drawAnnotationRect(data){
        var g = svg.selectAll("g")
            .data(data)
            .enter()
            .append("g");
        g.append("rect").attr("class","line");
        g.append("circle").attr("class","badge-circle");
        g.append("text").attr("class","badge-text");

        svg.selectAll("g")
            .data(data)
            .exit().remove();

        svg.selectAll("g")
            .data(data)
          .select("rect.line")
            .attr("class",function (d) {
                if(d.name=="military")
                    return "line military";
                else
                    return "line";
            })
            .attr("x",function(d){
                return x(d.minx);
            })
            .attr("y",function(d){return y(d.miny);})
            .attr("width",function(d){return x(d.maxx)-x(d.minx);})
            .attr("height",function(d){return y(d.maxy)-y(d.miny);})
            .on("mouseover",function(d,i){
                d3.select("rect.selected")
                    .classed("selected",false);
                d3.select(this)
                    .classed("selected",true);

                d3.select("img.selected-img")
                    .classed("selected-img",false);
                d3.selectAll("img.user-avatar").filter(function(dd,ii){
                        if(dd.minx== d.minx && dd.maxx== d.maxx && dd.miny== d.miny && dd.maxy== d.maxy)
                            return true;
                        else
                            return false;
                    })
                    .classed("selected-img",true);


            });

        svg.selectAll("g")
            .data(data)
           .select("text")
            .attr("class","badge-text")
            .attr("x",function(d){return x(d.maxx)-8;})
            .attr("y",function(d){return y(d.miny)+4;})
            .attr("dy",".7em")
            .text(function(d,index){
                return index+1;
            });

        svg.selectAll("g")
            .data(data)
          .select("circle")
            .attr("class","badge-circle")
            .attr("cx",function(d){return x(d.maxx)-8;})
            .attr("cy",function(d){return y(d.miny)+8;})
            .attr("r","8");

    }

    var last_json_id;
//获取不同类型样本集元数据
    function createHTML()
    {
        var getjsonurl = serviceip + "take_photo.json";
        // var getjsonurl = "take_photo.json";
        d3.json(getjsonurl,function(error,data){
            if(data!=null && data!="" && JSON.stringify(data)!="{}"){
                if(data.img_tag===last_json_id)
                    return;
                last_json_id = data.img_tag;
                var json_array=[];
                json_array.push(data);
                drawMainImage(json_array);//绘制主图像
                drawCostTime(json_array);
                var slice_data_array=[];
                $.each(data.list,function(){
                    slice_data_array.push(this);
                });
                if(data.img_width/width > data.img_height/height)
                {
                    var tmp=data.img_height/(data.img_width/width);
                    y.range([(height-tmp)/2,(height+tmp)/2]);
                }
                else
                {
                    var tmp=data.img_width/(data.img_height/height);
                    x.range([(width-tmp)/2,(width+tmp)/2]);
                }

                x.domain([0,data.img_width]);
                y.domain([0,data.img_height]);

                var img=new Image();
                img.src = serviceip+data.img_path;
                img.onload=function(){
                   drawAnnotationRect(slice_data_array);
                   updateSliceImg(slice_data_array);
                    attachToHistory(data);
                    $("#slice-container .panel-body").addClass("panel-scroller");
                    Core.init();
                };
                // drawAnnotationRect(slice_data_array);
                // updateSliceImg(slice_data_array);
                // attachToHistory(data);
                // $("#slice-container .panel-body").addClass("panel-scroller");
                // Core.init();
            }

        });
    }

    //添加到历史拍摄列表中
    function attachToHistory(data) {
        $('#historyList li').removeClass("active");
        var content_html='<li class="active" data-id="' + data.img_tag + '">'+
            '<a href="javascript:void(0)">'+
                '<span>'+
                    '<img src="'+ serviceip + data.img_path + '" class="img-responsive mw20 ib mr10">'+
                '</span>'+data.img_tag+
                '<b class="pull-right text-muted">'+data.img_time+'</b>'+
            '</a>'+

            '</li>';

        $("#historyList").append(content_html);

        $('#historyList li').click(function () {
            $("#historyList li.active").removeClass("active");
            $(this).addClass("active");
            var itemid = $(this).data("id");
            var getjsonurl = serviceip+"retrieve_photo_by_id/"+itemid+".json";
            d3.json(getjsonurl,function(error,data){
                if(data!=null && data!="" && JSON.stringify(data)!="{}"){
                    var json_array=[];
                    json_array.push(data);
                    drawMainImage(json_array);//绘制主图像
                    drawCostTime(json_array);
                    var slice_data_array=[];
                    $.each(data.list,function(){
                        slice_data_array.push(this);
                    });
                    if(data.img_width/width > data.img_height/height)
                    {
                        var tmp=data.img_height/(data.img_width/width);
                        y.range([(height-tmp)/2,(height+tmp)/2]);
                    }
                    else
                    {
                        var tmp=data.img_width/(data.img_height/height);
                        x.range([(width-tmp)/2,(width+tmp)/2]);
                    }

                    x.domain([0,data.img_width]);
                    y.domain([0,data.img_height]);

                    var img=new Image();
                    img.src = serviceip+data.img_path;
                    img.onload=function(){
                       drawAnnotationRect(slice_data_array);
                       updateSliceImg(slice_data_array);
                        drawAnnotationRect(slice_data_array);
                        updateSliceImg(slice_data_array);
                    };
                    // drawAnnotationRect(slice_data_array);
                    // updateSliceImg(slice_data_array);
                }
                // $("#slice-container .panel-body").addClass("panel-scroller");
                // Core.init();
            });
        });
    }


});

