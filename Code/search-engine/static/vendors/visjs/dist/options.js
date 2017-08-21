  function reloadDataScript(topic) {
    var src = "/static/vendors/visjs/datasource/"+topic+".js";

    $('script[src="' + src + '"]').remove();
    $('<script>').attr('src', src).appendTo('head');
  }

var network;

  function redrawAll() {
    var container = document.getElementById('mynetwork');
    var width = 800;
    var height = 800;

    var options = {
      width: width + 'px',
      height: height + 'px',
      nodes: {
        shape: 'dot',
        scaling: {
          min: 10,
          max: 40
        },
        font: {
          size: 12,
          face: 'Tahoma'
        }
      },
      edges: {
        color:{inherit:true},
        width: 0.15,
        smooth: {
         // type: 'continuous'
         type: 'horizontal'
        }
      },
      groups: {
            1: {color: { border: "#2B7CE9", background: "#97C2FC", highlight: { border: "#2B7CE9", background: "#D2E5FF" }, hover: { border: "#2B7CE9", background: "#D2E5FF" } }}, // 0: blue
            2: {color: { border: "#FFA500", background: "#FFFF00", highlight: { border: "#FFA500", background: "#FFFFA3" }, hover: { border: "#FFA500", background: "#FFFFA3" } }},
            3: {color: { border: "#FA0A10", background: "#FB7E81", highlight: { border: "#FA0A10", background: "#FFAFB1" }, hover: { border: "#FA0A10", background: "#FFAFB1" } }}, // 2: red
            4: {color: { border: "#41A906", background: "#7BE141", highlight: { border: "#41A906", background: "#A1EC76" }, hover: { border: "#41A906", background: "#A1EC76" } }}, // 3: green
            5: {color: { border: "#E129F0", background: "#EB7DF4", highlight: { border: "#E129F0", background: "#F0B3F5" }, hover: { border: "#E129F0", background: "#F0B3F5" } }}, // 4: magenta
            6: {color: { border: "#C37F00", background: "#FFA807", highlight: { border: "#C37F00", background: "#FFCA66" }, hover: { border: "#C37F00", background: "#FFCA66" } }}, // 6: orange
            7: {color: { border: "#7C29F0", background: "#AD85E4", highlight: { border: "#7C29F0", background: "#D3BDF0" }, hover: { border: "#7C29F0", background: "#D3BDF0" } }}, // 5: purple
        },
      physics: false,
      interaction: {
        hideEdgesOnDrag: true,
        tooltipDelay: 200
      },
      physics: false
    };

    var data = {nodes:nodes, edges:edges};
    network = new vis.Network(container, data, options);
    network.on("doubleClick",doubleClickFunction);
    network.moveTo({
    position: {x: 0, y: 0},
    offset: {x: -width/2, y: -height/2},
    scale: 1,
})
    

  }

function doubleClickFunction(params) {
  if (params.nodes.length == 1) {
    clicked_node = nodes[params.nodes[0]-1];
    // if people
    if(clicked_node.group == 2)
    {
      name = clicked_node.label.split(' ').join('+');
      window.open("/profile/"+name,"_self");
    }
    // if client
    if(clicked_node.group == 3)
    {

    }
    // if topic
    if(clicked_node.group == 4)
    {
      name = clicked_node.label.split(' ').join('+');
      window.open("/topic/"+name,"_self");
    }
    // if organization
    if(clicked_node.group == 5)
    {
      name = clicked_node.label.split(' ').join('+');
      window.open("/client/"+name,"_self");
    }
    // if places
    if(clicked_node.group == 6)
    {
      name = clicked_node.label;
      window.open("https://en.wikipedia.org/wiki/"+name,"_self");
    }
  }
}

window.onload = function() {
  redrawAll();
};

function updateOptions()
{
  var topicName = $('#topic_hidden_div').text();
    $.ajax({
      type: 'POST',
      url: '/topic',
      datatype: "json",
      data: { 'showPeople' : $('#showPeople').prop('checked'),
       'showTopics' : $('#showTopics').prop('checked'),
      'showExperts' : $('#showExperts').prop('checked'), 
      'showClients' : $('#showClients').prop('checked'),
      'showOrgs' : $('#showOrgs').prop('checked'),
      'showPlaces' : $('#showPlaces').prop('checked'),
      'topic_name': topicName},
      success: function(response) {
        reloadDataScript(topicName);
        redrawAll();
      }
  });
}

