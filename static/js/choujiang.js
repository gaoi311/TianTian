var click = false;
var scratchableLatex = {
    index: -1,     //��ǰת�����ĸ�λ�ã����λ��
    count: 0,      //�ܹ��ж��ٸ�λ��
    timer: 0,      //setTimeout��ID����clearTimeout���
    speed: 100,    //��ʼת���ٶ�
    times: 0,      //ת������
    cycle: 50,     //ת��������������������Ҫת�����ٴ��ٽ���齱����
    prize: -1,     //�н�λ��
    init: function () {
        this.bindEvent();
        this.lotteryInit('lottery');
    },
    bindEvent: function () {
        var that = this;
        $('body').on('click', '.rand_btn', function () {
            if (click) {
                //click����һ�γ齱�����в����ظ�����齱��ť������ĵ������Ӧ                            
                return false;
            } else {
                that.rotateFunc();  // תȦ���̲���Ӧclick�¼����Ὣclick��Ϊfalse
                click = true;       // һ�γ齱��ɺ�����clickΪtrue���ɼ����齱 
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
                var index = Math.random() * (this.count) | 0; //��̬��ʾ���������һ����Ʒ��ţ�ʵ��������ӿڲ���
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
            }, this.speed); //ѭ������
        }
        return false;
    }
}
scratchableLatex.init();