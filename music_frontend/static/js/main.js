/* eslint-disable linebreak-style */
/* eslint-disable no-restricted-syntax */

// const webPath = 'http://localhost:8001/'
const webPath = 'https://fma-small-dataset-song-matcher.herokuapp.com/'

function dropDown() {
    d3.json(`${webPath}getTestTracks/`).then(((data) => {
        $('.selectpicker').hide();
        for (const [key, value] of Object.entries(data)) {
            $('#songDropdownVal').append(`<option value="${key}">${value}</option>`);
        }
        refreshSelectPicker();
    }));
}

dropDown();

drag = simulation => {
  
    function dragstarted(d) {
        if (!d3.event.active) simulation.alphaTarget(0.3).restart();
        d.fx = d.x;
        d.fy = d.y;
      }
      
      function dragged(d) {
        d.fx = d3.event.x;
        d.fy = d3.event.y;
      }
      
      function dragended(d) {
        if (!d3.event.active) simulation.alphaTarget(0);
        d.fx = null;
        d.fy = null;
      }
    
    return d3.drag()
        .on("start", dragstarted)
        .on("drag", dragged)
        .on("end", dragended);
  }

function display(data) {
    const links = [];
    const nodes = [];

    nodes.push(Object.create(data[0]));

    for (let i = 1; i < Object.keys(data).length; i++) {
        const link = {
            source: data[0].track_name,
            target: data[i].track_name,
            value: data[i].distance,
            track_id: data[i].track_id,
        };
        links.push(Object.create(link));

        const node = {
            track_name: data[i].track_name,
            track_id: data[i].track_id,
            distance: data[i].distance,
        };
        nodes.push(Object.create(node));
    }

    const width = $('#scatterplot').outerWidth();
    const height = $('#scatterplot').outerHeight();
    const svg = d3.select('#scatterplot').append('svg')
        .attr('width', width)
        .attr('height', height);

    const tooltip = d3.select('body').append('div')
        .attr('class', 'tooltip')
        .style('opacity', 0)
        .style('background-color', 'white')
        .style('color', 'black')
        .style('border', 'solid')
        .style('border-width', '4px')
        .style('border-radius', '6px')
        .style('padding', '10px')
        .style('position', 'absolute');

    const mouseover = function () {
        tooltip
            .style('opacity', 1);
        d3.select(this)
            .style('opacity', 1);
    };

    const mousemove = function (d) {
        let html = '';
        html = `${`Name: ${d.__proto__.track_name}<br>Track ID: ${d.__proto__.track_id}
                <br>Distance: ${d.__proto__.distance}`}`;
        tooltip
            .html(html)
            .style('left', d3.event.pageX + 10 +'px')
            .style('top', d3.event.pageY + 10 +'px');
    };

    const mouseleave = function () {
        tooltip
            .style('opacity', 0);
        d3.select(this)
            .style('opacity', 0.8);
    };

    const simulation = d3.forceSimulation(nodes)
        .force('link', d3.forceLink(links).distance(d => parseFloat(d.value)).id(d => d.track_name))
        .force('charge', d3.forceManyBody())
        .force('center', d3.forceCenter(width / 2, height / 2));

    const link = svg.append('g')
        .attr('stroke', '#999')
        .attr('stroke-opacity', 1)
        .selectAll('line')
        .data(links)
        .join('line')
        .attr('stroke-width',  d => Math.cbrt(d.value));

    const node = svg.append('g')
        .attr('stroke', '#fff')
        .attr('stroke-width', 1.5)
        .selectAll('circle')
        .data(nodes)
        .join('circle')
        .attr('r', 9)
        .style('opacity', 0.8)
        .style('fill', d => (d.__proto__.distance == '1.0' ? 'teal' : 'brown'))
        .call(drag(simulation))
        .on('mouseover', mouseover)
        .on('mousemove', mousemove)
        .on('mouseleave', mouseleave);

    simulation.on('tick', () => {
        link
            .attr('x1', d => d.source.x)
            .attr('y1', d => d.source.y)
            .attr('x2', d => d.target.x)
            .attr('y2', d => d.target.y);

        node
            .attr('cx', d => d.x)
            .attr('cy', d => d.y);
    });

    return svg.node();
}

$('#searchMetadata').on('change', () => {
    $('#metaDataDropdown').toggle();
});

$('#searchContent').on('change', () => {
    $('#metaDataDropdown').toggle();
});

$('#songDropdownVal').on('change', () => {
    const trackID = $('#songDropdownVal').val();
    const kVal = $('#valueofK').val();
    d3.json(`${webPath}getKNeighbours/?trackID=${trackID}&k=${kVal}`).then(((data) => {
        d3.select('svg').remove();
        display(data);
    }));
});

$('#valueofK').on('change', () => {
    const trackID = $('#songDropdownVal').val();
    const kVal = $('#valueofK').val();
    d3.json(`${webPath}getKNeighbours/?trackID=${trackID}&k=${kVal}`).then(((data) => {
        d3.select('svg').remove();
        display(data);
    }));
});

$('#statbttn').on('click', () =>{
    d3.json(`${webPath}stats`).then(((data) => {
        let html =
        `Number of Rows and Columns in the Small Subset: ${data.shape}
        Total number of Unique Genres: ${data.genresl}
        Total number of Unique Bitrates: ${data.bitratel}
        Total number of Unique Artists: ${data.artistl}
        Total number of Unique Albums: ${data.albuml}`;
        alert(html);
    }));
});
