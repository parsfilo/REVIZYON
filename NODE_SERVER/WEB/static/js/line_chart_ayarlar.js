const config = {
    displayModeBar: false,
};

var data = [
    {
        type: 'scatter',
        mode: 'lines',
        y: [],
        showlegend: false,
        line: {
            color: '#FFFF00',
            width: 1
        }
    },
    {
        y: [],
        showlegend: false,
        line: {
            color: '#FFFFFF',
            width: 1
        }
    },
    {
        y: [],
        showlegend: false,
        line: {
            color: '#00FF00',
            width: 1
        }
    }
];

var layout = {
    margin: {
        l: 30,
        r: 30,
        b: 50,
        t: 50,
        pad: 0
    },
    yaxis: {
        autorange: true,
        showgrid: true,
        ticks: 'outside',
        dtick: 0.1,
        tickcolor: '#000',
        tickwidth: 2,
        range: [-0.1, 0.1],
        type: 'linear'

    },

    paper_bgcolor: '#f5f5dc',
    plot_bgcolor: '#000000',
    font: {
        size: 12,
        color: '#000000'
    }
};
Plotly.newPlot("myDiv", data, layout, config);