$(function(){
    var $li = $('.slide_pics li');
    var len = $li.length;
    // 将要运动过来的li
    var nowli = 0;
    // 当前要离开的li
    var prevli = 0;
    // 选择左右箭头
    var $prev = $('.prev');
    var $next = $('.next');
    // 定义定时器来自动播放幻灯片
    var timer = null;
    // 选择不是第一个的li元素
    $li.not(':first').css({left:450});
    // 通过程序动态设置幻灯片图片下方的圆点：使用循环
    $li.each(function(index){
        // 创建li元素
        var $sli = $('<li>');
        // 设置第一个li元素的class为active
        if(index==0){
            $sli.addClass('active');
        }
        $sli.appendTo('.points');
    });
    var $points = $('.points li');
    $points.click(function(){
        // 点击哪个圆点，就是要哪个li运动过来
        nowli = $(this).index();
        // 重复点击同一个圆点，图片会左右跳一下
        // 解决方法：设置在同一张图片点击的时候，不执行函数
        if(nowli==prevli){
            return;
        }
        move();
        // 设置圆点高亮对应当前的幻灯片图片
        $(this).addClass('active').siblings().removeClass('active');
    });
    // 设置左右箭头左右移动幻灯片
    $prev.click(function(){
        nowli--;
        move();
        // 设置圆点高亮和左右箭头移动幻灯片图片相对应
        $points.eq(nowli).addClass('active').siblings().removeClass('active');
    });
    $next.click(function(){
        nowli++;
        move();
        $points.eq(nowli).addClass('active').siblings().removeClass('active');
    });
    // 设置鼠标放到幻灯片图片区域（图片或圆点或左右箭头）上时，动画暂停
    $('.slide_con').mouseenter(function(){
        // 清空定时器
        clearInterval(timer);
    });
    $('.slide_con').mouseleave(function(){
        // 开启定时器
        timer = setInterval(autoplay,2000);
    });
    // 开启定时器
    timer = setInterval(autoplay,2000);
    // 设置自动播放幻灯片：播放下一张图片
    function autoplay(){
        nowli++;
        move();
        $points.eq(nowli).addClass('active').siblings().removeClass('active');
    }
    function move(){
        // 在第一张图片点击左箭头：要跳到最后一张图片，最后一张图片要从左边过来，第一张图片要从右边离开
        if(nowli<0){
            nowli = len-1;
            prevli = 0;
            $li.eq(nowli).css({left:-450});
            // 快速多次点击右箭头或左箭头时，图片会混乱
            // 解决方法：在每个animate()前添加stop()方法
            $li.eq(prevli).stop().animate({left:450});
            $li.eq(nowli).stop().animate({left:0});
            prevli = nowli;
            // 要使用return结束函数的运行，否则会继续执行下面的if(nowli>prevli){}
            return;
        }
        // 在最后一张图片点击右箭头：要跳到第一张图片，第一张图片要从右边过来，最后一张图片要从左边离开
        if(nowli>len-1){
            nowli = 0;
            prevli = len-1;
            $li.eq(nowli).css({left:450});
            $li.eq(prevli).stop().animate({left:-450});
            $li.eq(nowli).stop().animate({left:0});
            prevli = nowli;
            // 要使用return结束函数的运行，否则会继续执行下面的else{}
            return;
        }
        // 在最后一张图片点击右箭头
        // 从索引小的跳到大的：大的图片要从右边过来，小的图片要从左边离开
        if(nowli>prevli){
            $li.eq(nowli).css({left:450});
            $li.eq(prevli).stop().animate({left:-450});
            /* $li.eq(nowli).animate({left:0});
            // 把nowli赋值给prevli：将要运动过来的li运动过来了就会变成当前要离开的li
            prevli = nowli; */
        }
        // 从索引大的跳到小的：小的图片要从左边过来，大的图片要从右边离开
        else{
            $li.eq(nowli).css({left:-450});
            $li.eq(prevli).stop().animate({left:450});
            /* $li.eq(nowli).animate({left:0});
            prevli = nowli; */
        }
        $li.eq(nowli).stop().animate({left:0});
        prevli = nowli;
    }
});