(function() {
    var province_985211_chart = echarts.init(document.querySelector('.chart'));
    var datalist = []
    option = {
        tooltip: {
            trigger: 'axis',
            axisPointer: {
                type: 'shadow'
            }
        },
        color: ['rgb(255, 191, 138)', 'rgb(250, 168, 101)', 'rgb(255, 141, 47)'],
        legend: {
            top: '5%',
            left: '40%',
            data: ['985', '211', '双一流']
        },
        grid: {
            top: '12%',
            left: '10%',
            right: '15%',
            bottom: '10%',
            containLabel: true
        },
        xAxis: {
            type: 'value',
            boundaryGap: [0, 0.01]
        },
        yAxis: {
            type: 'category',
            data: [
                '北京', '天津', '上海', '重庆', '河北', '河南',
                '云南', '辽宁', '黑龙江', '湖南', '安徽', '山东', '新疆',
                '江苏', '浙江', '江西', '湖北', '广西', '甘肃', '山西',
                '内蒙古', '陕西', '吉林', '福建', '贵州', '广东', '青海',
                '西藏', '四川', '宁夏', '海南', '台湾', '香港', '澳门', '南海诸岛'
            ].reverse()
        },
        series: [{
                name: '985',
                type: 'bar',
                data: [
                    8, 2, 4, 1, 0, 0,
                    0, 2, 1, 3, 1, 2, 0,
                    2, 1, 0, 2, 0, 1, 0,
                    0, 3, 1, 1, 0, 2, 0,
                    0, 2, 0, 0, 0, 0, 0, 0
                ].reverse()
            },
            {
                name: '211',
                type: 'bar',
                data: [
                    26, 3, 10, 2, 2, 1,
                    1, 4, 4, 4, 3, 3, 2,
                    11, 1, 1, 7, 1, 1, 1,
                    1, 8, 3, 2, 1, 4, 1,
                    1, 5, 1, 1, 0, 0, 0, 0
                ].reverse()
            },
            {
                name: '双一流',
                type: 'bar',
                data: [
                    33, 5, 15, 2, 2, 2,
                    0, 4, 4, 5, 3, 3, 2,
                    16, 3, 1, 7, 1, 1, 2,
                    1, 8, 3, 2, 2, 8, 1,
                    2, 8, 1, 1, 0, 0, 0, 0
                ].reverse()
            }
        ]
    };
    province_985211_chart.setOption(option)
})();