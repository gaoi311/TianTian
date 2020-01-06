var click = false;
var scratchableLatex = {
    index: -1,     //当前转动到哪个位置，起点位置
    count: 0,      //总共有多少个位置
    timer: 0,      //setTimeout的ID，用clearTimeout清除
    speed: 100,    //初始转动速度
    times: 0,      //转动次数
    cycle: 50,     //转动基本次数：即至少需要转动多少次再进入抽奖环节
    prize: -1,     //中奖位置
    init: function () {
        this.bindEvent();
        this.lotteryInit('lottery');
    },
    bindEvent: function () {
        var that = this;
        $('body').on('click', '.rand_btn', function () {
            if (click) {
                //click控制一次抽奖过程中不能重复点击抽奖按钮，后面的点击不响应                            
                return false;
            } else {
                that.rotateFunc();  // 转圈过程不响应click事件，会将click置为false
                click = true;       // 一次抽奖完成后，设置click为true，可继续抽奖 
                return false;
            }
        })
    },
    lotteryInit: function (id) {
        if ($('#' + id).find('.lottery-unit').length > 0) {
            $lottery = $('#' + id);
            $units = $lottery.find('.lottery-unit');
            this.obj = $lottery;
            this.count = $units.length;
            $lottery.find('.turn_' + this.index).addClass('active');
        };
    },
    roll: function () {
        var index = this.index;
        var count = this.count;
        var lottery = this.obj;
        $(lottery).find('.turn_' + index).removeClass('active');
        index += 1;
        if (index > count - 1) {
            index = 0;
        };
        $(lottery).find('.turn_' + index).addClass('active');
        this.index = index;
        return false;
    },
    rotateFunc: function () {
        var that = this;
        this.times += 1;
        this.roll();
        if (this.times > this.cycle + 10 && this.prize == this.index) {
            clearTimeout(this.timer);
            this.prize = -1;
            this.times = 0;
            click = false;
        } else {
            if (this.times < this.cycle) {
                this.speed -= 10;
            } else if (this.times == this.cycle) {
                var index = Math.random() * (this.count) | 0; //静态演示，随机产生一个奖品序号，实际需请求接口产生
                this.prize = index;
            } else {
                if (this.times > this.cycle + 10 && ((this.prize == 0 && this.index == 7) || this.prize == this.index + 1)) {
                    this.speed += 80;
                } else {
                    this.speed += 20;
                }
            }
            if (this.speed < 40) {
                this.speed = 40;
            };
            this.timer = setTimeout(function () {
                that.rotateFunc()
            }, this.speed); //循环调用
        }
        return false;
    }
}
scratchableLatex.init();