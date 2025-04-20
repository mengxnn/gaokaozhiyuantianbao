let allData = [];
let chartInstance = null;

async function init() {
    const response = await fetch('/api/scores');
    allData = await response.json();

    initProvinceOptions();

    document.getElementById('province').addEventListener('change', updateDisplay);
    document.getElementById('subject').addEventListener('change', updateDisplay);
}

function initProvinceOptions() {
    const provinceSelect = document.getElementById('province');
    const provinces = [...new Set(allData.map(item => item.province))];

    provinces.forEach(province => {
        const option = document.createElement('option');
        option.value = province;
        option.textContent = province;
        provinceSelect.appendChild(option);
    });
}

function updateDisplay() {
    const province = document.getElementById('province').value;
    const subject = document.getElementById('subject').value;

    // 获取降序数据（同时用于表格和图表）
    const filteredData = allData.filter(item =>
        item.province === province &&
        item.subject1 === subject
    ).sort((a, b) => b.score - a.score);

    renderTable(filteredData);
    renderChart(filteredData); // 直接传递降序数据
}

function renderTable(data) {
    const tbody = document.querySelector('#score-table tbody');
    tbody.innerHTML = '';

    data.forEach((item, index) => {
        const row = `
            <tr>
                <td>${item.score}</td>
                <td>${item.num}</td>
                <td>${item.tot_num}</td>
            </tr>
        `;
        tbody.insertAdjacentHTML('beforeend', row);
    });
}

function renderChart(data) {
    if (!chartInstance) {
        chartInstance = echarts.init(document.getElementById('chart'));
    }

    // 预处理：创建分数与累计人数的映射
    const scoreMap = {};
    data.forEach(item => {
        scoreMap[item.score] = item.tot_num;
    });

    // 计算排名区间（使用累计人数）
    const rankRanges = data.map((item, index) => {
        const nextScore = data[index - 1]?.score; // 获取更高分数
        const start = nextScore ? scoreMap[nextScore] + 1 : 1;
        const end = item.tot_num;
        return `${start}-${end}`;
    });

    const option = {
        title: {
            text: '分数段分布图',
            left: 'center',
            textStyle: {
                fontFamily: 'Microsoft YaHei, Arial, sans-serif',
                fontSize: 16
            }
        },
        tooltip: {
            trigger: 'axis',
            formatter: params => {
                const rawData = data[params[0].dataIndex]; // 直接使用原始数据
                return `分数：${rawData.score}<br/>
                        同分人数：${rawData.num}<br/>
                        排名区间：${rankRanges[params[0].dataIndex]}`;
            }
        },
        xAxis: {
            type: 'category',
            data: data.map(item => item.score),
            name: '分数',
            nameTextStyle: {
                fontFamily: 'Microsoft YaHei',
                fontSize: 14
            },
            axisLabel: {
                fontFamily: 'Microsoft YaHei',
                rotate: 45 // 分数较多时自动旋转
            }
        },
        yAxis: {
            type: 'value',
            name: '人数',
            nameTextStyle: {
                fontFamily: 'Microsoft YaHei',
                fontSize: 14
            },
            axisLabel: {
                fontFamily: 'Microsoft YaHei'
            }
        },
        series: [{
            data: data.map(item => item.num), // 直接使用num字段
            type: 'bar',
            itemStyle: {
                color: '#5470C6'
            }
        }]
    };

    chartInstance.setOption(option);
    chartInstance.resize(); // 确保图表自适应容器
}

init();