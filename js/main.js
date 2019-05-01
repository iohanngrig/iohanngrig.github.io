$(".mynavbar").load('mynavbar.html');

// $(document).ready(function() {
//     $('.navbar-bar > li > a[href^="' + location.pathname.split("/")[3] + '"]').parent().addClass('active');
//     console.log(location.pathname.split("/")[3]);
// });


function appendData(data) {
    let mainContainer = document.getElementById("myData");
    for (let i = 0; i < data.length; i++) {
        let div = document.createElement("div");
        div.className = "col-lg-4 col-sm-6 portfolio-item";
        div.innerHTML =   "<div class='card h-100'>"
                        +    "<a href=" + data[i].url + "><img alt=' ' class='card-img-top' src=" + data[i].media + "></a>"
                        +    "<div class='card-body'>"
                        +      "<h4 class='card-title'><a href=" + data[i].url + ">" + data[i].title + "</a></h4>"
                        +      "<p class='card-text'>" + data[i].description + "</p>"
                        +  "</div></div>";
        mainContainer.appendChild(div);
    }
}


function appendData2(data) {
    let mainContainer = document.getElementById("myData2");
    for (let i = 0; i < data.length; i++) {
        let div = document.createElement("div");
        div.className = "row";
        div.innerHTML =  "<div class='col-md-7'>"
                        +  "<a href=" + data[i].url + "><img alt=' ' class='img-fluid rounded mb-3 mb-md-0' src=" + data[i].media2 + "></a>"
                        +"</div>"
                        +"<div class='col-md-5'>"
                        +   "<h3>" + data[i].title + "</h3>"
                        +   "<p>" + data[i].description + "</p>"
                        +   "<a class='btn btn-primary' href=" + data[i].url + ">View Project"
                        +     "<span class='glyphicon glyphicon-chevron-right'></span>"
                        +   "</a>"
                        +"</div>"
                        +"<hr>";
        mainContainer.appendChild(div);
        mainContainer.append(document.createElement("hr"))
    }
}

function appendData3(data) {
    let mainContainer = document.getElementById("myData3");
    for (let i = 0; i < data.length; i++) {
        let div = document.createElement("div");
        div.className = "row";
        div.innerHTML =  "<div class='col-md-7'>"
                        +  "<a href=" + data[i].url + "><img alt=' ' class='img-fluid rounded mb-3 mb-md-0' "
                        +                                   "src=" + data[i].media + " width='700' height='300'></a>"
                        +"</div>"
                        +"<div class='col-md-5'>"
                        +   "<h3>" + data[i].title + "</h3>"
                        +   "<p>" + data[i].description + "</p>"
                        +   "<a class='btn btn-primary' href=" + data[i].url + ">View Project"
                        +     "<span class='glyphicon glyphicon-chevron-right'></span>"
                        +   "</a>"
                        +"</div>"
                        +"<hr>";
        mainContainer.appendChild(div);
        mainContainer.append(document.createElement("hr"))
    }
}
