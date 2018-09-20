$(document).ready(function () {
   $.getJSON("/api/posts",function (data) {
           $.each(data,function(index,element){
               var title = element.title;
               if(title.length > 50){
                   title = title.substring(0,25) +"..."
               }
               $(".postlist").append("<li><a href='#' value='" + element.id +"'>"+ title +"</a><span>"+element.date +"</span></li>");
           })
       }
   );
  
    $(".postlist").on("click","li a",function(e){
        e.preventDefault();
        var id = $(this).attr("value");
        $.getJSON("./api/post/"+id,function (data) {
                var titleElement = document.getElementById("modalTitle");
                var bodyElement = document.getElementById("modalBody");
                titleElement.innerText = data.title;
                bodyElement.innerText = data.body;
            }
            );
            $(this).attr("data-toggle", "modal");
            $(this).attr("data-target", "#postmodal");
        });

    $(".navbar li a").click(function (e){
        e.preventDefault();
        $(this).attr("data-toggle", "modal");
        $(this).attr("data-target", ".bd-example-modal-sm");
        setTimeout(function() {
            $(".bd-example-modal-sm").modal('hide');
          }, 5000);
    });
});

