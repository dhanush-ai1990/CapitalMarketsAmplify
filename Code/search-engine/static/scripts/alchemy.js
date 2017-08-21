var json =  {
   
    "nodes": [
        {
            "id": "s1",
            "caption": "John Doe",
            "role": "person",
            "root": false,
        },
        {
            "id": "s2",
            "caption": "Sahba Ezami",
            "role": "person",
            "memoryUsage": 22,
            "root": true,

        },        
        {
            "id": "s3",
            "caption": "Aditi Miglani",
            "role": "person",
            "memoryUsage": 95,
            "root": true
        },
        {
            "id": "s5",
            "caption": "Ada Ene",
            "role": "person",
            "memoryUsage": 30,
            "root": false
        },
        {
            "id": "s6",
            "caption": "Dhanush Dharmaretnam",
            "role": "person",
            "memoryUsage": 10, 
            "root": false
        },
        {
            "id": "s8",
            "caption": "Greg Olmstad",
            "role": "person",
            "memoryUsage": 42,
            "root": false
        }

    ],
    "edges": [
        {
            "source": "s1",
            "target": "s2",
            "load": 0.6
        },
        {
            "source": "s1",
            "target": "s3",
            "load": 0.1
        },
        {
            "source": "s3",
            "target": "s6",
            "load": 2
        },
        {
            "source": "s5",
            "target": "s6",
            "load": 2
        },
        {
            "source": "s5",
            "target": "s2",
            "load": 2
        },
        {
            "source": "s8",
            "target": "s2",
            "load": 2
        },
        {
            "source": "s8",
            "target": "s3",
            "load": 2
        }
    ]
};
      var config = {
            dataSource: json,
            nodeTypes: { "role": 
                ["topic", "person"]
            }, 
            nodeCaptionsOnByDefault: true,
            forceLocked: true,
            nodeStyle: {
                
                "all": {
                    "borderColor": "#000000",
                    "borderWidth": function(d, radius) {
                        return 0
                    },
                    "color": function(d) { 

                        if(d.getProperties().root)
                        return "#1ABB9C"; else return "grey"
                    }, 
                    "radius": function(d) {
                        if(d.getProperties().root)
                        return 20; else return 12 
                    }, 
                    "text": function(d) {
                        display: ;
                    }, 
                }
            },
            edgeStyle: {
                "all": {
                    "width": function(d) {
                     return (d.getProperties().load + 0.5) * 1.3 
                    }
                }
            }
        };

    alchemy = new Alchemy(config)

   