var recent_analysis_chart_option = {
    title: {
        text: '近一个月分析情况'
    },
    tooltip : {
        trigger: 'axis',
        axisPointer: {
            type: 'cross',
            label: {
                backgroundColor: '#6a7985'
            }
        }
    },
    legend: {
        data:['高危','中危','低危']
    },
    grid: {
        left: '3%',
        right: '4%',
        bottom: '15%',
        containLabel: true
    },
    xAxis : [
        {
            type : 'category',
            boundaryGap : false,
            data : ['周一','周二','周三','周四','周五','周六','周日']
        }
    ],
    yAxis : [
        {
            type : 'value'
        }
    ],
    dataZoom: [
        {
            id: 'dataZoomX',
            type: 'slider',
            xAxisIndex: [0],
            filterMode: 'filter',
            bottom: 10,
            start: 75,
            end: 100
        }
    ],
    // color: [
    //     '#c22d00',
    //     '#edde4c',
    //     '#b0c4c8',
    //     '#d48265',
    //     '#91c7ae',
    //     '#749f83',
    //     '#ca8622'
    // ],
    series : [
        {
            name: "高危",
            type:'line'
        },
        {
            name: "中危",
            type:'line'
        },
        {
            name: "低危",
            type:'line'
        }
    ]
};


var recent_analysis_summary_chart_option = {
    title : [
        {
            text: '威胁情况统计',
            left:'center'
        },
        {
            text: "今日",
            left: "45%",
            top: "8%"
        },
        {
            text: "本周",
            left: "20%",
            top: "55%"
        },
        {
            text: "本月",
            left: "70%",
            top: "55%"
        }
    ],
    grid: {
        left: '3%',
        right: '4%',
        bottom: '15%',
        containLabel: true
    },
    tooltip : {
        trigger: 'item',
        formatter: "{a} <br/>{b} : {c} ({d}%)"
    },
    legend: {
        orient: 'vertical',
        left: 'left',
        data: ["高危", "中危", "低危"]
    },
    itemStyle: {
        normal: {
            // 阴影的大小
            shadowBlur: 100,
            // 阴影水平方向上的偏移
            shadowOffsetX: 0,
            // 阴影垂直方向上的偏移
            shadowOffsetY: 0,
            // 阴影颜色
            shadowColor: 'rgba(0, 0, 0, 0.3)'
        }
    },
    // color: [
    //     '#c22d00',
    //     '#caa74b',
    //     '#c7cbca',
    //     '#d48265',
    //     '#91c7ae',
    //     '#749f83',
    //     '#ca8622'
    // ],
    series : [
        {
            name:'今日',
            type:'pie',
            radius : [0, '50%'],
            center: ["50%", "40%"],
            areaStyle: {normal: {}},
            label: { normal: { show: false }, emphasis: { show: true }},
            lableLine: { normal: { show: false }, emphasis: { show: true }},
            data: [
                {value: 1, name: "高危"},
                {value: 1, name: "中危"},
                {value: 1, name: "低危"}
            ]
        },
        {
            name:'本周',
            type:'pie',
            radius : [0, '36%'],
            center: ["25%", "80%"],
            areaStyle: {normal: {}},
            label: { normal: { show: false }, emphasis: { show: true }},
            lableLine: { normal: { show: false }, emphasis: { show: true }},
            data: [
                {value: 1, name: "高危"},
                {value: 1, name: "中危"},
                {value: 1, name: "低危"}
            ]
        },
        {
            name:'本月',
            type:'pie',
            radius : [0, '36%'],
            center: ["75%", "80%"],
            areaStyle: {normal: {}},
            label: { normal: { show: false }, emphasis: { show: true }},
            lableLine: { normal: { show: false }, emphasis: { show: true }},
            data: [
                {value: 1, name: "高危"},
                {value: 1, name: "中危"},
                {value: 1, name: "低危"}
            ]
        }
    ]
};

var system_status_chart_option= {
        title: [
            {
                text: '系统负载',
                left: 'center'
            },
            {
                text: "磁盘",
                left: "15%",
                top: "55%"
            },
            {
                text: "CPU",
                left: "45%",
                top: "55%"
            },
            {
                text: "内存",
                left: "75%",
                top: "55%"
            }
        ],
        grid: {
            left: '3%',
            right: '4%',
            bottom: '15%',
            containLabel: true
        },
        tooltip : {
            trigger: 'item',
            formatter: "{a} <br/>{b} : {c} ({d}%)"
        },
        legend: {
            orient: 'vertical',
            left: 'left',
            data: ["已用", "可用"]
        },
        itemStyle: {
            normal: {
                // 阴影的大小
                shadowBlur: 100,
                // 阴影水平方向上的偏移
                shadowOffsetX: 0,
                // 阴影垂直方向上的偏移
                shadowOffsetY: 0,
                // 阴影颜色
                shadowColor: 'rgba(0, 0, 0, 0.3)'
            }
        },
        color: [
            '#929192',
            '#48a84e',
            '#b0c4c8',
            '#d48265',
            '#91c7ae',
            '#749f83',
            '#ca8622'
        ],
    series : [
        {
            name:'磁盘使用量',
            type:'pie',
            radius : ["28%", '42%'],
            center: ["20%", "60%"],
            areaStyle: {normal: {}},
            label: { normal: { show: false }, emphasis: { show: true }},
            lableLine: { normal: { show: false }, emphasis: { show: true }},
            tooltip : {
                trigger: 'item',
                formatter: "{a} <br/>{b} : {c}G ({d}%)"
            },
            data: [
                {value: 1, name: "已用"},
                {value: 1, name: "可用"}
            ]
        },
        {
            name:'CPU使用量',
            type:'pie',
            radius : ["28%", '42%'],
            center: ["50%", "60%"],
            areaStyle: {normal: {}},
            label: { normal: { show: false }, emphasis: { show: true }},
            lableLine: { normal: { show: false }, emphasis: { show: true }},
            tooltip : {
                trigger: 'item',
                formatter: "{a} <br/>{b} : {d}%"
            },
            data: [
                {value: 1, name: "已用" },
                {value: 1, name: "可用"}
            ]
        },
        {
            name:'内存使用量',
            type:'pie',
            radius : ["28%", '42%'],
            center: ["80%", "60%"],
            areaStyle: {normal: {}},
            label: { normal: { show: false }, emphasis: { show: true }},
            lableLine: { normal: { show: false }, emphasis: { show: true }},
            tooltip : {
                trigger: 'item',
                formatter: "{a} <br/>{b} : {c}G ({d}%)"
            },
            data: [
                {value: 1, name: "已用"},
                {value: 1, name: "可用"}
            ]
        }
    ]
};

