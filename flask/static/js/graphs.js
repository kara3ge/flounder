const charts = {};
const MAX_POINTS = 50;
const metrics = [
    {id: 'cpu', label: 'CPU', color1: 'rgb(75, 192, 192)', color2: 'rgba(75, 192, 192, 0.2)', key: 'cpu_usage'},
    {id: 'gpu', label: 'GPU', color1: 'rgb(255, 99, 132)', color2: 'rgba(255, 99, 132, 0.2)', key: 'gpu_usage'},
    {id: 'memory', label: 'Memory', color1: 'rgb(54, 162, 235)', color2: 'rgba(54, 162, 235, 0.2)', key: 'memory_usage'},
    {id: 'disk', label: 'Disk', color1: 'rgb(255, 206, 86)', color2: 'rgba(255, 206, 86, 0.2)', key: 'disk_usage'},
    {id: 'network', label: 'Network', color1: 'rgb(153, 102, 255)', color2: 'rgba(153, 102, 255, 0.2)', key: 'network_usage'},
    {id: 'temp', label: 'Temp', color1: 'rgb(255, 159, 64)', color2: 'rgba(255, 159, 64, 0.2)', key: 'temperature'}
];


function initGraphs() {
    const info = document.querySelector('.info');
    info.style.cssText = 'grid-template-columns: repeat(' + metrics.length + ', 1fr)';
    
    for (const metric of metrics) {
        const card = document.createElement('div');
        card.classList.add('graph-container');
        //make title 
        const title = document.createElement('h3');
        title.textContent = metric.label;
        title.classList.add('graph-title');
        
        const graph = document.createElement('canvas');
        graph.classList.add('graph');

        card.appendChild(title);
        card.appendChild(graph);
        info.appendChild(card);
        
        //create a new chart for given metric
        charts[metric.id] = {chart: new Chart(graph, {
            type: 'doughnut',
            data: {
                labels: ['Used%', 'Free%'], 
                datasets: [{
                    data: [0, 100], 
                    borderColor: metric.color1, 
                    backgroundColor: [metric.color1, metric.color2], 
                    borderWidth: 2, 
                    fill: true
                }]
            },
            options: {
                responsive: false,
                maintainAspectRatio: true,
                plugins: {legend: {display: false}, 
                tooltip: {callbacks: {label: c => c.parsed + '%'}}}
            }
        }), 
        key: metric.key,
    };
    }
}

function updateGraphs(data) {
    Object.keys(charts).forEach(id => {
        const {chart, key} = charts[id];
        const value = data[key];
        chart.data.datasets[0].data = [value, 100 - value];
        chart.update('none');
    });
}

async function fetchData() {
    console.log("graphs.js: fetchData");
    try {
        const res = await fetch('/api/graphs/info_update');
        const data = await res.json();
        updateGraphs(data);
    } catch(e) { console.error("graphs.js: fetchData error", e); }
}

console.log("graphs.js: document.readyState", document.readyState);
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => { 
        initGraphs(); 
        fetchData(); 
        setInterval(fetchData, 2000); 
    });
} else {
    initGraphs();
    fetchData();
    setInterval(fetchData, 2000);
}
