var navFlag = false;

$(document).ready(function(){
    $(".slide-toggle").click(function(){
        
        let sidebar = $(".sidebar");
        
        if(sidebar.css("width") === "300px"){
            $(".sidebar").animate({
                width: "0px"
            });
            $(".sidebarOverlay").css({"display": "none"})
        }
        else if(sidebar.css("width") === "0px"){
            $(".sidebar").animate({
                width: "300px"
            });
            $(".sidebarOverlay").css({"display": "block"})
        }
    });
    
    $(".exit-sidebar").click(function(){
       let sidebar = $(".sidebar");
        
        if(sidebar.css("width") === "300px"){
            $(".sidebar").animate({
                width: "0px"
            });
            $(".sidebarOverlay").css({"display": "none"})
        }
        else if(sidebar.css("width") === "0px"){
            $(".sidebar").animate({
                width: "300px"
            });
            $(".sidebarOverlay").css({"display": "block"})
        }
    });
    if($("title").html() === "Home"){
        $(".navbar").css({"background-color":"transparent"});
//        $(".logoCircle").css({"background-color":"white"});
    }
    
    if($("title").html() === "Photo Gallery"){
        $(".navbar").css({"background-color":"transparent"});
//        $(".logoCircle").css({"background-color":"white"});
    }
    
    
    var ht = $('nav').height(); 
    var additionalSpacing = 50;

    // help for this scroll function provided by http://jsfiddle.net/5d922roc/

    $(window).scroll(function() {
        var scroll = $(window).scrollTop(); 
        if(scroll > ht + additionalSpacing && navFlag == false){
            navFlag = true;
            
            
            $('.navbar').css({'background-color': '#79CDCD'});
        }

        if(scroll < ht + additionalSpacing && navFlag == true){
            navFlag = false;
            
            $('.navbar').css({'background-color': 'transparent'});
        }
    });
    
});

function nextSlide(){
    var currentElement = $(".active");
    currentElement.fadeOut().removeClass("active");
    var currentSlideNumber = currentElement.attr("id");
    console.dir(currentSlideNumber);
    
    setTimeout(function(){ 
        if(!currentSlideNumber.localeCompare("slide1")){
            $("#slide2").fadeIn(300).addClass("active");
        }
        else if(!currentSlideNumber.localeCompare("slide2")){
            $("#slide3").fadeIn(300).addClass("active");
        }
        else {
            $("#slide1").fadeIn(300).addClass("active");
        } 
    }, 400);
}

function previousSlide(){
    var currentElement = $(".active");
    currentElement.fadeOut().removeClass("active");
    var currentSlideNumber = currentElement.attr("id");
    
    setTimeout(function(){ 
        if(!currentSlideNumber.localeCompare("slide1")){
            $("#slide3").fadeIn(300).addClass("active");
        }
        else if(!currentSlideNumber.localeCompare("slide2")){
            $("#slide1").fadeIn(300).addClass("active");
        }
        else {
            $("#slide2").fadeIn(300).addClass("active");
        }
    }, 400);
    
}

function selectTab(evt, action) {
    var i, tabHiddenContent, links;
    tabHiddenContent = document.getElementsByClassName("tabHiddenContent");
    for (i = 0; i < tabHiddenContent.length; i++) {
        tabHiddenContent[i].style.display = "none";
    }
    links = document.getElementsByClassName("tablinks");
    for (i = 0; i < links.length; i++) {
        links[i].className = links[i].className.replace(" active", "");
    }
    document.getElementById(action).style.display = "block";
    evt.currentTarget.className += " active";
}


function showLoader() {
    $("#loader").addClass("loader");
}

// USE CASE 4
// will detect which fashion to filter/sort
// ex.) descending/ascending rating, rating zone, etc.
// input: filter options
// output: updates displayed photo order
function filter(){
    
}